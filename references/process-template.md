# Process Wiki Page Template

Use this template as a structure, not as a requirement to invent content. Omit sections with no evidence and record material gaps as Unknown.

## Metadata

- Process ID:
- Display name:
- Implementing repositories:
- Supported Platform Profiles:
- Source revisions:
- Status:
- Last reviewed:

## 1. Overview

- Responsibility:
- Functional boundary:
- What this process owns:
- What it explicitly does not own:
- Entry point/executable:
- Evidence:

## 2. Architecture

- Major runtime responsibilities:
- Important internal components only where they clarify process behavior:
- Main execution threads/event loops when evidenced:
- Configuration and feature guards:
- Evidence:

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
- evidence.

## 4. Interfaces

For each interface:
- interface ID/name;
- provider and consumer;
- mechanism/protocol;
- message/API/data contract;
- connection/setup sequence;
- error handling and compatibility;
- profile scope;
- evidence.

## 5. Dependencies

Separate:
- build dependencies;
- runtime dependencies;
- communication relationships;
- startup ordering;
- external services/devices.

Never infer runtime dependency from CMake linkage alone.

## 6. Data Flow

- input;
- processing;
- output;
- persistence/cache;
- ownership and lifetime;
- failure behavior;
- evidence.

## 7. Platform Profiles

Create a separate subsection/page for every confirmed profile:
- profile;
- implementation differences;
- OS APIs;
- IPC;
- security;
- deployment;
- lifecycle;
- resource constraints;
- evidence.

## 8. Security

- process identity;
- privilege/permission model;
- SELinux/secpol rules;
- device/resource access;
- trust boundaries;
- security-sensitive configuration;
- evidence.

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

Separate verified constraints, inferred constraints, and unresolved questions.

## 11. Evidence Index

Map each important claim to repository, full commit SHA, path, locator, and profile.
