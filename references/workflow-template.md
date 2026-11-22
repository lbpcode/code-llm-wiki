# Workflow Wiki Page Template

## Metadata

- Workflow ID:
- Display name:
- Workflow type: startup / shutdown / suspend-resume / recovery / update / other
- Process IDs:
- Platform Profile:
- Source revisions:
- Status:

## 1. Trigger and preconditions

- Trigger:
- Required state:
- Preconditions:
- Initiating process/component:

## 2. Normal sequence

| Step | Actor / Process | Action | Expected result | Evidence |
|---|---|---|---|---|

## 3. State and ordering

- Required ordering:
- Synchronization / acknowledgement:
- Timeouts:
- Persistent state:
- Resource ownership:

## 4. Failure and recovery paths

| Failure | Detection | State transition | Recovery / fallback | Evidence |
|---|---|---|---|---|

## 5. Profile-specific behavior

Describe only the selected profile. Compare profiles in a separate section/page and only where both have been inspected.

## 6. Open questions and Claim-Evidence index

List unknown ordering, missing participants, unverified timeouts, assumptions, and the exact evidence required to resolve them.
