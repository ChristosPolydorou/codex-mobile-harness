# iOS and KMP iOS gates

Inspect the live target architecture and deployment targets before planning or
implementation: workspace/project, schemes/configurations/destinations, Swift
and Xcode versions, SPM/dependency manager, package graph, UI framework,
navigation, persistence, generated/interoperability boundaries, shared KMP
ownership, and test plans. Choose SwiftUI, UIKit, Observation, Combine,
async/await, persistence, and navigation patterns only from that evidence and
applicable authority; do not use this gate as permission to migrate or
modernize.

## Deterministic complexity floors

Changes involving any of the following are at least L3: actor isolation;
MainActor hops; task cancellation; AsyncSequence or Combine ownership; SwiftUI
state ownership; navigation races; UIKit/SwiftUI interoperability; or
multi-target/package contracts.

Changes involving any of the following are at least L4 **and require explicit
human approval before implementation**: Core Data or SwiftData migrations;
authentication, Keychain, or cryptography; entitlements, capabilities, or
signing; background modes/tasks; deep-link trust boundaries; SPM dependency
additions; public framework API changes; or UIKit/SwiftUI migration.

Apply every matching floor and route at the highest level. Escalate to L5 when
the live facts meet an L5 condition in the shared complexity policy, including
payment/transfer/OTP/session/PII risk, destructive migration, plausible data
or credential loss, or release/signing impact.

## Mandatory shared human-approval gates

A complexity floor is not an approval waiver. Regardless of its L3 minimum
classification, an iOS change requires explicit human approval before
implementation when it changes entitlements, signing, capabilities, Keychain,
background modes, deep links, actor isolation, or persistence migration. This
is the complete iOS-specific approval list from the shared router and approved
specification. It applies in addition to the L4 approval triggers above and to
the shared L4/L5, security, persistence, migration, public-contract, and
new-dependency approval gates.

## Preservation gates

Preserve validation, error handling, analytics/audit behavior, accessibility,
localization, session behavior, privacy declarations, secret/PII handling, and
safe logging. Preserve UIKit, SwiftUI, or hybrid boundaries; established state
and navigation ownership; KMP framework/export boundaries; package/dependency
resolution; and generated/API contracts unless the approved contract explicitly
changes them.

## Required review

Review the changed path for all applicable concerns:

- Sendable and actor isolation, MainActor UI mutation, cross-actor hops,
  structured task lifetime/cancellation, stale-response races, and cleanup;
- retain cycles in closures/delegates/tasks, AsyncSequence/Combine subscription
  ownership/cancellation, and durable state versus one-shot event ownership;
- SwiftUI `State`, bindings, observable ownership, identity, task lifecycle,
  navigation identity/races, state restoration, accessibility, and repeated
  presentation behavior;
- UIKit controller containment, view lifecycle, delegates/closures, main-thread
  updates, Auto Layout/safe areas, trait/Dynamic Type/keyboard changes, and
  UIKit/SwiftUI interoperability where already present;
- scene/app lifecycle, route/deep-link input validation, back/dismiss/result
  delivery, authentication boundary, and restoration behavior;
- nullability/Objective-C/Kotlin/generated contracts, network mapping,
  loading/empty/error/retry states, retained validation, idempotency, and
  persistence behavior;
- plist/privacy declaration, entitlement/capability, signing, Keychain/data
  protection, permission usage description, background mode/task, notification,
  universal link, biometric, and deployment-target implications; and
- package resolution, build schemes/destinations, targeted Swift/Xcode tests,
  VoiceOver, localization, Dynamic Type, contrast, reduced motion, and iOS
  versus KMP Android evidence boundaries.

## Verification selection

Discover the actual workspace/project, shared schemes, test plans,
configurations, and destinations before naming `xcodebuild` commands. Run the
narrowest meaningful Swift/Xcode test, framework/scheme build, UI/snapshot,
simulator/device flow, archive/signing, or release check supported by the
repository and required by risk. A build is not runtime or visual proof; iOS
evidence is not KMP Android proof. Record unavailable checks as `BLOCKED` and
unselected checks as `NOT RUN`.
