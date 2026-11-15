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
