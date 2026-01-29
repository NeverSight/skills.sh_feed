---
name: rspack-tracing
description: Comprehensive guide and toolkit for diagnosing Rspack build issues. Quickly identify where crashes/errors occur, or perform detailed performance profiling to resolve bottlenecks. Use when the user encounters build failures, slow builds, or wants to optimize Rspack performance.
---

# Rspack Tracing & Performance Profiling

## When to Use This Skill
Use this skill when you need to:
1.  Diagnose why an Rspack build is slow.
2.  Understand which plugins or loaders are taking the most time.
3.  Analyze a user-provided Rspack trace file.
4.  Guide a user to capture a performance profile.

## Workflow

### 1. Capture a Trace
First, ask the user to run their build with tracing enabled.

```bash
# Set environment variables for logging to a file
RSPACK_PROFILE=TRACE RSPACK_TRACE_LAYER=logger RSPACK_TRACE_OUTPUT=./trace.json pnpm build
```

This will generate a trace file in a timestamped directory like `.rspack-profile-{timestamp}-{pid}/trace.json`.

See [references/tracing-guide.md](references/tracing-guide.md) for more details on configuration.

### 2. Quick Diagnosis for Crashes/Errors
If the user wants to identify **which stage a crash or error occurred in**, use `tail` to quickly view the last events without running the full analysis:

```bash
# Navigate to the generated profile directory
cd .rspack-profile-*/

# View the last 20 events to see where the build failed
tail -n 20 trace.json
```

The last events will show the span names and targets where the build stopped, helping to quickly pinpoint the problematic stage, plugin, or loader.

### 3. Full Performance Analysis
For detailed performance profiling (not just crash diagnosis), ask the user to run the bundled analysis script on the generated trace file.

```bash
# Navigate to the generated profile directory
cd .rspack-profile-*/

# Run the analysis script
node ${CLAUDE_PLUGIN_ROOT}/skills/tracing/scripts/analyze_trace.js trace.json
```

### 4. Interpret Results
Use the output from the script to identify bottlenecks.
Consult [references/bottlenecks.md](references/bottlenecks.md) to map span names to actionable fixes.

### 5. Locate Slow Plugins
Based on the "Top Slowest Hooks" from the analysis script:

1.  **Identify the Hook**: Note the hook name (e.g., `hook:CompilationOptimizeChunks`).
2.  **Inspect Configuration**: Read `rspack.config.js` or `rsbuild.config.ts`.
3.  **Map Hook to Plugin**: Look for plugins and their sources that tap into that specific hook.
4. **Output**: Output the paths, lines and columns of the suspected plugin source code.


## Common Scenarios & Quick Fixes
-   [Bottleneck Reference](references/bottlenecks.md): Mapping spans to concepts.
-   [Tracing Guide](references/tracing-guide.md): Detailed usage of `RSPACK_PROFILE`.
