# Platform Profile Reference

## 1. Definition

A Platform Profile is an atomic platform/deployment configuration used to scope process behavior and engineering knowledge. It binds the OS to its known deployment context. It is not an invitation to generate every possible OS × product combination.

## 2. Phase-one profiles

| Profile ID | OS | Deployment context | Notes |
|---|---|---|---|
| qnx | QNX | QNX target; product context must be discovered | Do not assume IVI or TBOX without evidence |
| android | Android | Android target; product context must be discovered | Do not assume IVI or TBOX without evidence |
| linux-tbox | Linux | TBOX | Treat Linux-TBOX as one bound profile |

These are the only approved profile IDs for v0.1.0. A new profile requires an explicit project decision.

## 3. Suggested attributes

Record only known values:
- profile_id;
- operating_system;
- deployment_context;
- OS release/version;
- BSP/vendor/platform;
- architecture/CPU;
- toolchain/compiler;
- init/service manager;
- IPC mechanisms;
- security model;
- filesystem/mount layout;
- suspend/resume model;
- boot/startup configuration;
- package/deployment format;
- source repositories and evidence.

## 4. Process applicability

A process may run on one, two, or all three profiles. Record only confirmed support.

For each process/profile pair, distinguish:
- supported and verified;
- present but not fully analyzed;
- unsupported with evidence;
- unknown.

Do not infer support from a directory name, build option, or old document alone.

## 5. Common versus profile-specific knowledge

Common knowledge is allowed only if the same claim is supported across all applicable profiles.

Use separate profile pages for platform-specific lifecycle, IPC implementation, security/permission configuration, deployment path, startup service configuration, toolchain/build differences, and suspend/resume behavior.

If a shared business responsibility is common but its implementation differs, keep the responsibility in common knowledge and implementation details under each profile.

## 6. Future expansion

If future engineering work adds another deployment configuration, first decide whether it is a genuinely distinct Platform Profile or a variant/configuration of an existing profile.

Do not split profiles solely based on product naming if runtime and deployment semantics are identical. Do not merge profiles when lifecycle, security, IPC, or deployment behavior materially differs.
