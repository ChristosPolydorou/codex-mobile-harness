# Deterministic routing

## Route procedure

1. Inspect applicable instructions, repository structure, likely files,
   contracts, and Git state before final classification.
2. Detect explicit mode: `implement`, `plan-only`, or `investigate-only`. If
   absent, infer `implement` only when the user asks to change behavior;
   otherwise ask for the intended mode.
3. Apply [complexity classification](complexity.md), including every
   deterministic floor. Record facts, not impressions.
4. Emit the route record before delegation:

   ```text
   mode: <implement | plan-only | investigate-only>
   complexity: <L0-L5>
   risk floors: <none or explicit triggering facts>
   investigator model: <none or approved model + high>
   planner model: <none or approved model + high>
   executor model: <none or approved model + high>
   verifier model: <none or approved model + high>
   approval requirement: <none | explicit human approval and reason>
   next artifact: <investigation report | Implementation Contract | execution record | verification report | escalation report>
   ```

5. Dispatch the named role at the exact model and `high` effort. Preserve
   stated route records and phase artifacts as immutable inputs unless the
   Planner revises the Implementation Contract.

## Implementation model matrix

| Level | Investigator | Planner | Executor | Verifier |
| --- | --- | --- | --- | --- |
| L0 | `none`, or `gpt-5.6-luna` high when investigation is required | `none` | `gpt-5.6-luna` high | deterministic checks or `gpt-5.6-luna` high |
| L1 | `none`, or `gpt-5.6-luna` high when investigation is required | `none` by default | `gpt-5.6-luna` high | `gpt-5.6-luna` high |
| L2 | `none`, or `gpt-5.6-terra` high when investigation is required | `gpt-5.6-terra` high | `gpt-5.6-luna` high | `gpt-5.6-terra` high |
| L3 | `none`, or `gpt-5.6-sol` high when investigation is required | `gpt-5.6-sol` high | `gpt-5.6-luna` high or `gpt-5.6-terra` high | `gpt-5.6-terra` high |
| L4 | `none`, or `gpt-6-astra` high when investigation is required | `gpt-6-astra` high -> human approval | `gpt-5.6-terra` high | `gpt-5.6-sol` high |
| L5 | `none`, or `gpt-6-astra` high when investigation is required | `gpt-6-astra` high -> human approval | `gpt-5.6-terra` high | `gpt-5.6-sol` high, or `gpt-6-astra` high only for exceptional critical review |

## Terminal model matrix

Every terminal route record names all four roles. Inactive roles are explicitly
`none`; terminal routes do not inherit active implementation roles.

- L0/L1 plan-only: Investigator `none`; Planner `gpt-5.6-luna` high; Executor `none`; Verifier `none`.
- L2 plan-only: Investigator `none`; Planner `gpt-5.6-terra` high; Executor `none`; Verifier `none`.
- L3 plan-only: Investigator `none`; Planner `gpt-5.6-sol` high; Executor `none`; Verifier `none`.
- L4/L5 plan-only: Investigator `none`; Planner `gpt-6-astra` high; Executor `none`; Verifier `none`.
- L0/L1 investigate-only: Investigator `gpt-5.6-luna` high; Planner `none`; Executor `none`; Verifier `none`.
- L2 investigate-only: Investigator `gpt-5.6-terra` high; Planner `none`; Executor `none`; Verifier `none`.
- L3 investigate-only: Investigator `gpt-5.6-sol` high; Planner `none`; Executor `none`; Verifier `none`.
- L4/L5 investigate-only: Investigator `gpt-6-astra` high; Planner `none`; Executor `none`; Verifier `none`.

`plan-only` stops after a decision-complete Implementation Contract and an
approval request when required. `investigate-only` uses a read-only
Investigator and stops after an investigation report. A request to execute an
existing plan must first verify that the contract is current, complete,
approved when necessary, and matches the live repository; otherwise escalate.
Plan-only never spawns an Executor or Verifier. Investigate-only never spawns
a Planner, Executor, or Verifier.

Human approval is required for L4/L5 and for new subsystem/pattern,
architecture or framework/UI migration, authentication/authorization,
cryptography/Keychain/Keystore, payment/transfer/OTP/session/PII behavior,
persistence/schema/retention, Android permissions/services/receivers/deep
links/background execution/signing/R8/DI boundary, iOS
entitlements/signing/capabilities/Keychain/background modes/deep links/actor
isolation, public contract expansion, or a new dependency. Approval applies
only to the written scope and architecture.
