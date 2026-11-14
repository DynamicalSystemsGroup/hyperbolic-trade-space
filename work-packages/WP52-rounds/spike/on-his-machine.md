# WP52 D-2: on his machine

Searched (filenames with find and grep; content with grep over Markdown and text, `mdfind` for the phrase): `~/Documents`,
`~/Downloads`, `~/Documents/GitHub`. `~/Library/Mobile Documents` is not readable (`ls`: "Operation not permitted");
it was not searched. `pypdf` is not installed in the repository's environment, so PDF content was not searched by the
rule; filenames only, and `pdftotext` was used on three public published PDFs and nothing else.

"why is their data": no file name or content outside this repository matches the phrase (the repository hits are the WP52
brief itself). The nearest title is `why-is-there-data-2024.md` (below).

Dates are file modification dates. R = read (public published item). L = listed only (private, draft, or not shown to be
public). The three GitHub repositories marked private were checked with `gh api` (private: true).

## Public items, read

| Path | Date | What |
|---|---|---|
| `~/Downloads/Ethnographic Praxis - 2026 - Rennie - Building the Loop  The Role of Ethnography in Artificial Organisational Intelligence.pdf` | 2026-04-12 | the published EPIC PDF; read in full (R). Copies "(1)" 2026-04-25 and "(2)" 2026-07-25 not opened. |
| `~/Downloads/BSci Model-Based Institutional Design.pdf` | 2025-06-27 | two-page firm flyer; first page and a marker scan only (R) |
| `~/Documents/GitHub/mission-twin-glossary/sources/archive/roth-economist-as-engineer-2002.pdf` | 2026-09-05 | the Econometrica article, 38 pp (R); copies in `mission-twin-reference-architecture/sources/archive/` (2026-09-01) |
| `~/Downloads/Meltdown (1).md` (and `Meltdown.md` 2025-08-28, `Meltdown (2).pdf`, `(3).pdf`, `Meltdown.pdf` 2025-09-22) | 2025-09-22 | the firm's public blog post; a keyword scan and the opening lines only (R) |

## Listed, not read

Public-looking published items of other titles, matched by name but not opened because they were not needed:

- `~/Downloads/Ethnographic Praxis - 2022 - RMIT - The Ethnography of a  Decentralized Autonomous Organization   DAO   De-mystifying.pdf` (2025-09-21) and `... (1).pdf` (2026-08-01)
- `~/Downloads/Zargham_Shorish_GDS_Part_I_Foundations_2022*.pdf` (2025-01-01 to 2026-09-01), `~/Downloads/Zargham_and_Ben_Meir_Chapter*.pdf` (2025-02-15), `~/Downloads/BSci Market Design.pdf` (2025-06-27), `~/Downloads/BSci Field Survey and Incentive Mapping.pdf` (2025-06-27)

Marked draft, or private, or a version in progress, by name or by repository; not read, not quoted:

- `~/Downloads/CSCW-draft-attention-economy.pdf` (2024-01-23): name says draft; the attention-economy paper's draft
- `~/Downloads/EPIC FULL PAPER drafting 10 June.md` (2025-09-21): name says drafting
- `~/Downloads/NabbenK_ZarghamM_2022_060822_EPIC_V2_CURRENT.pdf` (2022-09-16); `~/Downloads/Ethnography as a Feedback Loop_ ..._v1_200622.pdf` (2022-08-14) and `... - Google Docs.pdf` (2022-08-22); `~/Downloads/SourceCred ethnography - Google Docs.pdf` (2023-07-29); `~/Downloads/NabbenK_EPIC presentation 121022.pptx` (2022-09-28): working versions, not shown to be released
- `~/Downloads/Zargham_ Towards Model-Based Institutional Design.pdf` (2023-04-21): "Towards" suggests a draft; not read
- `~/Downloads/koi_direction_note*.md` (ten files, all 2026-05-09), `~/Downloads/Knowledge complex trl 0*.md`, `.docx`, `Knowledge complex memo.pdf` (2025-12-20 to 2026-04-11): direction and memo notes; content mentions the titles, not read
- `~/Documents/GitHub/dsg-ant-private/` (private repository): `wiki/Inscription-dsg--building-the-loop.md`, `wiki/Inscription-dsg--attention-economy-paper.md`, `wiki/Actant-dsg--ellie-rennie.md` (all 2026-08-17), plus `abstract.md`, three files under `briefs/`, twelve under `wiki/` that mention the titles
- `~/Documents/GitHub/mission-twin-glossary/` (private): `sources/rennie-aoi-building-the-loop-2025.md`, `sources/roth-economist-as-engineer-2002.md`, `sources/nabben-ai-constituted-system-2024.md`, `sources/why-is-there-data-2024.md` (all 2026-09-05). Exception: the first 30 lines of `why-is-there-data-2024.md` were read to take the citation (title, authors, SSRN number) and nothing of its excerpts is used.
- `~/Documents/GitHub/mission-twin-reference-architecture/` (private): the same four files (2026-09-01) and `sources/protocols-and-institutions-v2.md`
- `~/Documents/GitHub/trl-knowledgebase/` (private): `wiki/PriorArt-AOIBuildingTheLoop.md`, `PriorArt-RothEconomistAsEngineer.md`, `PriorArt-ParticipatoryDigitalEthnography.md`, `PriorArt-OstromIAD.md`, `PriorArt-NabbenAIConstitutedSystem.md`, `PriorArt-ProtocolsAndInstitutions.md`, `PriorArt-Meltdown.md` (all 2026-08-29); six files under `instances/`, one under `notes/`
- `~/Documents/GitHub/ant-rdf/` (28 files naming the titles; `briefs/koi-ethnographic-network.md` 2026-09-15; the KOI inscription of Building the Loop 2026-09-15), `brand-knowledge-complex/` (Ostrom Workshop actor and edge notes; 2026-01-11), `metagov-journal/wiki/Person-ellie-rennie.md` (2026-04-25), `distributed-knowledge-processing/experiments/03-koi-two-readings-collaboration/comparison-remote-erennie-20260602.md` (2026-06-02), and single files in `sbir-np004`, `Mission_Twinning_Service_Brief`, `dsg-atlas`, `Systemica`, `koi-search-v2`, `dsg-compliance-engine`, `civic-ai-tools`, `letters-of-support`, `tcpm-demo`, `mtg-kc`, `kernel-f9b9872`, `mission-twins-kernel-alpha`: knowledge bases and client or programme documents; not read

Privacy note: the content grep over Markdown opened these files to match a pattern but no text from them is used,
quoted or paraphrased anywhere in D-1 or D-3. Nothing under `~/Library/Mobile Documents` was read.

## Not found on his machine

A file titled or containing "why is their data"; "computer-aided institutional design"; any public copy of the
computer-aided governance or computer-aided ethnography posts (both were read online).
