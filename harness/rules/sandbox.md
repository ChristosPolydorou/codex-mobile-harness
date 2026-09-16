# Sandbox boundary policy

Every role must remain within its granted sandbox and may use only the tools,
files, network access, and other capabilities made available inside that
sandbox. Inspections, edits, builds, tests, and checks must be performed with
sandbox-available tools and within the granted workspace or other explicitly
permitted paths.

Roles must never request, use, or recommend unsandboxed or elevated bypasses,
host-level access, unrestricted filesystem access, or a workaround intended to
evade the sandbox. A tool failure or unavailable capability is an environment
constraint, not permission to broaden access.

When required evidence cannot be obtained inside the sandbox, stop at the safe
boundary. Record the check as `BLOCKED` or `NOT RUN`, state the unavailable
capability and residual risk, and emit an `ENVIRONMENT_BLOCKER` escalation.
Never claim evidence that was not obtained, and never treat a different
environment or a previous run as a substitute.

This policy guides agent behavior and is not cryptographic enforcement. Actual
sandbox permissions, repository protections, CI, secrets management, and human
review remain separate controls.
