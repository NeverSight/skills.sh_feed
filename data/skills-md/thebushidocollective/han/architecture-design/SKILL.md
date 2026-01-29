---
name: architecture-design
description: Use when designing system architecture, making high-level technical decisions, or planning major system changes. Focuses on structure, patterns, and long-term strategy.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Architecture Design Skill

Design system architecture and make strategic technical decisions.

## Core Principle

**Good architecture enables change while maintaining simplicity.**

## Architecture vs Planning

**Architecture Design (this skill):**

- Strategic: "How should the system be structured?"
- Component interactions and boundaries
- Technology and pattern choices
- Long-term implications
- System-level decisions

**Technical Planning (technical-planning skill):**

- Tactical: "How do I implement feature X?"
- Specific implementation tasks
- Execution details
- Short-term focus

**Use architecture when:**

- Designing new systems or subsystems
- Major refactors affecting multiple components
- Technology selection decisions
- Defining system boundaries and interfaces
- Making decisions with long-term impact

**Use planning when:**

- Implementing within existing architecture
- Breaking down specific features
- Task sequencing and execution

## Architecture Process

### 1. Understand Context

**Business context:**

- What problem are we solving?
- Who are the users?
- What are the business goals?
- What are the success metrics?

**Technical context:**

- What exists today?
- What constraints exist?
- What must we integrate with?
- What scale must we support?

**Team context:**

- What's our expertise?
- What can we maintain?
- What's our velocity?

### 2. Gather Requirements

**Functional requirements:**

- What must the system do?
- What are the features?
- What are the user scenarios?

**Non-functional requirements:**

- **Performance**: Response time, throughput
- **Scalability**: Expected load, growth
- **Availability**: Uptime requirements
- **Security**: Compliance, data protection
- **Maintainability**: Team size, skills
- **Cost**: Budget constraints

**Example:**

```markdown
## Requirements

### Functional
- Users can search products by name/category
- Users can add items to cart
- Users can checkout and pay

### Non-Functional
- Search response time < 200ms (p95)
- Support 10,000 concurrent users
- 99.9% uptime
- PCI DSS compliant for payments
- Team of 5 developers can maintain
```

### 3. Identify Constraints

**Technical constraints:**

- Must use existing authentication system
- Must integrate with legacy inventory system
- Database must be PostgreSQL (existing infrastructure)

**Business constraints:**

- Must launch in 3 months
- Budget of $50k for infrastructure
- Must support EU data residency

**Team constraints:**

- Team experienced in Python, less in Go
- No DevOps specialist on team
- Remote team across timezones

### 4. Consider Alternatives

**Never design in a vacuum - consider options:**

**Example: Data storage choice**

**Option 1: PostgreSQL**

- Pros: Team knows it, ACID guarantees, rich query support
- Cons: Vertical scaling limits, setup complexity

**Option 2: MongoDB**

- Pros: Flexible schema, horizontal scaling
- Cons: Team unfamiliar, eventual consistency

**Option 3: DynamoDB**

- Pros: Fully managed, auto-scaling
- Cons: Vendor lock-in, query limitations, cost at scale

**Decision: PostgreSQL**

- Team expertise outweighs scaling concerns
- Can re-evaluate if scale becomes issue
- Faster initial development

### 5. Design System Structure

**Define components and their responsibilities:**

```
┌─────────────────────────────────────────────┐
│             Client Apps                      │
│  (Web, iOS, Android)                         │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│          API Gateway / Load Balancer         │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────┐  ┌───────────────┐
│   Auth        │  │   Core API     │
│   Service     │  │   Service      │
└───────┬───────┘  └───────┬───────┘
        │                  │
        │         ┌────────┴────────┐
        │         ▼                 ▼
        │  ┌──────────────┐  ┌──────────────┐
        │  │  PostgreSQL  │  │   Redis      │
        │  │  (Primary)   │  │   (Cache)    │
        │  └──────────────┘  └──────────────┘
        │
        ▼
┌───────────────┐
│   User DB     │
└───────────────┘
```

**Component descriptions:**

```markdown
## Components

### API Gateway
**Responsibility:** Route requests, rate limiting, authentication
**Technology:** Nginx
**Dependencies:** Auth Service, Core API Service
**Scale:** 2-3 instances behind load balancer

### Auth Service
**Responsibility:** User authentication, session management, JWT issuing
**Technology:** Python (Flask), PostgreSQL
**API:** REST
**Scale:** Stateless, 2-N instances

### Core API Service
**Responsibility:** Business logic, data access, external integrations
**Technology:** Python (FastAPI), PostgreSQL, Redis
**API:** REST
**Scale:** Stateless, 2-N instances

### PostgreSQL
**Responsibility:** Primary data store
**Scale:** Primary with read replica

### Redis
**Responsibility:** Session storage, caching, rate limiting
**Scale:** Cluster mode (3 nodes)
```

### 6. Define Interfaces

**API contracts:**

```markdown
## API Design

### POST /api/auth/login
**Purpose:** Authenticate user, issue JWT

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**

```json
{
  "token": "eyJ...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Errors:**

- 400: Invalid request
- 401: Invalid credentials
- 429: Rate limit exceeded

```

### 7. Plan for Failure

**What can go wrong?**
- Database unavailable
- External API down
- Network partition
- High load
- Data corruption

**Mitigation strategies:**
- Retry with exponential backoff
- Circuit breakers for external services
- Graceful degradation
- Health checks and monitoring
- Database backups

**Example:**
```markdown
## Failure Scenarios

### Database Unavailable
**Impact:** Cannot read/write data
**Mitigation:**
- Read replica failover (automated)
- Circuit breaker after 3 failures
- Cache serves stale data for 5 minutes
- User sees degraded experience message
**Recovery:** Manual failover to replica, fix primary

### External Payment API Down
**Impact:** Cannot process payments
**Mitigation:**
- Retry 3 times with exponential backoff
- Queue payments for later processing
- User notified of delay
- Alert on-call engineer
**Recovery:** Process queued payments once API recovers
```

### 8. Document Decisions

**Architecture Decision Record (ADR):**

```markdown
# ADR-001: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2024-01-15
**Deciders:** Tech Lead, Backend Team

## Context

We need to choose a primary database for user data, products, and orders.

Requirements:
- Strong consistency (ACID)
- Complex queries (joins, aggregations)
- < 200ms query time for 90% of queries
- Support 100k users initially

## Decision

Use PostgreSQL as primary database.

## Alternatives Considered

### MongoDB
- **Pros:** Flexible schema, horizontal scaling
- **Cons:** Team unfamiliar, eventual consistency issues
- **Why not:** Team expertise more valuable than flexibility

### DynamoDB
- **Pros:** Managed service, auto-scaling
- **Cons:** Vendor lock-in, limited query capability, cost
- **Why not:** Query limitations would hurt development velocity

### MySQL
- **Pros:** Similar to PostgreSQL, team knows it
- **Cons:** Less feature-rich than PostgreSQL
- **Why not:** PostgreSQL offers JSON support, better full-text search

## Consequences

**Positive:**
- Team can be productive immediately
- Strong consistency guarantees
- Rich query capabilities
- JSON support for flexible data

**Negative:**
- Vertical scaling limits (mitigated: can add read replicas)
- More complex than managed services (mitigated: use RDS)
- Higher operational overhead

**Trade-offs:**
- Chose familiarity over horizontal scaling
- Chose rich queries over eventual consistency
- Can re-evaluate if scale requirements change

## Validation

- Team confirmed expertise in PostgreSQL
- Load testing shows meets performance requirements
- Cost analysis shows acceptable for first year
```

## Architecture Principles

### 1. Simplicity

**Start simple, add complexity only when needed.**

```
❌ BAD: Microservices from day 1 with 20 services
✅ GOOD: Start with monolith, split when needed
```

**Apply YAGNI:** You Aren't Gonna Need It

- Don't build for hypothetical future
- Add when actually needed
- Simpler is easier to maintain

### 2. Separation of Concerns

**Each component has one clear responsibility.**

```
✅ GOOD:
- Auth Service: Authentication only
- User Service: User profile management
- Order Service: Order processing

❌ BAD:
- God Service: Does everything
```

**Apply SOLID principles:**

- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

### 3. Loose Coupling

**Components depend on interfaces, not implementations.**

```typescript
// ❌ BAD: Tight coupling
class OrderService {
  constructor(private db: PostgresDatabase) {}
}

// ✅ GOOD: Loose coupling
class OrderService {
  constructor(private db: Database) {}  // Interface
}
```

**Benefits:**

- Easier to test (mock interface)
- Easier to swap implementations
- Components can evolve independently

### 4. High Cohesion

**Related functionality stays together.**

```
✅ GOOD:
user/
  - create_user.ts
  - update_user.ts
  - delete_user.ts
  - user_repository.ts

❌ BAD:
create/
  - create_user.ts
  - create_order.ts
update/
  - update_user.ts
  - update_order.ts
```

### 5. Explicit Over Implicit

**Make dependencies and contracts clear.**

```typescript
// ❌ BAD: Implicit dependency
function processOrder(orderId: string) {
  const db = global.database  // Where does this come from?
  // ...
}

// ✅ GOOD: Explicit dependency
function processOrder(
  orderId: string,
  db: Database,
  logger: Logger
) {
  // Dependencies are clear
}
```

### 6. Fail Fast

**Detect and report errors early.**

```typescript
// ❌ BAD: Silent failure
function divide(a: number, b: number) {
  if (b === 0) return 0  // Wrong!
  return a / b
}

// ✅ GOOD: Fail fast
function divide(a: number, b: number) {
  if (b === 0) {
    throw new Error('Division by zero')
  }
  return a / b
}
```

### 7. Design for Testability

**Make it easy to test.**

```typescript
// ❌ BAD: Hard to test
class OrderService {
  processOrder(orderId: string) {
    const db = new PostgresDatabase()  // Can't mock
    const api = new PaymentAPI()       // Can't mock
    // ...
  }
}

// ✅ GOOD: Easy to test
class OrderService {
  constructor(
    private db: Database,      // Can inject mock
    private api: PaymentAPI    // Can inject mock
  ) {}

  processOrder(orderId: string) {
    // ...
  }
}
```

## Common Architecture Patterns

### Layered Architecture

```
┌─────────────────────┐
│  Presentation       │ (UI, API controllers)
├─────────────────────┤
│  Business Logic     │ (Domain, services)
├─────────────────────┤
│  Data Access        │ (Repositories, ORMs)
├─────────────────────┤
│  Database           │ (Storage)
└─────────────────────┘
```

**When to use:** Simple to moderate complexity

### Hexagonal Architecture (Ports & Adapters)

```
        ┌───────────────────────┐
        │   External Systems    │
        │  (UI, DB, APIs)       │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │      Adapters         │ (Implementation)
        │  (REST, PostgreSQL)   │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │       Ports           │ (Interfaces)
        │  (IUserRepo, IAuth)   │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │    Core Domain        │ (Business logic)
        │    (Pure logic)       │
        └───────────────────────┘
```

**When to use:** Want to isolate business logic, multiple frontends

### Microservices

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│  User   │  │  Order  │  │ Payment │
│ Service │  │ Service │  │ Service │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
          ┌───────▼────────┐
          │  Message Bus   │
          │  (Event-driven)│
          └────────────────┘
```

**When to use:** Large team, need independent deploy, clear boundaries

**Avoid when:** Small team, unclear boundaries, early stage

### Event-Driven Architecture

```
┌─────────┐       ┌─────────────┐       ┌─────────┐
│Producer │──────▶│ Event Bus   │──────▶│Consumer │
└─────────┘       └─────────────┘       └─────────┘
```

**When to use:** Async processing, decoupled systems, audit trails

## Anti-Patterns

### ❌ Premature Optimization

**Don't optimize for scale you don't have.**

```
BAD: Build microservices for 100 users
GOOD: Start with monolith, split when needed
```

### ❌ Resume-Driven Architecture

**Don't choose technology to pad resume.**

```
BAD: "I want to learn Kubernetes, let's use it"
GOOD: "Kubernetes fits our scale needs"
```

### ❌ Distributed Monolith

**Microservices that are tightly coupled.**

```
BAD: Service A can't deploy without Service B
GOOD: Services are independently deployable
```

### ❌ Big Ball of Mud

**No structure, everything depends on everything.**

```
BAD: Any code can call any other code
GOOD: Clear layers and boundaries
```

### ❌ Analysis Paralysis

**Over-analyzing, never shipping.**

```
BAD: Spend 6 months on perfect architecture
GOOD: Design enough to start, iterate
```

## Architecture Review Checklist

- [ ] Business goals clearly understood
- [ ] Functional requirements documented
- [ ] Non-functional requirements defined
- [ ] Constraints identified
- [ ] Multiple alternatives considered
- [ ] Trade-offs explicitly stated
- [ ] Component responsibilities clear
- [ ] Interfaces well-defined
- [ ] Failure scenarios planned for
- [ ] Security considered
- [ ] Scalability addressed
- [ ] Testability designed in
- [ ] Decisions documented (ADRs)
- [ ] Team can implement and maintain

## Integration with Other Skills

- Apply **solid-principles** - Guide component design
- Apply **simplicity-principles** - KISS, YAGNI
- Apply **orthogonality-principle** - Independent components
- Apply **structural-design-principles** - Composition patterns
- Use **technical-planning** - For implementation after design

## Remember

1. **Simplicity first** - Start simple, add complexity when needed
2. **Document decisions** - Future you will thank you
3. **Consider alternatives** - Never the first idea only
4. **State trade-offs** - Every decision has consequences
5. **Design for change** - Systems evolve

**The best architecture is the one that's simple enough to ship and flexible enough to evolve.**
