# Escalation and resumption

Stop work and write an escalation report for one or more of these categories:

| Category | Stop condition |
| --- | --- |
| `PLAN_DISCREPANCY` | Live ownership or API differs from the Implementation Contract. |
| `SCOPE_EXPANSION` | An unapproved file, subsystem, dependency, or public contract is required. |
| `RISK_ESCALATION` | Security, privacy, persistence, concurrency, lifecycle, signing, or migration implications appear. |
| `VERIFICATION_CONTRADICTION` | Required evidence fails or contradicts assumed behavior. |
| `ENVIRONMENT_BLOCKER` | Permission, unavailable service/device, corrupted cache, or missing secret prevents evidence. |
| `USER_DECISION_REQUIRED` | Product or architecture alternatives remain. |

The report must contain: observed fact; evidence; contract assumption; impact;
work completed; files touched; safe rollback guidance; and requested decision.
It must also name the category, current route, and whether any user work was
encountered or preserved.

Read-only Investigator, Planner, and Verifier author and return complete
artifact or escalation content in their response; they never write repository
files. The primary controller may persist returned content only during an
authorized implementation workflow and only within approved scope. Plan-only
and investigate-only remain conversation-output-only and modify no workspace
file unless the user separately asks to save the result. Executor may write
only authorized implementation/execution records within its workspace-write
scope. Escalation content may be authored by any active role, not only
Executor.

Only the Planner may revise an Implementation Contract. Only the human may
approve new L4/L5 scope. After the decision or revised contract is available,
resume from the existing Executor with the revised artifact, rather than
spawning an uninformed replacement. Reclassify and request approval again when
the revision adds a risk floor or changes approved scope.
