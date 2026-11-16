"""WP72 market maker: fetch a Uniswap v2 pair's event logs from a public Ethereum JSON-RPC endpoint.

``uv run python work-packages/WP72-rounds/fetch_amm.py`` writes, under ``data/amm/`` (ignored by
git), ``logs.jsonl`` (the raw logs, one per line) and ``reserves.csv`` (one row per ``Sync`` event:
block, log index, timestamp, the two reserves, and the event that caused it), and prints the
SHA-256 of each for ``amm-manifest.toml``.

A v2 pair emits ``Sync(reserve0, reserve1)`` each time its reserves change, followed in the same
transaction by ``Swap``, ``Mint`` (liquidity added) or ``Burn`` (liquidity removed); a ``Sync`` with
none of these is a bare ``sync()`` call. The reserves are therefore read per event, not
reconstructed by summing deltas.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "amm"

RPC = "https://eth.drpc.org"
PAIR = "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11"  # Uniswap v2 DAI/WETH
FROM_BLOCK = 12_959_744
TO_BLOCK = 12_989_743  # 30,000 blocks, about four and a half days of August 2021
CHUNK = 100
TOPICS = {
    "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1": "Sync",
    "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822": "Swap",
    "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f": "Mint",
    "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496": "Burn",
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer",
    "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925": "Approval",
}


def rpc(method, params):
    """One JSON-RPC call through the system's curl (the endpoint refuses Python's urllib client)."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    cmd = ["curl", "-s", "-m", "60", "-X", "POST", "-H", "content-type: application/json"]
    for attempt in range(6):
        try:
            r = subprocess.run([*cmd, "--data", body, RPC], capture_output=True, check=True)
            out = json.loads(r.stdout)
            if "error" in out:
                raise RuntimeError(out["error"])
            return out["result"]
        except Exception as e:
            if attempt == 5:
                raise
            print("retry", method, e)
            time.sleep(2 * (attempt + 1))


def fetch():
    OUT.mkdir(parents=True, exist_ok=True)
    token0 = "0x" + rpc("eth_call", [{"to": PAIR, "data": "0x0dfe1681"}, "latest"])[-40:]
    token1 = "0x" + rpc("eth_call", [{"to": PAIR, "data": "0xd21220a7"}, "latest"])[-40:]
    logs = []
    for start in range(FROM_BLOCK, TO_BLOCK + 1, CHUNK):
        end = min(start + CHUNK - 1, TO_BLOCK)
        logs += rpc(
            "eth_getLogs", [{"address": PAIR, "fromBlock": hex(start), "toBlock": hex(end)}]
        )
        time.sleep(0.2)
    logs.sort(key=lambda x: (int(x["blockNumber"], 16), int(x["logIndex"], 16)))
    with open(OUT / "logs.jsonl", "w") as f:
        for x in logs:
            f.write(json.dumps(x, sort_keys=True) + "\n")
    return token0, token1, logs


def derive(logs):
    """One row per Sync, labelled by the next Swap, Mint or Burn log of the same transaction."""
    rows = []
    for i, x in enumerate(logs):
        if TOPICS.get(x["topics"][0]) != "Sync":
            continue
        cause = "sync"
        for y in logs[i + 1 :]:
            if y["transactionHash"] != x["transactionHash"]:
                break
            kind = TOPICS.get(y["topics"][0])
            if kind in ("Swap", "Mint", "Burn"):
                cause = kind
                break
        data = x["data"][2:]
        rows.append(
            {
                "block": int(x["blockNumber"], 16),
                "log_index": int(x["logIndex"], 16),
                "timestamp": int(x.get("blockTimestamp", "0x0"), 16),
                "reserve0": int(data[:64], 16),
                "reserve1": int(data[64:128], 16),
                "event": cause,
                "tx": x["transactionHash"],
            }
        )
    with open(OUT / "reserves.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if __name__ == "__main__":
    t0, t1, logs = fetch()
    rows = derive(logs)
    counts = {}
    for r in rows:
        counts[r["event"]] = counts.get(r["event"], 0) + 1
    print("token0", t0, "token1", t1, "logs", len(logs), "syncs", len(rows), counts)
    for name in ("logs.jsonl", "reserves.csv"):
        p = OUT / name
        print(name, p.stat().st_size, sha256(p))
