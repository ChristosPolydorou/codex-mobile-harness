# Android and KMP Android gates

Inspect the live target architecture before planning or implementation:
modules/source sets, product flavors/build types, min/target/compile SDK,
Kotlin/AGP/Gradle versions, current UI boundary, navigation, DI, state,
network, persistence, and test tasks. Choose Compose, XML/Views, Hilt, Koin,
manual DI, state primitives, and module boundaries only from that evidence and
applicable authority; do not use this gate as permission to migrate or
modernize.

## Deterministic complexity floors

Changes involving any of the following are at least L3: ViewModel ownership;
StateFlow or SharedFlow one-shot events; coroutine cancellation or dispatchers;
Compose lifecycle collection; navigation races; WorkManager coordination;
Services; or multi-module contracts.

Changes involving any of the following are at least L4 **and require explicit
human approval before implementation**: Room migrations; authentication,
Keystore, or cryptography; permissions; deep-link trust boundaries; background
execution policy; DI boundary redesign; Gradle, plugin, or version-catalog
architecture; dependency additions; R8/ProGuard rules with security or release
impact; or XML/Compose migration.

Apply every matching floor and route at the highest level. Escalate to L5 when
the live facts meet an L5 condition in the shared complexity policy, including
payment/transfer/OTP/session/PII risk, destructive migration, plausible data
or credential loss, or release/signing impact.

## Mandatory shared human-approval gates

A complexity floor is not an approval waiver. Regardless of its L3 minimum
classification, an Android change requires explicit human approval before
implementation when it changes permissions, Services, receivers, deep links,
background execution, signing, R8/ProGuard, or a DI boundary. This is the
complete Android-specific approval list from the shared router and approved
specification. It applies in addition to the L4 approval triggers above and to
the shared L4/L5, security, persistence, migration, public-contract, and
new-dependency approval gates.

## Preservation gates

Preserve existing validation, error handling, analytics/audit behavior,
accessibility semantics, localization, session behavior, PII protections and
safe logging. Preserve the established Compose, XML/View, or hybrid boundary;
the existing DI style and module ownership; resource/token conventions; and
generated/API boundaries unless the approved contract explicitly changes them.

## Required review

Review the changed path for all applicable concerns:

- recomposition safety, stable keys, state hoisting, remembered state, and
  Compose side-effect keys;
- ViewModel/state ownership, StateFlow/SharedFlow one-shot events, and
  lifecycle-aware collection;
- structured concurrency, cancellation propagation, dispatcher ownership,
  duplicate work, and main-thread/UI safety;
- navigation arguments/results/back-stack ownership, navigation races, process
  death/state restoration, and configuration changes;
- view-binding lifecycle and clearing, adapter updates, observer lifecycle,
  and XML/Compose interoperability where already present;
- nullability/platform/generated types, loading/empty/error/retry behavior,
  request/response mapping, and retained validation;
- manifest, component/exported state, intent/deep-link validation, permissions,
  WorkManager, Services, receivers, notification, background execution, and
  storage implications;
- min/target SDK/API-level availability; resources, RTL, large text, focus,
  keyboard/insets, TalkBack semantics, and localization; and
- targeted Gradle tasks/variants, affected module contracts, test coverage,
  and Android versus KMP iOS evidence boundaries.

## Verification selection

Discover actual targeted Gradle tasks and variants before naming commands.
Run the narrowest meaningful unit/contract/UI, compile, lint, resource,
manifest, assembly, instrumentation, device/emulator, or release check that
the repository supports and the changed risk needs. A compile is not runtime
or UI evidence; an Android result is not KMP iOS proof. Record unavailable
checks as `BLOCKED` and unselected checks as `NOT RUN`.
