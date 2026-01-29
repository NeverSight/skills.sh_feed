---
name: structural-design-principles
description: Use when designing modules and components requiring Composition Over Inheritance, Law of Demeter, Tell Don't Ask, and Encapsulation principles that transcend programming paradigms.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
---

# Structural Design Principles

These principles originated in object-oriented design but apply to **any
programming paradigm**
. They're about code structure, not paradigm.

## Paradigm Translations

In **functional programming** (Elixir), they manifest as:

- **Composition Over Inheritance** → Function composition, module
  composition, pipe operators
- **Law of Demeter** → Minimize coupling between data structures,
  delegate to owning modules
- **Tell, Don't Ask** → Push logic to the module owning the data type
- **Encapsulation** → Module boundaries, immutability, pattern matching,
  opaque types

In **object-oriented programming** (TypeScript/React): Apply traditional OO
interpretations with classes, interfaces, and encapsulation.

**The underlying principle is the same across paradigms: manage dependencies,
reduce coupling, and maintain clear boundaries.**

---

## Four Core Principles

### 1. Composition Over Inheritance

**Favor composition (combining simple behaviors) over inheritance
(extending base classes).**

**Why:** Inheritance creates tight coupling and fragile hierarchies.
Composition provides flexibility.

### Elixir Approach (No Inheritance)

Elixir doesn't have inheritance - it uses composition naturally through:

- Module imports (`use`, `import`, `alias`)
- Function composition (`|>` pipe operator)
- Struct embedding
- Behaviour protocols

```elixir
# GOOD - Composition with pipes
def process_payment(order) do
  order
  |> validate_items()
  |> calculate_total()
  |> apply_discounts()
  |> charge_payment()
  |> send_receipt()
end

# GOOD - Compose behaviors
defmodule User do
  use YourApp.Model
  use Ecto.Schema
  import Ecto.Changeset

  # Composes functionality from multiple modules
end

# GOOD - Struct embedding
defmodule Address do
  embedded_schema do
    field :street, :string
    field :city, :string
  end
end

defmodule User do
  schema "users" do
    embeds_one :address, Address
  end
end
```

### TypeScript Examples

```typescript
// BAD - Inheritance hierarchy
class Animal {
  move() { }
}

class FlyingAnimal extends Animal {
  fly() { }
}

class SwimmingAnimal extends Animal {
  swim() { }
}

class Duck extends FlyingAnimal {
  // Problem: Can't also inherit from SwimmingAnimal
  // Forced to duplicate swim() logic
}

// GOOD - Composition with interfaces
interface Movable {
  move(): void;
}

interface Flyable {
  fly(): void;
}

interface Swimmable {
  swim(): void;
}

class Duck implements Movable, Flyable, Swimmable {
  move() { this.walk(); }
  fly() { /* flying logic */ }
  swim() { /* swimming logic */ }
  private walk() { /* walking logic */ }
}
```

```typescript
// GOOD - React composition (pattern)
// Instead of class inheritance, compose components

// Base behaviors as hooks
function useTaskData(gigId: string) {
  // Data fetching logic
}

function useTaskActions(gig: Task) {
  // Action handlers
}

function useTaskValidation(gig: Task) {
  // Validation logic
}

// Compose in component
function TaskDetails({ gigId }: Props) {
  const gig = useTaskData(gigId);
  const actions = useTaskActions(gig);
  const validation = useTaskValidation(gig);

  // Combines all behaviors through composition
  return <View>{/* render */}</View>;
}
```

### Composition Guidelines

- Elixir: Use pipes, protocols, and behaviors instead of inheritance trees
- TypeScript: Use interfaces, hooks, and function composition instead of class hierarchies
- Build complex behavior from simple, reusable parts
- Favor "has-a" over "is-a" relationships
- Keep hierarchies shallow (max 2-3 levels if unavoidable)

### 2. Law of Demeter (Principle of Least Knowledge)

**A module should only talk to its immediate friends, not strangers.**

**The Rule:** Only call methods on:

1. The object itself
2. Objects passed as parameters
3. Objects it creates
4. Its direct properties/fields

### DON'T chain through multiple objects (train wrecks)

### Why (Elixir Context)

- **Reduces coupling**: When you reach through multiple data structures
  (`engagement.worker.address.city`), you're coupled to the entire chain.
  If any intermediate structure changes, your code breaks.
- **Improves testability**: Code that only calls functions on its
  immediate collaborators is easier to test - you don't need to construct
  deep object graphs.
- **Enables refactoring**: You can change internal structure without
  breaking callers if they only interact with top-level functions.
- **Follows functional boundaries**: In Elixir, each module should be
  responsible for its own data type. The Law of Demeter enforces this by
  pushing you to delegate to the owning module.

### Elixir Examples

```elixir
# BAD - Violates Law of Demeter (train wreck)
def get_worker_city(engagement) do
  engagement.worker.address.city
  # Knows too much about internal structure
end

# What if worker doesn't have address?
# What if address structure changes?
# Tightly coupled to implementation

# GOOD - Delegate to the module that owns the data type
defmodule Assignment do
  def worker_city(%{worker: worker}) do
    User.city(worker)
  end
end

defmodule User do
  def city(%{address: address}) do
    Address.city(address)
  end

  def city(_), do: nil
end

# Now can call: Assignment.worker_city(engagement)
# Each module is responsible for its own data
# Coupling minimized to immediate collaborators
```

```elixir
# BAD - Reaching through associations
def total_gig_hours(user_id) do
  user = Repo.get!(User, user_id)
  assignments = user.assignments
  Enum.reduce(assignments, 0, fn eng, acc ->
    acc + eng.shift.hours  # Reaching through
  end)
end

# GOOD - Delegate to the domain
def total_gig_hours(user_id) do
  user = Repo.get!(User, user_id)
  User.total_hours(user)
end

defmodule User do
  def total_hours(%{assignments: assignments}) do
    Enum.reduce(assignments, 0, fn eng, acc ->
      acc + Assignment.hours(eng)
    end)
  end
end

defmodule Assignment do
  def hours(%{shift: shift}), do: WorkPeriod.hours(shift)
end
```

### TypeScript Examples: Law of Demeter

```typescript
// BAD - Chain of doom
function displayUserLocation(engagement: Assignment) {
  const location = engagement.worker.profile.address.city;
  // Knows about 4 levels of object structure!
  return `Location: ${location}`;
}

// GOOD - Each object provides what you need
function displayUserLocation(engagement: Assignment) {
  const location = engagement.getUserCity();
  return `Location: ${location}`;
}

class Assignment {
  getUserCity(): string {
    return this.worker.getCity();
  }
}

class User {
  getCity(): string {
    return this.address.city;
  }
}
```

```typescript
// BAD - GraphQL fragments violating Law of Demeter
const fragment = graphql`
  fragment TaskCard_gig on Task {
    id
    requester {
      organization {
        billing {
          paymentMethod {
            last4
          }
        }
      }
    }
  }
`;
// TaskCard shouldn't know about payment details!

// GOOD - Only query what you need
const fragment = graphql`
  fragment TaskCard_gig on Task {
    id
    title
    payRate
    location {
      city
      state
    }
  }
`;
// TaskCard only knows about gig display data
```

### Law of Demeter Guidelines

- One dot (method call) is okay: `object.method()`
- Multiple dots is a code smell: `object.property.property.method()`
- Create wrapper methods instead of chaining
- Each module should only know about its direct collaborators
- Particularly important in GraphQL - don't query deep nested data you don't need

**Exception:** Fluent interfaces designed for chaining

In Elixir, the pipe operator and certain builder patterns (like Ecto) are
designed for chaining:

```elixir
# This is okay - designed for chaining
User.changeset(%{})
|> cast(attrs, [:email])
|> validate_required([:email])
|> unique_constraint(:email)

# This is okay - Ecto.Query builder pattern
from(u in User)
|> where([u], u.active == true)
|> join(:inner, [u], p in assoc(u, :profile))
|> select([u, p], {u, p})

# These patterns are explicitly designed for method chaining
# Each function returns a chainable structure
```

The key difference: fluent interfaces are **designed** for chaining as their
primary API, whereas reaching through data structures (`.worker.address.city`)
is **accidental** coupling.

### 3. Tell, Don't Ask

**Tell objects what to do, don't ask for their data and do it yourself.**

### Why (Functional Context)

In Elixir, "Tell, Don't Ask" means **delegating to the module that owns the data
type**
.
Instead of pulling data out of a structure and making decisions based on it, you
pass the structure to the owning module and let it handle the logic.

This principle:

- **Encapsulates business rules** with the data they operate on
- **Reduces coupling** - callers don't need to know internal state or
structure
- **Improves cohesion** - related logic lives together in the owning
module
- **Enables polymorphism** - different implementations can handle the
same "tell" differently

Think of it as: "Don't ask a struct for its fields and decide what to
do - tell the module to do it."

### Elixir Examples: Tell Don't Ask

```elixir
# BAD - Asking for data and making decisions
def process_engagement(engagement) do
  if engagement.status == "pending" and engagement.worker_id != nil do
    attrs = %{status: "confirmed", confirmed_at: DateTime.utc_now()}
    Repo.update(Assignment.changeset(engagement, attrs))
  end
end
# We're asking about the engagement's state and deciding what to do

# GOOD - Delegate to the module that owns the Assignment struct
def process_engagement(engagement) do
  Assignment.confirm(engagement)
end

defmodule Assignment do
  def confirm(%{status: "pending", worker_id: worker_id} = engagement)
      when not is_nil(worker_id) do
    changeset = change(engagement, %{
      status: "confirmed",
      confirmed_at: DateTime.utc_now()
    })
    Repo.update(changeset)
  end

  def confirm(engagement), do: {:error, :invalid_state}
  # Assignment module knows its own business rules
  # Callers just "tell" it to confirm, don't "ask" about status
end
```

```elixir
# BAD - Asking and deciding
def charge_gig(gig) do
  if gig.payment_type == "per_hour" do
    rate = gig.hourly_rate
    hours = gig.total_hours
    Money.multiply(rate, hours)
  else
    gig.fixed_amount
  end
end

# GOOD - Delegate to the module that owns the Task struct
def charge_gig(gig) do
  Task.total_charge(gig)
end

defmodule Task do
  def total_charge(%{payment_type: "per_hour", hourly_rate: rate,
total_hours: hours}) do
    Money.multiply(rate, hours)
  end

  def total_charge(%{payment_type: "fixed", fixed_amount: amount}) do
    amount
  end
  # Business logic lives with the data in the owning module
end
```

### TypeScript Examples: Tell Don't Ask

```typescript
// BAD - Asking for data
function renderTaskStatus(gig: Task) {
  let statusText: string;
  let statusColor: string;

  if (gig.status === 'active' && gig.workerCount > 0) {
    statusText = 'In Progress';
    statusColor = 'green';
  } else if (gig.status === 'active') {
    statusText = 'Waiting for Users';
    statusColor = 'yellow';
  } else {
    statusText = 'Completed';
    statusColor = 'gray';
  }

  return <Badge text={statusText} color={statusColor} />;
}

// GOOD - Tell the gig to provide display info
function renderTaskStatus(gig: Task) {
  const { text, color } = gig.getStatusDisplay();
  return <Badge text={text} color={color} />;
}

class Task {
  getStatusDisplay(): { text: string; color: string } {
    if (this.status === 'active' && this.workerCount > 0) {
      return { text: 'In Progress', color: 'green' };
    } else if (this.status === 'active') {
      return { text: 'Waiting for Users', color: 'yellow' };
    }
    return { text: 'Completed', color: 'gray' };
  }
}
```

### Tell, Don't Ask Guidelines

- Push behavior into the module that owns the data type (Elixir) or object (TypeScript)
- Commands over queries (when possible)
- Modules/objects should protect their own invariants
- Reduces coupling - callers don't need to know internal state
- Particularly important in Command handlers - they tell, don't ask

### Pattern

Command handlers follow "Tell, Don't Ask":

```elixir
# Command tells the system what to do
%CreateTask{requester_id: id, title: "Landscaping"}
|> CreateTaskHandler.handle()
# Handler tells domain objects to execute
# Not: Handler asks domain for data and decides
```

### 4. Encapsulation

**Hide internal implementation details. Expose minimal, stable interfaces.**

### Why: Encapsulation (Elixir Context)

- **Enables change**: You can change internal implementation without
breaking callers
- **Enforces invariants**: Internal state can only change through
controlled functions
- **Improves testability**: Test the public interface, not
implementation details
- **Reduces cognitive load**: Callers only need to understand the
public API
- **Supports modularity**: Clear boundaries between modules

In Elixir, encapsulation is achieved through:

- Module boundaries (private functions with `defp`)
- Opaque types (`@opaque`)
- Pattern matching guards
- Changesets for validation at boundaries
- Minimizing public API surface

### Elixir Examples: Encapsulation

```elixir
# BAD - Exposing internals
defmodule PaymentProcessor do
  defstruct [:stripe_client, :api_key, :retry_count]

  def process(processor, amount) do
    # Callers can access processor.stripe_client directly
    # Breaks if we change internal implementation
  end
end

# GOOD - Encapsulate internals
defmodule PaymentProcessor do
  @type t :: %__MODULE__{
    stripe_client: term(),
    api_key: String.t(),
    retry_count: integer()
  }

  @enforce_keys [:stripe_client, :api_key]
  defstruct [:stripe_client, :api_key, retry_count: 3]

  # Public API
  def new(api_key), do: %__MODULE__{
    stripe_client: Stripe.Client.new(api_key),
    api_key: api_key
  }

  def process(%__MODULE__{} = processor, amount) do
    # Internal implementation hidden
    do_process(processor, amount)
  end

  # Private implementation
  defp do_process(processor, amount) do
    # Can change internals without affecting callers
  end
end
```

```elixir
# BAD - Ecto schema with map fields (no structure)
defmodule Task do
  schema "tasks" do
    field :data, :map  # Anything goes!
  end
end

# GOOD - Explicit fields (encapsulation via type system)
defmodule Task do
  schema "tasks" do
    field :title, :string
    field :description, :string
    field :pay_rate, Money.Ecto.Composite.Type
    field :status, Ecto.Enum, values: [:draft, :published, :active, :completed]
  end

  # Changesets enforce valid transitions
  def publish_changeset(gig) do
    gig
    |> change(%{status: :published})
    |> validate_required([:title, :description, :pay_rate])
  end
  # Can't publish without required fields (encapsulated business rule)
end
```

### TypeScript Examples: Encapsulation

```typescript
// BAD - Public mutable state
class ShoppingCart {
  public items: Item[] = [];  // Anyone can modify directly!

  public total(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}

const cart = new ShoppingCart();
cart.items.push(invalidItem);  // Bypasses validation!

// GOOD - Encapsulated state
class ShoppingCart {
  private items: Item[] = [];  // Hidden implementation

  public addItem(item: Item): void {
    if (this.isValid(item)) {
      this.items.push(item);
    } else {
      throw new Error('Invalid item');
    }
  }

  public removeItem(itemId: string): void {
    this.items = this.items.filter(item => item.id !== itemId);
  }

  public getTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  public getItemCount(): number {
    return this.items.length;
  }

  private isValid(item: Item): boolean {
    return item.price > 0 && item.quantity > 0;
  }
  // All state changes go through controlled methods
}
```

```typescript
// GOOD - React component encapsulation
function TaskCard({ gigRef }: Props) {
  // Encapsulate internal state
  const [expanded, setExpanded] = useState(false);
  const gig = useFragment(fragment, gigRef);

  // Private helpers
  const handleToggle = () => setExpanded(!expanded);

  // Public interface is just the props
  return (
    <Pressable onPress={handleToggle}>
      {/* Internal implementation */}
    </Pressable>
  );
}
// Parent components don't know about 'expanded' state
// Clean interface: pass gig data, get rendered card
```

### Encapsulation Guidelines

- Make fields/functions private by default, public only when needed
- Use TypeScript `private`, `protected` modifiers
- Use Elixir module attributes (@) for internal data
- Elixir: prefix private functions with `defp`
- Validate inputs at boundaries (changesets, prop validation)
- Don't expose internal data structures
- Provide focused, minimal public APIs
- Change detection should be internal (don't expose dirty flags)

### Patterns

- **Ecto Changesets**: Encapsulate validation and constraints
- **GraphQL Types**: Only expose fields needed by frontend
- **Command Handlers**: Encapsulate business rules
- **Relay Fragments**: Encapsulate data requirements in component

## Application Checklist

### Before implementing

- [ ] Can I compose instead of inherit? (Composition > Inheritance)
- [ ] Am I reaching through multiple objects? (Law of Demeter)
- [ ] Should this object do the work instead of me? (Tell, Don't Ask)
- [ ] Are internals hidden? (Encapsulation)

### During implementation

- [ ] Use composition (pipes, hooks, interfaces)
- [ ] Call methods on direct collaborators only
- [ ] Push behavior to data owners
- [ ] Make fields/functions private by default
- [ ] Validate at boundaries

### During code review

- [ ] Any deep inheritance hierarchies? (max 2-3 levels)
- [ ] Train wreck chains? (`a.b.c.d()`)
- [ ] Logic operating on other objects' data?
- [ ] Public mutable state?

## Red Flags

### Composition Over Inheritance

- Deep class hierarchies (>3 levels)
- Can't extend because already inheriting
- Duplicating code because can't multi-inherit

### Law of Demeter

- Multiple dots: `user.profile.address.city`
- GraphQL queries 5+ levels deep
- Functions taking many parameters to avoid chaining

### Tell, Don't Ask

- Lots of getters used in if statements
- Business logic outside the entity
- Type checking with if/else (`if type == 'x'`)

### Encapsulation

- Public mutable fields
- Map/any types instead of structured data
- Callers modifying internal state directly
- No validation at boundaries

## Integration with Existing Skills

### Works with

- `solid-principles`: Particularly Single Responsibility and Dependency Inversion
- `ecto-patterns`: Changesets encapsulate validation
- `cqrs-pattern`: Commands tell, don't ask
- `atomic-design-pattern`: Components composed from atoms/molecules
- `simplicity-principles`: Simple composition over complex inheritance

## Remember

### Favor object composition over class inheritance (Gang of Four)

- **Compose** simple behaviors into complex ones
- **Delegate** to direct collaborators only
- **Tell** objects what to do, don't interrogate them
- **Hide** implementation details behind clean interfaces

**Good design is about managing dependencies and protecting
invariants - regardless of paradigm.**
