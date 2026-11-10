#!/bin/sh
# Occurrences of "facet" (case-insensitive) by surface, from the repo root. Spike 2026-11-09.
cd "$(dirname "$0")/../../../.." || exit 1
for s in glossary.yaml paper/paper.ipynb paper/supporting_material.ipynb "paper/*.py" "paper/figures/*.py" \
         paper/environment_values.toml paper/length_ledger.toml docs/user-guide docs/theory.md docs/examples.md \
         docs/api.md docs/generated/glossary.md docs/superpowers derivation src tests examples claims_register.toml \
         work-packages/interface-contract.md work-packages/interface-contract.toml scripts site; do
  n=$(eval grep -r -i -o facet $s 2>/dev/null | wc -l | tr -d ' '); printf '%-45s %s\n' "$s" "$n"
done
# notebook cells: markdown vs outputs
uv run python - <<'PY'
import json, re
for nb in ("paper/paper.ipynb", "paper/supporting_material.ipynb"):
    d = json.load(open(nb)); md = out = 0
    for c in d["cells"]:
        s = "".join(c["source"]); n = len(re.findall("facet", s, re.I))
        if c["cell_type"] == "markdown": md += n
        else: out += sum(len(re.findall("facet", json.dumps(o), re.I)) for o in c.get("outputs", []))
    print(f"{nb}: markdown {md}, outputs {out}")
PY
