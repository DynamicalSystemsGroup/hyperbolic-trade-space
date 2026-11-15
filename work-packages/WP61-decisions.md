# WP61 — Decisions: the work-packages directory, archived and indexed

## Direction (15:46 EST, 2026-11-15)

**Supervisor, verbatim:** "one thing i noticed while reviewing is that the status information in the workpackages
directory seems pretty long out of data, you may want to update your tracking protocol and how you organize
historical workpackages. complete work packages can probably be archived as along as we maintain a record of the git
hash where they were delivered"

**Applied as (approved by the driver as his proxy, housekeeping under the tidiness mandate):** one index file is the
status of every package, with the dev commit where each landed; completed packages' documents move to an archive
folder, except files that code, tests, notebooks or docs read, which stay where they are and are listed; the scope
files carry no live status line; the protocol is written into the directory's README and followed from here (a
package is archived at its landing with its hash).

**Supervisor, verbatim (15:48 EST):** "we may also want to gitignore the archive because those records being on the history at every commit is a lot of storage. i think it should suffice to keep the records needed to dereference them from an older commit. maybe we need 2 values the one where the scope was locked and the one where the results were accepted"

**Applied as:** no archive folder in the tree: a completed package's documents are removed from the working tree at its landing and read back from history by hash; `INDEX.md` records two commits per package, the one where the scope was locked (its approval) and the one where its results were accepted or landed, with the command to dereference (`git show <hash>:work-packages/<file>`); `work-packages/archive/` is git-ignored for local copies; files read by code, tests or docs stay tracked in place.

**Supervisor, verbatim (15:52 EST):** "you likely need a similar protocol for supporting content, documentation, research spike outputs. this is more directed at thinning out docs. i don't want a bloated repo but i don't want to lose the history of work"

**Applied as (WP62, after WP61 lands, the same index):** an inventory of the supporting content outside the packages (`docs/superpowers/notes/`, the paper's notes and browser records, spike outputs, scratch artifacts, old figure rounds) classified as live (read by code, tests, docs or CLAUDE.md, or current guidance) or historical; the historical leave the tree at one commit and are listed in `INDEX.md`'s second table with the commit that holds them and their purpose; nothing is lost from history; the protocol in the README covers them (a note or spike output is removed when its package lands, with its hash).

**Supervisor, verbatim (15:53 EST):** "i mean specifically the stuff under superpowers which is essentially prompt residue by most interpretations"

**Applied as (WP62, scoped after WP61 lands):** `docs/superpowers/` is retired as a location. The notes that are live guidance (claims-review, figure-review, proof-conventions, sklearn-conformance, vocabulary-review, presentation-framing, user-journeys, notation, residual-review, reader-grid, verification-strategy, abstraction-gaps, the design spec) move to a plain `notes/` folder at the repository root with every reference in CLAUDE.md, the tests, the scripts and the paper updated; the spike folders and the rest (spike-facet-refit, spike-figure1, spike-horopca, spike-sysml-diagrams, figure-candidates, paper-sources, adcs-tensions-probe, kernel-direction, references-verified, paper-prior-art-sources) leave the tree at one commit and enter the index's second table with the commit that holds them, except files that tests or scripts import (bench_oracle.py, project.py), which move with their readers updated or stay with the index naming the reader.

**Supervisor, verbatim (15:55 EST):** "but really anything else in the repo that is historical rather than part of the delivered content in the paper, the package, the doc site, the worked examples or the boundary content detailing our future work directions based on our research spikes."

**Applied as (the rule WP62 scopes against, repository-wide):** the tree holds the delivered content and what builds and checks it (the package, the tests, the derivations, the paper with its generators and figures, the docsite, the worked examples, the glossary, the register, the contract, the workflows), the live guidance for working on it (CLAUDE.md, the notes that move to `notes/`), the boundary content on the future directions drawn from the research spikes (the readouts of WP36, WP41, WP43, WP48, WP50, WP52 and the ternary spike, kept together under `notes/directions/` or cited from the paper's Future work), and the live packages with the index, the board and the driver log. Everything else is historical: it leaves the tree at one commit, recorded in the index with the commit that holds it. WP62's first deliverable is the inventory of every top-level path with its class and disposition, for the driver's approval as proxy before a file moves.

**Supervisor, verbatim (15:58 EST), the heuristic:** "the heuristic i want you to keep in mind is that * the repos job is current state * the git histories job is the historical trajectory * indexes and ledgers of past comments in state make the historical material discoverable and dereferencable on demand"

**Applied as:** the rule of WP61 and WP62 and of every landing after them: the tree is the current state; history is the trajectory; the index and the ledgers in the tree (`INDEX.md`, the driver log, the decisions files of live packages, the length ledger, the claims register) make past material discoverable and dereferenceable by hash. Added to CLAUDE.md under Process.
