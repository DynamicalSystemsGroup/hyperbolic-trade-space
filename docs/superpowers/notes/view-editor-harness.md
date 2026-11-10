# A minimal harness for the view-editor loops (WP26)

The steps the WP26 round used to read and write the model through the OpenMBEE View Editor
(https://openmbee-view-editor.vercel.app/app) from an agent's browser tools, so a later round repeats them instead
of rediscovering them. Each snippet runs in the editor's page (the browser tool's JavaScript execution); each was
used in the round, and its step in the round's log is named. The editor keeps its work in the browser's local
recovery; no account and no server.

Two of the page's internals are used below, both observed on the editor's build of 2026-11-10 and not a published
interface: the source pane is a CodeMirror 6 editor reached through `.cm-content`'s `cmTile.view` (the older
`cmView` key is absent), and the diagram is a React Flow canvas (`.react-flow__node`, `.react-flow__edge`). If either
moves, the snippets fail loudly (an undefined property), not silently.

## 1. Open the project

Open `/app`; the landing page offers "Restore recovery" for the last project (here "cubesat"). Restoring brings back
the last source text, applied or not: an unapplied edit survived a tab being navigated away (steps 05, 06). Wait
about 8 s after restoring before reading the source pane.

The pane is cramped below about 1000 px; emulate a 1600 x 1000 viewport and use the diagram layout (the third
layout button beside the source/split buttons) to see a whole view (step 08).

## 2. Load a source file verbatim (length and checksum)

The model text comes from the repository's public raw URL at a commit, so nothing is retyped; the view package is
appended after it. The editor's project holds one file, so the two are joined there (the repository keeps them
apart).

```js
const raw = "https://raw.githubusercontent.com/DynamicalSystemsGroup/hyperbolic-trade-space";
window.__cub = await (await fetch(`${raw}/<commit>/examples/adcs/model_v2/cubesat.sysml`)).text();
window.__views = await (await fetch(`${raw}/<commit>/examples/adcs/model_v2/views.sysml`)).text();
const v = document.querySelector(".cm-content").cmTile.view;
const text = window.__cub + "\n" + window.__views;
v.dispatch({ changes: { from: 0, to: v.state.doc.length, insert: text } });
const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(v.state.doc.toString()));
({ len: v.state.doc.length, sha: [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("") });
```

Compare with the files on disk (characters, not bytes: `wc -m`, or Python's `len` and `hashlib.sha256` of
`cubesat + "\n" + views`). In the round both matched: 56,550 characters, sha256 `a4ff88cc447f…` (step 21's note).
A view file not yet pushed was passed inline as a JSON string instead of fetched (step 07). Small edits to the
applied text were made as string replacements on `v.state.doc.toString()` followed by one `dispatch` over the
changed range (steps 17, 19, 21).

## 3. Apply and read the issues panel

Click "Apply source" (find it by its accessible name). Then read the state from the page text:

```js
const t = document.body.innerText;
({ issues: (t.match(/Issues \(\d+\)/) || [""])[0],
   clean: t.includes("No issues in the current applied model"),
   revision: (t.match(/\d+ files · revision \d+/) || [""])[0] });
```

A red banner from an earlier session ("Exploration source correspondence is outside the applied project.") stayed
on screen after clean applies (step 07); the Issues panel is the reading to trust.

## 4. List the views and their render status

Click a view in the Explorer's Views list, wait about 3 s, then:

```js
const nodes = [...document.querySelectorAll(".react-flow__node")]
  .map((n) => n.innerText.replace(/\n+/g, " | ").slice(0, 160));
const edges = [...document.querySelectorAll(".react-flow__edge")]
  .map((e) => (e.getAttribute("aria-label") || "").slice(0, 90));
const msg = (document.querySelector(".model-data-diagram") || {}).innerText || "";
({ n: nodes.length, nodes, e: edges.length, edges, unavailable: msg.includes("Rendering unavailable") });
```

`unavailable` is true for a view whose filter admits a case definition ("The case representation has no renderer
in this foundation", steps 11, 13). Edge labels name the relationship (`satisfy:`, `not satisfy:`, `verify:`,
`typed by:`, `binding =:`), which is how the requirements view was checked against the model (step 12).

## 5. Read the requirements table and the traceability matrix as data

Open the "Requirements table" or "Traceability matrix" tab above the canvas and read the panel's text (tab
separated rows); the matrix's relationship is a select ("Satisfaction" or "Verification"):

```js
document.querySelector(".requirements-panel").innerText;
```

Each panel also has "Export CSV" (not used in the round). Steps 14 to 16.

## 6. Capture a view to an image

The browser tool's screenshot of the pane, one per step, named `NN-slug.jpg` beside the step log; read each image
before acting on it, since the pane's screenshot can lag one action. Fit-to-screen on a tall view leaves the text
unreadable; the node texts of section 4 are the record of what a view shows.

## 7. Export or import the project

The header's "Download project" and "Open" (and the landing page's "Open files or project") go through the
operating system's file dialog, which the browser tools cannot drive; WP26 grants computer use for that dialog only.
Not exercised in the round: the source pane route of section 2 was enough.
