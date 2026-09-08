# Git and workspace policy

Perform read-only Git inspection before edits and a final task-attributable diff
review before any completion claim. Preserve every pre-existing dirty hunk and
report whether the workspace is Git-backed.

Never discard, reset, clean, overwrite, stage, commit, push, rebase, or
force-update user work unless the user explicitly authorizes the specific
operation and repository policy permits it. The harness itself never treats
architecture approval as Git-operation approval. Prefer recoverable operations
and report non-Git workspaces honestly. A permission to implement does not
authorize history changes, staging, publication, or destructive cleanup.
