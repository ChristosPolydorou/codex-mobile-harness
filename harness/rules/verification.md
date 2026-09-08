# Verification policy

Verification is evidence for a precisely named claim, not a generic green
signal. Select checks from the live repository's actual variants, tasks,
schemes, destinations, and test infrastructure. Record each check as `PASS`,
`FAIL`, `BLOCKED`, or `NOT RUN`; `NOT RUN` and `BLOCKED` remain visible in the
final report with their reason and residual risk.

## Evidence matrix

| Evidence obtained | Directly supports | Does not establish |
| --- | --- | --- |
| Static inspection | A reviewed source/configuration path has the stated text or structure. | Runtime behavior, lifecycle behavior, device/simulator behavior, visual fidelity, installation, launch, or cross-platform parity. |
| Compile | The selected source set/variant type-checks and links under that compile task. | Unit, integration, UI, runtime, visual, installation, launch, or release behavior. |
| Unit test | The exercised unit behavior under the test environment. | Device/simulator behavior, visual fidelity, full navigation/lifecycle, installation, or launch behavior. |
| Integration/UI test | The specific exercised integration/UI flow in its named environment. | Unexercised variants, device/simulator parity, visual fidelity, installation, launch, or release behavior unless directly observed. |
| Signature or build artifact | The named artifact was built or signed as checked. | Installation, first launch, runtime behavior, device behavior, or App Store/Play release acceptance. |
| Android-only evidence | The named Android source set, variant, or device/emulator condition. | KMP iOS framework, Xcode host, iOS simulator/device, or iOS visual/runtime behavior. |
| iOS-only evidence | The named iOS target, scheme, simulator, or device condition. | KMP Android source set, Gradle variant, Android emulator/device, or Android visual/runtime behavior. |

Never substitute a previous run, a different variant, static inspection, a
compile, or an artifact for the evidence named in an acceptance criterion.

## Independent Verifier handoff

The independent Verifier receives all of the following before review:

- the original request and acceptance criteria;
- the route decision, complexity, risk floors, and approval requirement;
- baseline Git status/diff, including pre-existing dirty work;
- final task-attributable diff and final Git status;
- exact command outputs and direct manual-observation results, including every
  `PASS`, `FAIL`, `BLOCKED`, and `NOT RUN` item.

For L2-L5, or whenever the route requires a contract, also provide the current
approved Implementation Contract and its approval evidence. For a direct L0/L1
route, provide an immutable route/execution record plus the explicit
direct-route change budget instead; do not manufacture a Planner artifact.

### Minimum direct-route inputs

The direct-route change budget must state the original observable request and
acceptance criteria; L0/L1 route decision, risk floors, and approval outcome;
in-scope files/symbols; current and expected behavior; exact change; MUST,
MAY, and OUT OF SCOPE boundaries; preservation constraints; exact tests and
checks; and escalation conditions. It is immutable evidence for review unless
an escalation returns the work to planning.

The implementer may explain intent but cannot replace these inputs or verify
its own work. The Verifier uses the verification-report template and reports
evidence boundaries honestly.

## Review gates

The Verifier independently checks, in proportion to the change:

- requested behavior and every acceptance criterion;
- approved scope, non-goals, preservation of user work, and repository
  conventions;
- nullability/type contracts, lifecycle ownership, cancellation/concurrency,
  navigation and durable versus one-shot state;
- security/privacy, authentication/session/PII boundaries, validation, error
  handling, retries, and analytics/audit preservation;
- accessibility semantics and focus, localization/RTL/dynamic-type behavior,
  and user-visible loading/empty/error states;
- Android, iOS, KMP/shared, variant, generated-boundary, and public-contract
  effects; and
- whether selected tests meaningfully exercise the changed risk without
  mocking away the relevant behavior.

Static inspection may establish scope or code-path evidence, but it never
upgrades runtime, visual, device, simulator, installation, launch, release, or
other-platform claims.

## Verdict gate

The verification report orders findings as `BLOCKER`, `MAJOR`, `MINOR`, then
`INFORMATIONAL`, records requirement-by-requirement results, scope result,
evidence table, unrun checks, and residual risks, and ends with exactly one of
`PASS`, `PASS WITH CONCERNS`, or `FAIL`.

`PASS WITH CONCERNS` records each bounded concern and its owner. At L5 it is
not completion evidence until a human explicitly accepts those concerns and
the report records durable acceptance evidence. `FAIL` or a verification
contradiction stops the Executor and requires the escalation path.
