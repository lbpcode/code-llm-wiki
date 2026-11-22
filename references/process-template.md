# Process Wiki Page Template

Use this template as a structure, not as a requirement to invent content. Omit sections with no evidence and record material gaps as Unknown. Every material statement must map to a Claim ID and exact Evidence.

## Metadata

- Process ID:
- Display name:
- Lifecycle status: active / candidate / deprecated_candidate / retired_confirmed
- Implementing repositories:
- Supported Platform Profiles and support status:
- Source Manifest version:
- Source revisions:
- Wiki content status:
- Change ID:
- Last reviewed:

## 1. Overview

- Responsibility:
- Functional boundary:
- What this process owns:
- What it explicitly does not own:
- Entry point/executable:
- Repository mapping evidence:
- Claim IDs:

## 2. Architecture

- Major runtime responsibilities:
- Important internal components only where they clarify process behavior:
- Main execution threads/event loops when evidenced:
- Configuration and feature guards:
- Claim IDs and evidence:

## 3. Lifecycle

For each applicable profile:
- process creation/start trigger;
- initialization sequence;
- ready/healthy state;
- normal operation;
- shutdown;
- restart/recovery;
- suspend/resume behavior;
- failure and timeout handling;
- evidence and unknowns.

## 4. Interfaces

For each interface:
- interface ID/name;
- provider and consumer;
- mechanism/protocol;
- message/API/data contract;
- connection/setup sequence;
- error handling and compatibility;
- profile scope;
- evidence on provider and consumer sides;
- Claim IDs.

Use references/interface-template.md for substantial contracts.

## 5. Dependencies

Separate:
- build dependencies;
- runtime dependencies;
- communication relationships;
- startup ordering;
- external services/devices.

For each relationship record from, type, to, profile, evidence, status, and constraints. Never infer runtime dependency from CMake linkage alone.

## 6. Data Flow

- input;
- processing;
- output;
- persistence/cache;
- ownership and lifetime;
- failure behavior;
- evidence.

## 7. Platform Profiles

Create a separate subsection/page for every confirmed or explicitly in-scope profile:
- profile and support status;
- implementation differences;
- OS APIs;
- IPC;
- security;
- deployment;
- lifecycle;
- resource constraints;
- evidence.

Keep uninspected profiles Unknown.

## 8. Security

- process identity;
- privilege/permission model;
- SELinux/secpol rules;
- device/resource access;
- trust boundaries;
- security-sensitive configuration;
- evidence.

Do not copy secret values into the Wiki.

## 9. Deployment

- binary/package;
- installation path;
- configuration path;
- startup/service definition;
- user/group;
- required devices/resources;
- dependencies;
- evidence.

## 10. Constraints and Open Questions

Separate verified constraints, inferred constraints, unresolved questions, source conflicts, and uninspected scope.

## 11. Claim-Evidence Index

Map every material claim to repository, full commit SHA, path, locator, evidence type, and profile.

## 12. Update and Review Metadata

- Page-Source Map entry:
- Affected dependent pages:
- Last accepted change:
- Current review status:
