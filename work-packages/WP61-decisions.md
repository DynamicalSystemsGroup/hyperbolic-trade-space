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
