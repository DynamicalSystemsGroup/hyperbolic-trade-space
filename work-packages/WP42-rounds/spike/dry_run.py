"""The checker's dry run: the glossary drafts and the extended stems against the surfaces.

    uv run --frozen python work-packages/WP42-rounds/spike/dry_run.py

Builds a temporary tree of symlinks to the repository's surfaces (nothing in the repository is
written), with ``glossary.yaml`` replaced by a copy that has ``glossary-drafts.yaml`` merged in
(entries replaced by id or appended, avoid and alias lists as drafted, stems extended) and the
draft texts (``drafts.md``) added as a docs page. Prints the violation counts for three states: the
repository as it is (no baseline), the extended stems alone, and the drafts; and writes the
violations of the last to ``dry_run_violations.txt`` with the tension, objective and loss uses.
"""

from __future__ import annotations

import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_vocabulary as cv  # noqa: E402


def tree(glossary: dict, with_drafts: bool) -> Path:
    d = Path(tempfile.mkdtemp(prefix="wp42-dry-"))
    for name in ("paper", "site", "src", "examples", "README.md"):
        (d / name).symlink_to(ROOT / name)
    (d / "docs").mkdir()
    for p in (ROOT / "docs").iterdir():
        if p.name != "superpowers":
            (d / "docs" / p.name).symlink_to(p)
    if with_drafts:
        (d / "docs" / "wp42-drafts.md").write_text((HERE / "drafts.md").read_text())
    (d / "glossary.yaml").write_text(yaml.safe_dump(glossary, sort_keys=False, width=10**6))
    return d


def run(glossary, with_drafts=False):
    d = tree(glossary, with_drafts)
    return cv.analyse(d)["violations"]


def merged(base, drafts, entries=True, stems=True):
    g = {k: (list(v) if isinstance(v, list) else v) for k, v in base.items()}
    if entries:
        by = {e["id"]: i for i, e in enumerate(g["entries"])}
        for e in drafts["entries"]:
            if e["id"] in by:
                g["entries"][by[e["id"]]] = e
            else:
                g["entries"].append(e)
    if stems:
        g["stems"] = [*g["stems"], *[s for s in drafts["stems"] if s not in g["stems"]]]
    return g


def count(vs):
    return dict(Counter(v.kind for v in vs)), len(vs)


def main():
    base = yaml.safe_load((ROOT / "glossary.yaml").read_text())
    drafts = yaml.safe_load((HERE / "glossary-drafts.yaml").read_text())
    v0 = run(base)
    v1 = run(merged(base, drafts, entries=False))
    v2 = run(merged(base, drafts), with_drafts=True)
    k0 = {v.key for v in v0}
    new1 = [v for v in v1 if v.key not in k0]
    new2 = [v for v in v2 if v.key not in k0]
    print("repository as it is, no baseline:", count(v0))
    print("extended stems only:", count(v1), "new:", len(new1), dict(Counter(v.kind for v in new1)))
    print("drafts (entries, avoid lists, stems, draft texts):", count(v2), "new:", len(new2),
          dict(Counter(v.kind for v in new2)))  # fmt: skip
    drafts_hits = [v for v in v2 if v.file in ("docs/wp42-drafts.md", "glossary.yaml")]
    print("violations in the draft texts or the glossary itself:", len(drafts_hits))
    lines = [
        f"{v.kind}\t{v.file}\t{v.phrase}\t{v.where}"
        for v in sorted(new2, key=lambda v: (v.kind, v.file, v.phrase))
    ]
    (HERE / "dry_run_violations.txt").write_text("\n".join(lines) + "\n")
    by = Counter((v.kind, v.phrase.split()[-1] if v.kind == "stem" else v.phrase) for v in new2)
    print("new violations by kind and stem or phrase:", dict(by))
    for v in drafts_hits:
        print("  DRAFT:", v.kind, v.file, v.phrase, v.where)


if __name__ == "__main__":
    main()
