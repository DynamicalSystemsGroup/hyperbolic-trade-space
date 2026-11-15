# Issue admissibility conditions

A draft becomes an issue only when every condition below holds. Each row says whether the condition is verified by
machine (conformance: the field is there and well formed) or judged by a code owner (fitness: the content is sound),
and what enforces or records it. The admissibility workflow checks the machine rows when a draft is opened or edited
and, on a failure, comments with the gap named and keeps the `draft` label. The code owner rows are decided by the
person who removes the label; the label change records who and when.

| Condition | Kind | Enforced or recorded by |
|---|---|---|
| The scope says what is delivered and what is not | conformance, machine | the template's scope and non-goals fields present and non-empty |
| The scope is bounded: one package a reviewer can judge, not a programme | fitness, a code owner | the code owner's reading before the label is removed |
| The blast radius names the files and surfaces the work may touch | conformance, machine | the template's blast-radius field present and non-empty |
| The blast radius is sane: small enough to review in one sitting | fitness, a code owner | the code owner's reading |
| Good is stated: what the work aims at | conformance, machine | the field present and non-empty |
| Good enough is stated as items, each marked conformance or fitness | conformance, machine | the field present; each item carries one of the two marks |
| The good-enough items are checkable as written | fitness, a code owner | the code owner's reading; an item that cannot be checked is returned |
| Open decisions, if any, are listed with plain options | conformance, machine | the field present (it may say none) |
| The approach is left to the person doing the work | fitness, a code owner | the code owner returns a draft that prescribes the how |
| Only a code owner turns a draft into an issue | conformance, machine | the `draft` label is removable by code owners only; any other removal is reverted |

The template that asks for each field is [`ISSUE_TEMPLATE/scope-of-work.yml`](ISSUE_TEMPLATE/scope-of-work.yml).
