# System Wiki Page Template

## Metadata

- System ID:
- Source superproject:
- Source revisions:
- Platform Profiles covered:
- Status:
- Last reviewed:

## 1. System Overview

Describe the system purpose and its major responsibilities. Avoid unsupported product assumptions.

## 2. Process Inventory

List processes with stable process IDs, implementing repositories, and confirmed Platform Profiles.

## 3. System Architecture

Describe process boundaries and high-level relationships. Every edge must have a relationship type and evidence.

## 4. Runtime Dependencies

Record only dependencies that affect runtime behavior. Identify startup, availability, timeout, and failure semantics where evidence exists.

## 5. Inter-process Interfaces

Describe providers, consumers, protocols, data contracts, versioning, and profile-specific variants.

## 6. Startup and Shutdown

Create a profile-specific sequence. Do not combine sequences across profiles unless their equivalence is proven.

## 7. Suspend and Resume

Record which processes participate, ordering, state persistence, wake sources, timeout constraints, and failure behavior for each applicable profile.

## 8. Data Flow

Describe system-level data movement and ownership. Distinguish control plane from data plane where useful.

## 9. Platform Differences

Compare QNX, Android, and Linux-TBOX only where the relevant source repositories have been inspected. Mark uninspected areas Unknown.

## 10. Deployment and Security

Summarize process composition, startup configuration, permissions, and security boundaries per profile.

## 11. Open Questions and Risks

Track evidence gaps, unresolved conflicts, and areas requiring engineering confirmation.

## 12. Evidence Index

Every material architecture statement must link to source evidence at pinned commits.
