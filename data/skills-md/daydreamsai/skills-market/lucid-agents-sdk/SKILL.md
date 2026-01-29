---
name: lucid-agents-sdk
description: |
  Skill for working with the Lucid Agents SDK - a TypeScript framework for building
  and monetizing AI agents. Use this skill when building or modifying Lucid Agents
  projects, working with agent entrypoints, payments, identity, or A2A communication.

  Activate when: Building or modifying Lucid Agents projects, working with agent
  entrypoints, payments, identity, or A2A communication, developing in the
  lucid-agents monorepo, creating new templates or CLI features, or questions about
  the Lucid Agents architecture or API.

see-also:
  - https://github.com/daydreamsai/lucid-agents/blob/master/AGENTS.md: Full AI coding guide for the lucid-agents monorepo
  - https://github.com/daydreamsai/lucid-agents/blob/master/CONTRIBUTING.md: Contribution guidelines
---

# Lucid Agents SDK Skill

Use this skill when working with the Lucid Agents SDK - a TypeScript framework for building and monetizing AI agents.

## When to Use This Skill

This skill should be activated when:
- Building or modifying Lucid Agents projects
- Working with agent entrypoints, payments, identity, or A2A communication
- Developing in the lucid-agents monorepo
- Creating new templates or CLI features
- Questions about the Lucid Agents architecture or API

## Project Overview

Lucid Agents is a TypeScript/Bun monorepo for building, monetizing, and verifying AI agents. It provides:

- **@lucid-agents/core** - Protocol-agnostic agent runtime with extension system
- **@lucid-agents/http** - HTTP extension for request/response handling
- **@lucid-agents/identity** - ERC-8004 identity and trust layer
- **@lucid-agents/payments** - x402 payment utilities with bi-directional tracking
- **@lucid-agents/analytics** - Payment analytics and reporting
- **@lucid-agents/wallet** - Wallet SDK for agent and developer wallets
- **@lucid-agents/a2a** - A2A Protocol client for agent-to-agent communication
- **@lucid-agents/ap2** - AP2 (Agent Payments Protocol) extension
- **@lucid-agents/hono** - Hono HTTP server adapter
- **@lucid-agents/express** - Express HTTP server adapter
- **@lucid-agents/tanstack** - TanStack Start adapter
- **@lucid-agents/cli** - CLI for scaffolding new agent projects

**Tech Stack:**
- Runtime: Bun (Node.js 20+ compatible)
- Language: TypeScript (ESM, strict mode)
- Build: tsup
- Package Manager: Bun workspaces
- Versioning: Changesets

## Architecture Overview

### Extension System

The framework uses an extension-based architecture where features are added via composable extensions:

```typescript
const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(http())
  .use(wallets({ config: walletsFromEnv() }))
  .use(payments({ config: paymentsFromEnv() }))
  .use(identity({ config: identityFromEnv() }))
  .use(a2a())
  .build();
```

**Available Extensions:**
- **http** - HTTP request/response handling, streaming, SSE
- **wallets** - Wallet management for agents
- **payments** - x402 payment verification and tracking
- **analytics** - Payment analytics and reporting
- **identity** - ERC-8004 on-chain identity and trust
- **a2a** - Agent-to-agent communication protocol
- **ap2** - Agent Payments Protocol extension

### Adapter System

The framework supports multiple runtime adapters:

- **Hono** (`@lucid-agents/hono`) - Lightweight HTTP server, edge-compatible
- **Express** (`@lucid-agents/express`) - Traditional Node.js/Express server
- **TanStack Start** (`@lucid-agents/tanstack`) - Full-stack React with dashboard (UI) or API-only (headless)

Templates are adapter-agnostic and work with any compatible adapter.

### Payment Networks

**EVM Networks:**
- `base` - Base mainnet (L2, low cost)
- `base-sepolia` - Base Sepolia testnet
- `ethereum` - Ethereum mainnet
- `sepolia` - Ethereum Sepolia testnet

**Solana Networks:**
- `solana` - Solana mainnet (high throughput, low fees)
- `solana-devnet` - Solana devnet

**Key Differences:**
- **EVM**: EIP-712 signatures, ERC-20 tokens (USDC), 0x-prefixed addresses
- **Solana**: Ed25519 signatures, SPL tokens (USDC), Base58 addresses
- **Transaction finality**: Solana (~400ms) vs EVM (12s-12min)
- **Gas costs**: Solana (~$0.0001) vs EVM ($0.01-$10)

## Code Structure Principles

### 1. Single Source of Truth
One type definition per concept. Avoid duplicate types. Use type composition or generics, not separate type definitions.

### 2. Encapsulation at the Right Level
Domain complexity belongs in the owning package. The payments package should handle all payments-related complexity.

### 3. Direct Exposure
Expose runtimes directly without unnecessary wrappers. If the type matches what's needed, pass it through.

### 4. Consistency
Similar concepts should follow the same pattern. Consistency reduces cognitive load.

### 5. Public API Clarity
If something needs to be used by consumers, include it in the public type. Don't hide methods or use type casts.

### 6. Simplicity Over Indirection
Avoid unnecessary getters, wrappers, and intermediate objects. Prefer straightforward code.

### 7. Domain Ownership
Each package should own its complexity and return what consumers need.

### 8. No Premature Abstraction
Keep it simple until you actually need the complexity. YAGNI (You Aren't Gonna Need It) applies.

## Monorepo Structure

```
/
├── packages/
│   ├── core/               # Protocol-agnostic runtime
│   ├── http/               # HTTP extension
│   ├── wallet/             # Wallet SDK
│   ├── payments/           # x402 payment utilities
│   ├── analytics/          # Payment analytics
│   ├── identity/           # ERC-8004 identity
│   ├── a2a/                # A2A Protocol client
│   ├── ap2/                # AP2 extension
│   ├── hono/               # Hono adapter
│   ├── express/            # Express adapter
│   ├── tanstack/           # TanStack adapter
│   └── cli/                # CLI scaffolding tool
├── scripts/
└── package.json            # Workspace config
```

## Common Commands

### Workspace-Level
```bash
# Install dependencies
bun install

# Build all packages
bun run build:packages

# Create changeset
bun run changeset

# Version packages
bun run release:version

# Publish packages
bun run release:publish
```

### Package-Level
```bash
cd packages/[package-name]

# Build this package
bun run build

# Run tests
bun test

# Type check
bunx tsc --noEmit
```

## API Quick Reference

### Core Agent Creation

```typescript
import { createAgent } from '@lucid-agents/core';
import { http } from '@lucid-agents/http';
import { z } from 'zod';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
  description: 'My first agent',
})
  .use(http())
  .build();

agent.entrypoints.add({
  key: 'greet',
  input: z.object({ name: z.string() }),
  async handler({ input }) {
    return { output: { message: `Hello, ${input.name}` } };
  },
});
```

### Hono Adapter

```typescript
import { createAgent } from '@lucid-agents/core';
import { http } from '@lucid-agents/http';
import { createAgentApp } from '@lucid-agents/hono';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(http())
  .build();

const { app, addEntrypoint } = await createAgentApp(agent);

addEntrypoint({
  key: 'echo',
  description: 'Echo back input',
  input: z.object({ text: z.string() }),
  handler: async ctx => {
    return { output: { text: ctx.input.text } };
  },
});

export default {
  port: Number(process.env.PORT ?? 3000),
  fetch: app.fetch,
};
```

### Express Adapter

```typescript
import { createAgent } from '@lucid-agents/core';
import { http } from '@lucid-agents/http';
import { createAgentApp } from '@lucid-agents/express';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(http())
  .build();

const { app, addEntrypoint } = await createAgentApp(agent);

// Express apps need to listen on a port
const server = app.listen(process.env.PORT ?? 3000);
```

### TanStack Adapter

```typescript
import { createAgent } from '@lucid-agents/core';
import { http } from '@lucid-agents/http';
import { createTanStackRuntime } from '@lucid-agents/tanstack';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(http())
  .build();

const { runtime: tanStackRuntime, handlers } = await createTanStackRuntime(agent);

// Use runtime.addEntrypoint() instead of addEntrypoint()
tanStackRuntime.addEntrypoint({ ... });

// Export for TanStack routes
export { runtime: tanStackRuntime, handlers };
```

### Payments Extension

```typescript
import { createAgent } from '@lucid-agents/core';
import { payments, paymentsFromEnv } from '@lucid-agents/payments';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(
    payments({
      config: {
        ...paymentsFromEnv(),
        policyGroups: [
          {
            name: 'Daily Limits',
            outgoingLimits: {
              global: { maxTotalUsd: 100.0, windowMs: 86400000 },
            },
            incomingLimits: {
              global: { maxTotalUsd: 5000.0, windowMs: 86400000 },
            },
          },
        ],
      },
      storage: { type: 'sqlite' }, // or 'in-memory' or 'postgres'
    })
  )
  .build();
```

### Analytics Extension

```typescript
import { createAgent } from '@lucid-agents/core';
import { analytics, getSummary, exportToCSV } from '@lucid-agents/analytics';
import { payments, paymentsFromEnv } from '@lucid-agents/payments';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(payments({ config: paymentsFromEnv() }))
  .use(analytics())
  .build();

// Get payment summary
const summary = await getSummary(agent.analytics.paymentTracker, 86400000);

// Export to CSV for accounting
const csv = await exportToCSV(agent.analytics.paymentTracker);
```

### Identity Extension

```typescript
import { createAgent } from '@lucid-agents/core';
import { wallets, walletsFromEnv } from '@lucid-agents/wallet';
import { identity, identityFromEnv } from '@lucid-agents/identity';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(wallets({ config: walletsFromEnv() }))
  .use(identity({ config: identityFromEnv() }))
  .build();

// Identity automatically handles ERC-8004 registration
```

### A2A Extension

```typescript
import { createAgent } from '@lucid-agents/core';
import { http } from '@lucid-agents/http';
import { a2a } from '@lucid-agents/a2a';

const agent = await createAgent({
  name: 'my-agent',
  version: '1.0.0',
})
  .use(http())
  .use(a2a())
  .build();

// Call another agent
const result = await agent.a2a.client.invoke(
  'https://other-agent.com',
  'skillId',
  { input: 'data' }
);
```

### Streaming Entrypoints

```typescript
addEntrypoint({
  key: 'chat',
  description: 'Chat with AI assistant',
  input: z.object({ message: z.string() }),
  streaming: true,
  async stream(ctx, emit) {
    const stream = await ai.chat.stream({ messages: [{ role: 'user', content: ctx.input.message }] });

    for await (const chunk of stream) {
      await emit({
        kind: 'delta',
        delta: chunk.delta,
        mime: 'text/plain',
      });
    }

    return {
      output: { completed: true },
      usage: { total_tokens: stream.usage.total_tokens },
    };
  },
});
```

## CLI Usage

### Interactive Mode
```bash
bunx @lucid-agents/cli my-agent
```

### With Adapter Selection
```bash
# Hono adapter
bunx @lucid-agents/cli my-agent --adapter=hono

# Express adapter
bunx @lucid-agents/cli my-agent --adapter=express

# TanStack UI (full dashboard)
bunx @lucid-agents/cli my-agent --adapter=tanstack-ui

# TanStack Headless (API only)
bunx @lucid-agents/cli my-agent --adapter=tanstack-headless
```

### Non-Interactive Mode
```bash
bunx @lucid-agents/cli my-agent \
  --adapter=hono \
  --template=axllm \
  --non-interactive \
  --AGENT_NAME="My AI Agent" \
  --AGENT_DESCRIPTION="AI-powered assistant" \
  --OPENAI_API_KEY=your_api_key_here \
  --PAYMENTS_RECEIVABLE_ADDRESS=0xYourAddress \
  --NETWORK=base-sepolia \
  --DEFAULT_PRICE=1000
```

## Coding Standards

### General
- **No emojis** - Do not use emojis in code, comments, or commit messages unless explicitly requested
- **Re-exports are banned** - Do not re-export types or values from other packages. Define types in `@lucid-agents/types` or in the package where they are used.

### TypeScript
- **ESM only** - Use `import`/`export`, not `require()`
- **Strict mode** - All packages use `strict: true`
- **Explicit types** - Avoid `any`, prefer explicit types or `unknown`
- **Type exports** - Export types separately: `export type { MyType }`

### File Naming
- Source: `kebab-case.ts`
- Types: `types.ts` or inline
- Tests: `*.test.ts` in `__tests__/`
- Examples: Descriptive names in `examples/`

## Testing Local Packages

Use bun's linking feature for testing local changes:

1. **Register packages globally**:
   ```bash
   cd packages/types
   bun link

   cd ../wallet
   bun link
   ```

2. **Update test project's `package.json`**:
   ```json
   {
     "dependencies": {
       "@lucid-agents/wallet": "link:@lucid-agents/wallet"
     }
   }
   ```

3. **Install and test**:
   ```bash
   cd my-test-agent
   bun install
   ```

4. **Make changes and rebuild**:
   ```bash
   cd lucid-agents/packages/wallet
   # Make changes
   bun run build
   # Changes reflected immediately
   ```

## Common Development Tasks

### Adding a New Feature to a Package

1. Create implementation in `packages/[package]/src/feature.ts`
2. Add types to `types.ts` or inline
3. Export from `index.ts`
4. Add tests in `__tests__/feature.test.ts`
5. Update package `README.md` and `AGENTS.md`
6. Create changeset: `bun run changeset`

### Creating a New Template

1. Create directory: `packages/cli/templates/my-template/`
2. Add required files: `src/agent.ts`, `src/index.ts`, `package.json`, `tsconfig.json`
3. Create `template.json` with wizard configuration
4. Create `template.schema.json` documenting all arguments
5. Create `AGENTS.md` with comprehensive examples
6. Test: `bunx ./packages/cli/dist/index.js test-agent --template=my-template`

## Troubleshooting

### "Module not found" errors
1. Build all packages: `bun run build:packages`
2. Install dependencies: `bun install`
3. Check import paths are correct

### TypeScript errors in templates
1. Build packages first
2. Check template `package.json` references correct versions
3. Run `bunx tsc --noEmit` in template directory

### Build fails
1. Check TypeScript version matches across packages
2. Verify all imports are resolvable
3. Check for circular dependencies
4. Run `bun install` again

## Key Files

- **packages/core/src/core/** - AgentCore, entrypoint management
- **packages/core/src/extensions/** - AgentBuilder, extension system
- **packages/http/src/extension.ts** - HTTP extension definition
- **packages/payments/src/extension.ts** - Payments extension
- **packages/identity/src/extension.ts** - Identity extension
- **packages/hono/src/app.ts** - Hono adapter implementation
- **packages/express/src/app.ts** - Express adapter implementation
- **packages/tanstack/src/runtime.ts** - TanStack adapter implementation
- **packages/cli/src/index.ts** - CLI implementation

## Resources

- [AGENTS.md](../https://github.com/daydreamsai/lucid-agents/blob/master/AGENTS.md) - Full AI coding guide
- [CONTRIBUTING.md](../https://github.com/daydreamsai/lucid-agents/blob/master/CONTRIBUTING.md) - Contribution guidelines
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [x402 Protocol](https://github.com/paywithx402)
- [A2A Protocol](https://a2a-protocol.org/)
