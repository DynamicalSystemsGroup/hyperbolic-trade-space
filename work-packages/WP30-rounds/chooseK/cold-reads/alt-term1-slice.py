import sys, numpy as np, matplotlib; matplotlib.use("Agg")
sys.path.insert(0,'paper/figures'); sys.path.insert(0,'paper')
import planes
case=planes._case(); _,kt,pl=case._lib()
for tag,pr in (("slew-vs-unitcost",[(6,11),(9,11)]),):
    kt.slice_pairs=lambda est,pr=pr: pr
    f=planes.planes_figure()
    f.savefig(f"work-packages/WP30-rounds/chooseK/cold-reads/alt-term1-{tag}.png",dpi=80)
