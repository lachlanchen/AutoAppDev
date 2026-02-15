# Development Ordering Rationale

## Phase strategy
The sequence is designed to deliver a usable product early, then expand capability in layers while minimizing cross-platform regressions.

1. `home_shell` (seq 1-17)
- Establishes app spine first: home states (disconnected/connected/update/recording toasts), profile entry, device settings, recording settings, firmware flow, and about screen.
- This creates the baseline navigation, data models, and device-state rendering required by nearly every downstream feature.

2. `permission_setup` (seq 18-34)
- Adds background execution reliability immediately after shell stability.
- The order follows user flow coherence from setup entry -> system battery dialog -> tutorial hub -> OEM-specific tutorials and step-2 recents lock guidance.
- This de-risks later translation/meeting/assistant sessions that depend on long-running background behavior.

3. `tutorial_onboarding` (seq 35-55)
- Implements first-run behavior guides after core + permissions are available.
- Keeps in-group visual continuity using step progression (1..N) for hardware controls and touchpad gesture tutorials.
- Ends with voice assistant wake guide because it bridges onboarding into assistant features.

4. `assistant_core` (seq 56-63)
- Delivers assistant settings, timbre/quality controls, model capability guides, language settings, then AI chat variants.
- This order enables configuration and expectations before user-facing generation/chat outputs.

5. `translation_meeting` (seq 64-76)
- Starts from translation hub, then conversation + simultaneous modes, then meeting minutes/detail, then transcription queue/help, then translation history/edit.
- Dependency logic: mode entry -> active session -> persisted artifacts -> artifact editing.

6. `media_pipeline` (seq 77-84)
- Builds album import lifecycle in execution order: import trigger/filter -> Wi-Fi handoff -> import progress -> timeline/history -> batch edit -> album settings.
- This phase is placed after translation/meeting because media and transcription both depend on stabilized device transfer and background behavior established earlier.

7. `profile_support` (seq 85-90)
- Final polish for profile edit and FAQ/help localization/sections.
- Safe to parallelize late because it has lower coupling with core runtime workflows.

## How AiMemo-style auth should be integrated
AiMemo reference patterns indicate a practical baseline: explicit register/login mode split, JWT bearer session, `auth/me` bootstrap, secure token persistence, and optional OAuth providers.

Recommended insertion point in this order:
- Introduce auth platform primitives at end of `home_shell` and before `assistant_core`.
- Gate all server-backed features in `assistant_core`, `translation_meeting`, and `media_pipeline` behind a shared authenticated session contract.

Concrete integration shape (from AiMemo patterns):
- Backend: `/auth/register`, `/auth/login`, `/auth/me`, token issuance and verification middleware, refresh policy.
- PWA: login/register UI state machine, token storage, startup session bootstrap, unauthorized fallback.
- Android/iOS: secure token storage + startup rehydrate + uniform unauthorized handling.
- OAuth (Google/Apple) should be staged after email/password parity is stable across all clients.

## Risk controls for backend/pwa/android/ios consistency
1. Contract-first API governance
- Freeze endpoint and payload contracts per phase before client work starts.
- Maintain versioned API schema snapshots (OpenAPI or equivalent) and block client merges when contract tests fail.

2. Shared state-machine parity
- Define cross-platform state machines for: device connectivity, background-permission readiness, auth session, translation session, media import.
- Require each platform to map identical state names and terminal/error states.

3. Vertical slice milestones
- For each phase, ship backend + PWA + Android + iOS on the same minimum feature slice before expanding scope.
- Avoid completing whole features on one client while others lag by multiple phases.

4. Permission and lifecycle regression gates
- Add explicit manual regression scripts for Android background kill scenarios and iOS foreground/background transitions.
- Re-run these gates before enabling meeting/transcription and media import features.

5. Feature flags and staged rollout
- Use server-driven flags for high-risk flows (assistant model actions, transcription batch operations, firmware-facing actions).
- Keep kill-switches available until all clients pass parity checks.

6. Deterministic artifact ordering
- This TSV order should be treated as canonical sequencing input for planning tools and sprint slicing.
- Any reorder should require dependency note updates in this rationale to prevent silent drift.
