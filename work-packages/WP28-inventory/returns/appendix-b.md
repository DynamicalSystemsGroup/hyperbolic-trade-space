# appendix-b

## Q1. What the appendix conveys

For each of the 19 results behind the paper's theorems, it gives the statement, its file, and the proof as numbered steps. Each step pairs a sentence of prose with the one line of SymPy that checks it, and says whether the step is computed, uses a declared axiom or uses a proved result. A checker table at the end ties the whole set to a committed record.

## Q2. Which sentence of the story it serves

Main results items 1 to 4, through the line "Main results (Section 6; each has hypotheses, a sketch and a script)". The appendix carries the full proofs and their scripts behind Theorems 1 to 12, Lemmas 1 and 2 and Proposition 3. It also serves the Section 1 sentence that the justification must be "recognized, reproducible, rigorous". Item 7 (the cubesat case) and item 5 (PCA) are not served.

## Q3. Verdict: advances

The story says each main result has a script. This is the only unit that shows those scripts step by step against the proof's prose, and it holds the axiom ledger entries each step uses. The main text points here 27 times, mostly as one-line pointers ("Appendix B, L4"), so the main text keeps only the sketches and depends on this appendix for the full version. The opening also bounds what the scripts establish: a pencil-and-paper substitute, not formal verification. A careful reader needs that framing to read the results honestly.

## Q4. If repeats

Not applicable.

## Q7. Tables

- `tab-B-how-to-read`: main text points to it: no (no pointer names this part). Would a reader wanting the full version look for it: yes, to learn how to read a step, its address and its three kinds. Verdict: advances. It is the key to the step tables. On the page it is prose and bullets, not a table.
- `tab-B-proof-map`: points to it: no, not by name, though the bare "Appendix B, L1" to "L17" pointers land on its rows. Would a reader look for it: yes, as an index of results with step counts by kind. Verdict: advances, as the index. It lists L-numbers only and never the paper's Theorem numbers.
- `tab-B-proofs-fit` (the per-step tables for L1 to L11): points to it: yes (Appendix B, L1 to L11; L3.9, L4.14 to L4.24, L5.25). Would a reader look for it: yes, for the full proofs of items 1 to 3 (homogeneity, convexity, the geometric program, elasticities, chart, Pareto efficiency). Verdict: advances. Long, so I skimmed it after L5.
- `tab-B-proofs-solver` (the per-step tables for L12 to L17): points to it: yes (Appendix B, L12 to L17, L17.12, L17.13, L17.19, B.2). Would a reader look for it: yes, for the full proofs of item 4 (the levels of guarantee, the stopping declaration and the soft-fit certificate). Verdict: advances. Skimmed.
- `tab-B-checker`: points to it: no, though Section 10's "Appendix B gives one line of code to read each proof step against" is about what it checks. Would a reader look for it: yes, a reader who wants to rerun the check, for the commands and the record's hash. Verdict: advances, though thinly for the story. Its per-file rows largely repeat the ledger lines already given under each proof and the counts in `tab-B-proof-map`. Only the commands, the hash and the signed-symbol counts are new.

## Q9. Things I read twice and still could not place

- "per proof, in the paper's numbering": the appendix numbers results L1 to L17, while the story numbers Theorem 1 to Theorem 12, Lemma 1, Lemma 2 and Proposition 3. Nothing on this page maps Theorem n to Lk, except L14, which is named "Proposition 3". A reader starting from "Theorem 9" cannot tell which entry to open.
- The parts list says "The solver for K > 1 and its three levels of guarantee (L12 to L17)", but the heading reads "B.2 The several-term fit and its levels of guarantee". Two names for the same part.
- "L14. Proposition 3": unlike every other entry, the title gives no statement, so the proof map row says nothing about what is proved.
- Step kinds that do not match their prose. L1.8 is listed "by declared axiom A1", but its prose is about the simplex sum (A2). L5.10 is listed under A3 alone, but its prose cites "F5, A3".
- "Signed symbols declared as hypotheses" (the checker table: 5 for L11, 10 for L13): the term is not explained on the page. The checker text says only "no premise hides in a signed symbol".
