---
name: rspack-debugging
description: Helps Rspack users and developers debug crashes or deadlocks/hangs in the Rspack build process using LLDB. Use this Skill when users encounter "Segmentation fault" errors during Rspack builds or when the build progress gets stuck.
---

# Rspack Debugging

## Overview

This Skill guides you on how to capture the underlying crash state of Rspack (which is based on Rust). By using the LLDB debugger and Rspack packages with debug symbols, we can obtain detailed stack backtraces, which are crucial for pinpointing issues. The guides focus on non-interactive, automated debugging to easily capture backtraces.

## Preparation

Before starting, please ensure your environment meets the requirements.

1.  **Install LLDB**: You must install the LLDB debugger.
    *   macOS: Run `xcode-select --install`
    *   Linux: Install the `lldb` package (e.g., `apt-get install lldb`)
    *   Detailed guide: [references/lldb.md](references/lldb.md)

2.  **Replace Debug Packages**:
    Production packages like `@rspack/core` have debug symbols stripped. They must be replaced with the `@rspack-debug/*` series packages to see useful stack information.

    **Automatic Replacement Script**:
    ```bash
    node ${CLAUDE_PLUGIN_ROOT}/skills/debugging/scripts/setup_debug_deps.cjs
    ```
    Running the above script will automatically add `pnpm.overrides` configuration to `package.json`, pointing Rspack packages to their corresponding Debug versions. Afterwards, please be sure to run `pnpm install` to update dependencies.

## Debugging Workflows

Identify your specific scenario and follow the corresponding linked guide.

## Detailed Guides

## Detailed Guides

### Guide A: Crash during HMR
**Scenario**: Stable Crash/Deadlock during DevServer HMR.
[Read Guide: references/guide_a_hmr_crash.md](references/guide_a_hmr_crash.md)

### Guide B: Crash during Build
**Scenario**: Stable Crash/Deadlock during Build (or Unstable Build Crash that is frequent enough).
[Read Guide: references/guide_b_build_crash.md](references/guide_b_build_crash.md)

### Guide C: Attach to Stuck Process
**Scenario**: Unstable Deadlock during Build (happens randomly).
[Read Guide: references/guide_c_attach_to_stuck_process.md](references/guide_c_attach_to_stuck_process.md)

### Guide D: Coredump Analysis (Dev)
**Scenario**: Unstable Crash during DevServer HMR (hard to catch interactively).
[Read Guide: references/guide_d_coredump_analysis_dev.md](references/guide_d_coredump_analysis_dev.md)

### Guide E: Coredump Analysis (Build)
**Scenario**: Unstable Crash during Build.
[Read Guide: references/guide_e_coredump_analysis_build.md](references/guide_e_coredump_analysis_build.md)

### Guide F: Async Deadlock Identification
**Scenario**: Unstable Async Deadlock. Main thread stuck in `uv_run`.
[Read Guide: references/guide_f_async_deadlock.md](references/guide_f_async_deadlock.md)

## Saving Debug Artifacts

**Critical Instruction for Agents**:
When you successfully obtain a backtrace or a tracing log, you **MUST** save it to a local file in the user's project directory so it is preserved after the session.

1.  **Create Directory**: Ensure a directory named `debug_artifacts` exists in the project root.
2.  **Save Backtraces**: Write the full output of `thread backtrace all` to `debug_artifacts/backtrace_<timestamp>.txt`.
3.  **Save Tracing Logs**: (Only if using Tracing Skill)

## Environment Restoration

After debugging is complete, restore your `package.json` to use production packages:

```bash
node ${CLAUDE_PLUGIN_ROOT}/skills/debugging/scripts/setup_debug_deps.cjs --restore
pnpm install
```