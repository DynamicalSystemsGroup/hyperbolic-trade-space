# Spike: which platform can be the container of record (2026-11-09, the driver)

Question. WP10 Amendment 1 names a pinned container as the environment of record, and the driver
set its platform to linux/amd64 to match CI, telling the supervisor that it would come back to him
if that did not run workably on his Mac. Does it?

## What was run

All on the supervisor's Mac (Apple M1 Max, macOS 26.5, Colima 0.8.1, aarch64 VM, Rosetta for amd64
containers), from a clean checkout of `dev` at 6bb85e7, with the committed Dockerfile; the arm64
image is the same Dockerfile with the base pinned by the multi-arch index digest and the platform
set to linux/arm64. CI facts are from Tests run 42560520228 (ubuntu-24.04, real amd64).

| Environment | Paper notebooks execute | Planted table hash (Appendix C) | Figure 1 data hash |
|---|---|---|---|
| macOS arm64, native (where the outputs were committed) | yes | fa86f857... (committed) | f9d7219d... (pinned) |
| linux/arm64 container, native in Colima | yes, about two minutes for both notebooks and the paper's tests | equal to the committed one | 4040cb8e..., differs |
| linux/amd64 container, Rosetta emulation | **no**: the Jupyter kernel never becomes ready (300 s); the lemma chain, the proof map and the site build do run | not obtained | not obtained |
| linux/amd64, CI hardware | not attempted (tests only) | c127dd4c..., differs | not known |

In the linux/arm64 container `tests/test_paper.py` gives 67 passed, 1 failed (the Figure 1 hash).

## What it shows

1. linux/amd64 is not workable on this Mac as the place to produce the paper's outputs. Getting
   there by switching the VM's emulation is a change to the supervisor's own system; an implementer
   tried it without authority, the VM hung, and the driver restored the configuration.
2. A sha256 of computed floating-point data is not a property of the code. It changes with the
   processor architecture (the planted table: arm64 against amd64) and with the operating system's
   mathematics library on one architecture (Figure 1's data: macOS against Linux, both arm64).
3. The linux/arm64 image runs everything natively and quickly on the author's machine.

## The driver's call (provisional; the supervisor was told it would come back to him)

- **The container of record is linux/arm64**, the same pinned image built for the architecture the
  author's machine runs natively. The paper's committed outputs are produced inside it.
- **Exact equality is asserted only inside the environment of record** (the image sets a variable
  the tests read). Everywhere else, CI on amd64 included, the same quantities are compared within a
  stated tolerance, and each value that is exact only in the environment of record (a hash of
  generated data) is named in one list with its reason. No test is skipped on other platforms.
- The image stays buildable for linux/amd64 from the same pinned index; Appendix F states what is
  known to differ there, measured on CI.
- Not done, and for the supervisor to choose if he prefers it: producing the outputs of record on
  CI's amd64 hardware inside the image and committing them from there, which matches CI exactly but
  cannot be run on his Mac.
