---
name: solid-principles
description: Use during implementation when designing modules, functions, and components requiring SOLID principles for maintainable, flexible architecture.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
---

# SOLID Principles

Apply SOLID design principles for maintainable, flexible code architecture.

## The Five Principles

### 1. Single Responsibility Principle (SRP)

### A module should have one, and only one, reason to change

### Elixir Pattern

```elixir
# BAD - Multiple responsibilities
defmodule UserManager do
  def create_user(attrs) do
    # Creates user
    # Sends welcome email
    # Logs to analytics
    # Updates cache
  end
end

# GOOD - Single responsibility
defmodule User do
  def create(attrs), do: Repo.insert(changeset(attrs))
end

defmodule UserNotifier do
  def send_welcome_email(user), do: # email logic
end

defmodule UserAnalytics do
  def track_signup(user), do: # analytics logic
end
```

### TypeScript Pattern

```typescript
// BAD - Multiple responsibilities
class UserComponent {
  render() { /* UI */ }
  fetchData() { /* API */ }
  formatDate() { /* Formatting */ }
  validateInput() { /* Validation */ }
}

// GOOD - Single responsibility
function UserProfile({ user }: Props) {
  return <View>{/* UI only */}</View>;
}

function useUserData(id: string) {
  // Data fetching only
}

function formatUserDate(date: Date): string {
  // Formatting only
}
```

**Ask yourself:** "What is the ONE thing this module does?"

### 2. Open/Closed Principle (OCP)

**Software entities should be open for extension, closed for modification.**

### Elixir Pattern (Behaviours)

```elixir
# Define interface
defmodule PaymentProvider do
  @callback process_payment(amount :: Money.t(), token :: String.t()) ::
    {:ok, transaction :: map()} | {:error, reason :: String.t()}
end

# Implementations extend without modifying
defmodule StripeProvider do
  @behaviour PaymentProvider
  def process_payment(amount, token), do: # Stripe logic
end

defmodule PayPalProvider do
  @behaviour PaymentProvider
  def process_payment(amount, token), do: # PayPal logic
end

# Usage - add new providers without changing this code
def charge(provider_module, amount, token) do
  provider_module.process_payment(amount, token)
end
```

### TypeScript Pattern (Composition)

```typescript
// BAD - Requires modification for new types
function renderItem(item: Item) {
  if (item.type === 'gig') {
    return <TaskCard />;
  } else if (item.type === 'shift') {
    return <WorkPeriodCard />;
  }
  // Have to modify this function for new types
}

// GOOD - Extension through props
interface CardRenderer {
  (item: Item): ReactElement;
}

const renderers: Record<string, CardRenderer> = {
  gig: (item) => <TaskCard gig={item} />,
  shift: (item) => <WorkPeriodCard shift={item} />,
  // Add new types here without modifying renderItem
};

function renderItem(item: Item) {
  const renderer = renderers[item.type];
  return renderer ? renderer(item) : <DefaultCard item={item} />;
}
```

**Ask yourself:** "Can I add new functionality without changing existing code?"

### 3. Liskov Substitution Principle (LSP)

### Subtypes must be substitutable for their base types

### Elixir Pattern (LSP)

```elixir
# BAD - Violates LSP (raises when base type would return)
defmodule PaymentCalculator do
  def calculate_total(items) when length(items) > 0 do
    Enum.sum(items)
  end
  # Missing clause - raises on empty list
end

# GOOD - Honors contract
defmodule PaymentCalculator do
  def calculate_total(items) when is_list(items) do
    Enum.sum(items)  # Returns 0 for empty list
  end
end
```

### TypeScript Pattern (LSP)

```typescript
// BAD - Violates LSP
class Bird {
  fly(): void { /* flies */ }
}

class Penguin extends Bird {
  fly(): void {
    throw new Error('Penguins cannot fly');  // Breaks contract
  }
}

// GOOD - Correct abstraction
interface Bird {
  move(): void;
}

class FlyingBird implements Bird {
  move(): void { this.fly(); }
  private fly(): void { /* flies */ }
}

class SwimmingBird implements Bird {
  move(): void { this.swim(); }
  private swim(): void { /* swims */ }
}
```

**Ask yourself:** "Can I replace this with its parent/interface without
breaking behavior?"

### 4. Interface Segregation Principle (ISP)

**Clients should not be forced to depend on interfaces they don't use.**

### Elixir Pattern (ISP)

```elixir
# BAD - Fat interface
defmodule User do
  @callback work() :: :ok
  @callback take_break() :: :ok
  @callback eat_lunch() :: :ok
  @callback clock_in() :: :ok
  @callback clock_out() :: :ok
  # Not all users need all these
end

# GOOD - Segregated interfaces
defmodule Workable do
  @callback work() :: :ok
end

defmodule Breakable do
  @callback take_break() :: :ok
end

defmodule TimeTrackable do
  @callback clock_in() :: :ok
  @callback clock_out() :: :ok
end

# Implement only what you need
defmodule ContractUser do
  @behaviour Workable
  def work(), do: :ok
  # No time tracking needed
end
```

### TypeScript Pattern (ISP)

```typescript
// BAD - Fat interface
interface User {
  work(): void;
  takeBreak(): void;
  clockIn(): void;
  clockOut(): void;
  receiveBenefits(): void;
  // Not all users need all methods
}

// GOOD - Segregated interfaces
interface Workable {
  work(): void;
}

interface TimeTrackable {
  clockIn(): void;
  clockOut(): void;
}

interface BenefitsEligible {
  receiveBenefits(): void;
}

// Compose only what you need
type FullTimeUser = Workable & TimeTrackable & BenefitsEligible;
type ContractUser = Workable & TimeTrackable;
type TaskUser = Workable;
```

**Ask yourself:** "Does this interface force implementations to define unused methods?"

### 5. Dependency Inversion Principle (DIP)

### Depend on abstractions, not concretions

### Elixir Pattern (DIP)

```elixir
# BAD - Direct dependency on implementation
defmodule UserService do
  def create_user(attrs) do
    PostgresRepo.insert(attrs)  # Tightly coupled
  end
end

# GOOD - Depend on abstraction
defmodule UserService do
  def create_user(attrs, repo \\ YourApp.Repo) do
    repo.insert(attrs)  # Can inject any Repo implementation
  end
end

# Even better - use behaviour
defmodule UserService do
  @callback create_user(attrs :: map()) :: {:ok, User.t()} | {:error, term()}
end

defmodule PostgresUserService do
  @behaviour UserService
  def create_user(attrs), do: Repo.insert(User.changeset(attrs))
end

# Application config determines implementation
config :yourapp, :user_service, PostgresUserService
```

### TypeScript Pattern (DIP)

```typescript
// BAD - Direct dependency
class UserManager {
  private api = new StripeAPI();  // Tightly coupled

  async processPayment(amount: number) {
    return this.api.charge(amount);
  }
}

// GOOD - Depend on abstraction
interface PaymentAPI {
  charge(amount: number): Promise<Transaction>;
}

class UserManager {
  constructor(private paymentAPI: PaymentAPI) {}  // Injected

  async processPayment(amount: number) {
    return this.paymentAPI.charge(amount);
  }
}

// Usage
const stripeAPI: PaymentAPI = new StripeAPI();
const manager = new UserManager(stripeAPI);
```

**Ask yourself:** "Can I swap implementations without changing dependent code?"

## Application Checklist

### Before writing new code

- [ ] Identify the single responsibility
- [ ] Design for extension points (behaviours, interfaces)
- [ ] Define abstractions before implementations
- [ ] Keep interfaces minimal and focused

### During implementation

- [ ] Each module has ONE reason to change (SRP)
- [ ] New features extend, don't modify (OCP)
- [ ] Implementations honor contracts (LSP)
- [ ] Interfaces are minimal (ISP)
- [ ] Dependencies are injected/configurable (DIP)

### During code review

- [ ] Are responsibilities clearly separated?
- [ ] Can we add features without modifying existing code?
- [ ] Do all implementations fulfill their contracts?
- [ ] Are interfaces focused and minimal?
- [ ] Are dependencies abstracted?

## Common Violations in Codebase

### SRP Violation

- GraphQL resolvers that also contain business logic (use command handlers)
- Components that fetch data AND render (use hooks + presentation components)

### OCP Violation

- Long if/else or case statements for types (use behaviours/polymorphism)
- Hardcoded provider logic (use dependency injection)

### LSP Violation

- Raising exceptions in implementations when base would return nil/error tuple
- Changing return types between implementations

### ISP Violation

- Fat GraphQL types requiring all fields (use fragments)
- Monolithic component props (split into focused interfaces)

### DIP Violation

- Direct calls to external services (wrap in behaviours)
- Hardcoded Repo calls (inject repository)

## Integration with Existing Skills

### Works with

- `boy-scout-rule`: Apply SOLID when improving code
- `test-driven-development`: Write tests for each responsibility
- `elixir-code-quality-enforcer`: Credo enforces some SOLID principles
- `typescript-code-quality-enforcer`: TypeScript interfaces support ISP/DIP

## Remember

**SOLID is about managing dependencies and responsibilities, not about
creating more code.**

Good design emerges from applying these principles pragmatically, not
dogmatically.
