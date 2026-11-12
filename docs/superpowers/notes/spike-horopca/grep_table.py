"""Reading pass: every prose occurrence of 'hyperbolic' (identifiers excluded), with file and sentence."""
import json, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
files = ["paper/paper.ipynb","paper/supporting_material.ipynb","docs/index.md","docs/theory.md","docs/further-reading.md",
         "docs/getting-started.md","docs/examples.md","docs/api.md","glossary.yaml","README.md","claims_register.toml",
         "paper/prior_art.yaml","paper/reading_pass.yaml","paper/myst.yml","mkdocs.yml"]
files += [str(p.relative_to(root)) for p in sorted((root/"docs/user-guide").glob("*.md"))]
files += [str(p.relative_to(root)) for p in sorted((root/"docs").glob("overview*.md"))]
ident = re.compile(r"hyperbolic[_-]trade[_-]space|HyperbolicTradeSpace|hyperbolic-trade-space", re.I)
for f in files:
    p = root/f
    if not p.exists(): continue
    if f.endswith(".ipynb"):
        nb = json.load(open(p, encoding="utf-8")); texts=[]
        for i,c in enumerate(nb["cells"]):
            if c["cell_type"]=="markdown": texts.append((f"{f} cell {i}", "".join(c["source"])))
            else: texts.append((f"{f} cell {i} (code)", "".join(c["source"])))
    else:
        texts=[(f, p.read_text(encoding="utf-8"))]
    for loc,t in texts:
        t2 = ident.sub("PKG", t)
        for m in re.finditer(r"hyperbol", t2, re.I):
            s = max(t2.rfind(". ",0,m.start())+2, t2.rfind("\n",0,m.start())+1, 0)
            e = t2.find(". ", m.end()); e = len(t2) if e<0 else e+1
            n = t2.find("\n", m.end()); e = min(e, n if n>=0 else e)
            print(f"{loc} | {t2[s:e].strip()[:400]}")
