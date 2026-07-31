"""
Reclassify environmental violation records using Claude Sonnet API with prompt caching.

Strategy:
  1. Deduplicate on (agency, description) — reduces 26,746 records to ~4,413 unique pairs
  2. Batch 10 unique pairs per API call (~442 calls total)
  3. Merge classifications back to the full dataset
  4. Supports resuming from checkpoint if interrupted
"""

import asyncio
import pandas as pd
import anthropic
import json
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
INPUT_CSV   = BASE_DIR / "VT_environmental_violation_with_desc.csv"
OUTPUT_CSV  = BASE_DIR / "VT_env_violation_classified.csv"
CHECKPOINT  = BASE_DIR / "checkpoint.json"   # {dedup_key: label}
PROMPT_FILE = BASE_DIR / "llm_reclassify_env_violation_prompt.md"
KEYS_FILE   = Path(r"D:\Dropbox\fengheliu\tools\keys.txt")

# ── Settings ───────────────────────────────────────────────────────────────────
MODEL       = "claude-sonnet-4-5"
MAX_TOKENS  = 200      # enough for 10 labels
BATCH_SIZE  = 10
CONCURRENCY = 15
BATCH_SAVE  = 50       # save checkpoint every N batches

VALID_LABELS = {
    "air pollution violation",
    "asbestos violation",
    "fuel economy (cafe) violation",
    "water pollution violation",
    "drinking water violation",
    "mtbe violation",
    "pcb violation",
    "pfas violation",
    "oil spill",
    "animal feeding operation violation",
    "hazardous waste violation",
    "radioactive waste violation",
    "underground storage tank violation",
    "pipeline safety violation",
    "oil or gas drilling violation",
    "mining environmental violation",
    "pesticide violation",
    "solid waste violation",
    "lead violation",
    "energy conservation violation",
    "environmental violation",   # fallback
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def read_api_key() -> str:
    for line in KEYS_FILE.read_text().splitlines():
        if line.startswith("claude:"):
            return line.split(":", 1)[1].strip()
    raise ValueError("Claude key not found in keys.txt")


def make_dedup_key(agency, description) -> str:
    """Stable string key for a (agency, description) pair."""
    a = str(agency).strip()   if pd.notna(agency)      else "__NA__"
    d = str(description).strip() if pd.notna(description) else "__NA__"
    return f"{a}|||{d}"


def build_batch_message(rows: list[dict]) -> str:
    """Build a user message for a batch of records, numbered 1..N."""
    lines = []
    for i, row in enumerate(rows, 1):
        agency      = str(row['agency']).strip()      if pd.notna(row['agency'])      else 'Unknown'
        description = str(row['description']).strip() if pd.notna(row['description']) else 'Not provided'
        lines.append(f"Record {i}:\nAgency: {agency}\nDescription: {description}")
    batch_prompt = (
        "Classify each record below into one of the 20 categories. "
        "Respond with exactly one line per record in the format:\n"
        "1: <category label>\n2: <category label>\n...\n\n"
    )
    return batch_prompt + "\n\n".join(lines)


def parse_batch_response(text: str, batch_size: int) -> list[str]:
    """Parse numbered response lines into a list of labels."""
    labels = {}
    for line in text.strip().splitlines():
        m = re.match(r"^\s*(\d+)\s*[:\.\)]\s*(.+)$", line)
        if m:
            idx   = int(m.group(1))
            label = m.group(2).strip().lower()
            if label not in VALID_LABELS:
                label = "environmental violation"
            labels[idx] = label
    # Fill any missing indices with fallback
    return [labels.get(i, "environmental violation") for i in range(1, batch_size + 1)]


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {}


def save_checkpoint(results: dict):
    CHECKPOINT.write_text(json.dumps(results))


# ── Main classification ────────────────────────────────────────────────────────

async def classify_batch(
    client: anthropic.AsyncAnthropic,
    system_prompt: str,
    semaphore: asyncio.Semaphore,
    batch_rows: list[dict],
) -> list[tuple[str, str]]:
    """Returns list of (dedup_key, label) for each row in batch."""
    user_message = build_batch_message(batch_rows)
    async with semaphore:
        for attempt in range(5):
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=[{
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=[{"role": "user", "content": user_message}],
                )
                labels = parse_batch_response(
                    response.content[0].text, len(batch_rows)
                )
                return [
                    (make_dedup_key(row['agency'], row['description']), label)
                    for row, label in zip(batch_rows, labels)
                ]
            except anthropic.RateLimitError:
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                if attempt == 4:
                    print(f"  Batch failed: {e}")
                    return [
                        (make_dedup_key(row['agency'], row['description']), "error")
                        for row in batch_rows
                    ]
                await asyncio.sleep(2 ** attempt)
    return [(make_dedup_key(row['agency'], row['description']), "error") for row in batch_rows]


async def run():
    api_key       = read_api_key()
    system_prompt = PROMPT_FILE.read_text()

    df = pd.read_csv(INPUT_CSV, low_memory=False)
    print(f"Total records: {len(df):,}")

    # ── Deduplicate ────────────────────────────────────────────────────────────
    df["_dedup_key"] = df.apply(
        lambda r: make_dedup_key(r['agency'], r['description']), axis=1
    )
    unique_rows = (
        df.drop_duplicates(subset="_dedup_key")[["agency", "description", "_dedup_key"]]
        .to_dict("records")
    )
    print(f"Unique agency+description pairs: {len(unique_rows):,}")

    # ── Resume from checkpoint ─────────────────────────────────────────────────
    results = load_checkpoint()
    todo    = [r for r in unique_rows if r["_dedup_key"] not in results]
    print(f"Already classified: {len(results):,} | Remaining: {len(todo):,}")

    # ── Build batches ──────────────────────────────────────────────────────────
    batches = [todo[i:i+BATCH_SIZE] for i in range(0, len(todo), BATCH_SIZE)]
    print(f"Batches to process: {len(batches):,} (batch size={BATCH_SIZE})")

    client    = anthropic.AsyncAnthropic(api_key=api_key)
    semaphore = asyncio.Semaphore(CONCURRENCY)

    tasks = [classify_batch(client, system_prompt, semaphore, b) for b in batches]

    done = 0
    for coro in asyncio.as_completed(tasks):
        pairs = await coro
        for key, label in pairs:
            results[key] = label
        done += 1
        if done % 50 == 0:
            print(f"  {done:,} / {len(batches):,} batches done "
                  f"({done*BATCH_SIZE:,} records classified)")
        if done % BATCH_SAVE == 0:
            save_checkpoint(results)

    save_checkpoint(results)
    print(f"Classification done. {len(results):,} unique pairs classified.")

    # ── Merge back to full dataset ─────────────────────────────────────────────
    df["primary_offense_new"] = df["_dedup_key"].map(results)
    df = df.drop(columns=["_dedup_key"])

    out = df[["unique_id", "primary_offense_new"]]
    out.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(out):,} rows to {OUTPUT_CSV.name}")

    # ── Distribution ──────────────────────────────────────────────────────────
    print("\nClassification distribution:")
    print(out["primary_offense_new"].value_counts().to_string())


if __name__ == "__main__":
    asyncio.run(run())
