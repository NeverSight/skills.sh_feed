---
name: cel-k8s
description: Write production-ready CEL (Common Expression Language) code for Kubernetes ValidatingAdmissionPolicies, CRD validation rules, and security policies. Use when users need to create admission policies, validate Kubernetes resources, enforce security constraints, or write CEL expressions for Kubernetes.
---

# CEL for Kubernetes - Production-Ready Policy Generator

Generate solid, high-quality, production-ready CEL (Common Expression Language) code for Kubernetes admission control, CRD validation, and security policy enforcement.

## When to Use This Skill

Use this skill when the user wants to:
- **Write ValidatingAdmissionPolicy** resources with CEL expressions
- **Create CRD validation rules** using x-kubernetes-validations
- **Enforce security policies** (Pod Security Standards, image restrictions, etc.)
- **Validate resource configurations** (labels, annotations, resource limits)
- **Build admission control** without external webhooks
- **Migrate from OPA/Gatekeeper/Kyverno** to native Kubernetes CEL
- **Debug or optimize existing CEL expressions**

## CEL Quick Reference

### Core Operators

```cel
// Comparison
==  !=  <  <=  >  >=

// Logical
&&  ||  !

// Arithmetic
+  -  *  /  %

// Membership
in  // Check if element exists in collection

// Ternary
condition ? trueValue : falseValue
```

### Essential Functions

```cel
// Field existence (CRITICAL - always check before accessing optional fields)
has(object.spec.field)

// String functions
size(string)                    // Length
contains(string, substring)     // Contains check
startsWith(string, prefix)      // Prefix check
endsWith(string, suffix)        // Suffix check
matches(string, regex)          // Regex match
split(string, delimiter)        // Split to list
lower(string)                   // Lowercase
upper(string)                   // Uppercase
trim(string)                    // Remove whitespace

// Collection functions
size(list)                      // List length
all(list, var, condition)       // All elements satisfy
exists(list, var, condition)    // Any element satisfies
exists_one(list, var, condition) // Exactly one satisfies
filter(list, var, condition)    // Filter elements
map(list, var, transformation)  // Transform elements

// Kubernetes-specific
quantity(string)                // Parse K8s quantity (e.g., "2Gi", "500m")
isQuantity(string)              // Validate quantity format
url(string)                     // Parse URL
```

### Available Context Variables

**In ValidatingAdmissionPolicy:**
- `object` - The incoming resource being validated
- `oldObject` - The existing resource (UPDATE operations)
- `request` - Admission request metadata (user, operation, namespace)
- `params` - Parameters from ValidatingAdmissionPolicyBinding
- `namespaceObject` - The namespace resource

**In CRD Validation (x-kubernetes-validations):**
- `self` - The field being validated
- `oldSelf` - Previous field value (UPDATE)

## Instructions for Writing CEL Policies

### Step 1: Understand the Requirement

Before writing any CEL:
1. What resource types need validation? (Deployments, Pods, Services, etc.)
2. What operations should trigger validation? (CREATE, UPDATE, DELETE)
3. What specific conditions must be enforced?
4. Should violations block the request or just audit?

### Step 2: Design the Expression

Follow these principles:

**1. Always use `has()` for optional fields:**
```cel
// CORRECT - Safe field access
has(object.spec.template.spec.securityContext) &&
object.spec.template.spec.securityContext.runAsNonRoot == true

// WRONG - Will error if field doesn't exist
object.spec.template.spec.securityContext.runAsNonRoot == true
```

**2. Handle null/missing values gracefully:**
```cel
// Check for labels existence before accessing
has(object.metadata.labels) &&
'app' in object.metadata.labels &&
object.metadata.labels['app'] == 'myapp'
```

**3. Use short-circuit evaluation:**
```cel
// Fast checks first, expensive operations last
has(object.metadata.labels) &&           // Fast: field existence
'app' in object.metadata.labels &&       // Medium: map lookup
object.metadata.labels['app'].matches('^[a-z]+$')  // Slow: regex
```

**4. Prefer positive assertions:**
```cel
// BETTER - Clear intent
object.spec.replicas >= 1 && object.spec.replicas <= 10

// AVOID - Double negatives
!(object.spec.replicas < 1 || object.spec.replicas > 10)
```

### Step 3: Write the ValidatingAdmissionPolicy

Use this structure:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: "policy-name.example.com"
spec:
  failurePolicy: Fail  # or Ignore for non-critical policies
  matchConstraints:
    resourceRules:
    - apiGroups: ["apps"]
      apiVersions: ["v1"]
      operations: ["CREATE", "UPDATE"]
      resources: ["deployments"]
  validations:
  - expression: "CEL expression here"
    message: "Human-readable error message"
    messageExpression: "'Dynamic message with ' + object.metadata.name"
```

### Step 4: Create the Binding

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: "policy-binding"
spec:
  policyName: "policy-name.example.com"
  validationActions: [Deny]  # or [Audit] for testing
  matchResources:
    namespaceSelector:
      matchLabels:
        environment: production
```

### Step 5: Test Before Deploying

1. **Use dry-run mode:**
   ```bash
   kubectl apply --dry-run=server -f test-resource.yaml
   ```

2. **Start with Audit mode:**
   ```yaml
   validationActions: [Audit]  # Log violations, don't block
   ```

3. **Check events for violations:**
   ```bash
   kubectl get events --field-selector reason=PolicyAudit
   ```

## Common Policy Patterns

### Security Policies

**Require non-root containers:**
```yaml
validations:
- expression: |
    has(object.spec.template.spec.securityContext) &&
    has(object.spec.template.spec.securityContext.runAsNonRoot) &&
    object.spec.template.spec.securityContext.runAsNonRoot == true
  message: "Pods must run as non-root user"
```

**Disallow privileged containers:**
```yaml
validations:
- expression: |
    !has(object.spec.template.spec.containers) ||
    !object.spec.template.spec.containers.exists(c,
      has(c.securityContext) &&
      has(c.securityContext.privileged) &&
      c.securityContext.privileged == true
    )
  message: "Privileged containers are not allowed"
```

**Drop all capabilities:**
```yaml
validations:
- expression: |
    object.spec.template.spec.containers.all(c,
      has(c.securityContext) &&
      has(c.securityContext.capabilities) &&
      has(c.securityContext.capabilities.drop) &&
      c.securityContext.capabilities.drop.exists(cap, cap == 'ALL')
    )
  message: "All containers must drop ALL capabilities"
```

**Restrict to approved registries:**
```yaml
validations:
- expression: |
    object.spec.template.spec.containers.all(c,
      c.image.startsWith('myregistry.io/') ||
      c.image.startsWith('gcr.io/myproject/')
    )
  message: "Container images must come from approved registries"
```

**Disallow latest tag:**
```yaml
validations:
- expression: |
    object.spec.template.spec.containers.all(c,
      c.image.contains(':') && !c.image.endsWith(':latest')
    )
  message: "Container images must not use 'latest' tag"
```

### Resource Validation

**Require resource limits:**
```yaml
validations:
- expression: |
    object.spec.template.spec.containers.all(c,
      has(c.resources) &&
      has(c.resources.limits) &&
      has(c.resources.limits.memory) &&
      has(c.resources.limits.cpu) &&
      has(c.resources.requests) &&
      has(c.resources.requests.memory) &&
      has(c.resources.requests.cpu)
    )
  message: "All containers must define CPU and memory limits and requests"
```

**Enforce resource quotas:**
```yaml
validations:
- expression: |
    object.spec.template.spec.containers.all(c,
      !has(c.resources.requests.memory) ||
      quantity(c.resources.requests.memory) <= quantity('2Gi')
    )
  message: "Memory requests cannot exceed 2Gi per container"
```

### Label and Annotation Validation

**Require specific labels:**
```yaml
validations:
- expression: |
    has(object.metadata.labels) &&
    'app' in object.metadata.labels &&
    'environment' in object.metadata.labels &&
    'team' in object.metadata.labels
  message: "Resources must have 'app', 'environment', and 'team' labels"
```

**Validate label values:**
```yaml
validations:
- expression: |
    !has(object.metadata.labels) ||
    !('environment' in object.metadata.labels) ||
    object.metadata.labels['environment'] in ['dev', 'staging', 'prod']
  message: "environment label must be one of: dev, staging, prod"
```

**Validate naming conventions:**
```yaml
validations:
- expression: |
    object.metadata.name.matches('^[a-z][a-z0-9-]*[a-z0-9]$') &&
    object.metadata.name.size() <= 63
  message: "Resource name must be lowercase alphanumeric with hyphens, max 63 chars"
```

### Network Policies

**Disallow hostNetwork:**
```yaml
validations:
- expression: |
    !has(object.spec.template.spec.hostNetwork) ||
    object.spec.template.spec.hostNetwork == false
  message: "hostNetwork is not allowed"
```

**Disallow hostPath volumes:**
```yaml
validations:
- expression: |
    !has(object.spec.template.spec.volumes) ||
    object.spec.template.spec.volumes.all(v, !has(v.hostPath))
  message: "hostPath volumes are not allowed"
```

## CRD Validation Rules

For CustomResourceDefinitions, use `x-kubernetes-validations`:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myresources.example.com
spec:
  group: example.com
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas:
                type: integer
                minimum: 1
                maximum: 100
                x-kubernetes-validations:
                - rule: "self >= 1 && self <= 100"
                  message: "Replicas must be between 1 and 100"
              schedule:
                type: string
                x-kubernetes-validations:
                - rule: "self.matches('^(\\\\d+|\\\\*)(/\\\\d+)?(\\\\s+(\\\\d+|\\\\*)(/\\\\d+)?){4}$')"
                  message: "Must be a valid cron expression"
            x-kubernetes-validations:
            - rule: "has(self.replicas) || has(self.schedule)"
              message: "Either replicas or schedule must be specified"
```

## Performance Best Practices

### Set Schema Constraints

Help the cost estimator by bounding collections:

```yaml
properties:
  containers:
    type: array
    maxItems: 20       # Bound array iterations
  labels:
    type: object
    maxProperties: 50  # Bound map operations
  name:
    type: string
    maxLength: 253     # Bound string operations
```

### Avoid O(n^2) Patterns

```yaml
# BAD - O(n^2): Nested iteration over same collection
- expression: |
    object.spec.containers.all(c1,
      object.spec.containers.all(c2,
        c1.name != c2.name || c1 == c2
      )
    )

# GOOD - O(n): Use unique check
- expression: |
    object.spec.containers.map(c, c.name).size() ==
    object.spec.containers.size()
  message: "Container names must be unique"
```

### Use Targeted Match Rules

Limit policy scope to reduce evaluations:

```yaml
matchConstraints:
  resourceRules:
  - apiGroups: ["apps"]          # Specific group
    apiVersions: ["v1"]           # Specific version
    operations: ["CREATE"]        # Only CREATE, not every operation
    resources: ["deployments"]    # Specific resource
  namespaceSelector:              # Target specific namespaces
    matchLabels:
      enforce-policies: "true"
```

## Debugging CEL Expressions

### Common Errors and Fixes

**Error: "no such key"**
```cel
// Problem: Accessing map key that doesn't exist
object.metadata.labels['app']

// Fix: Check key existence
has(object.metadata.labels) && 'app' in object.metadata.labels &&
object.metadata.labels['app']
```

**Error: "type mismatch"**
```cel
// Problem: Comparing wrong types
object.spec.replicas == "5"

// Fix: Use correct type
object.spec.replicas == 5
```

**Error: "no such field"**
```cel
// Problem: Accessing field on null object
object.spec.securityContext.runAsNonRoot

// Fix: Check parent existence
has(object.spec.securityContext) &&
object.spec.securityContext.runAsNonRoot == true
```

### Testing Commands

```bash
# Test with dry-run
kubectl apply --dry-run=server -f resource.yaml

# Check policy status
kubectl get validatingadmissionpolicy
kubectl describe validatingadmissionpolicy <name>

# View audit events
kubectl get events --field-selector reason=PolicyAudit

# Check type checking warnings
kubectl get validatingadmissionpolicy <name> -o yaml | grep -A 20 typeChecking
```

## Output Format

When generating CEL policies, always provide:

1. **Complete ValidatingAdmissionPolicy YAML**
2. **Corresponding ValidatingAdmissionPolicyBinding YAML**
3. **Test resources** (both passing and failing examples)
4. **Explanation** of each validation rule
5. **Deployment instructions**

## Reference Files

- **[CEL Syntax Reference](./references/cel_syntax.md)** - Complete language reference
- **[Common Patterns](./references/common_patterns.md)** - Reusable validation patterns
- **[Templates](./templates/)** - Production-ready policy templates

## Kubernetes Version Compatibility

- **CEL in ValidatingAdmissionPolicy**: GA in Kubernetes 1.30+
- **CEL in CRD validation**: GA in Kubernetes 1.29+
- **Alpha/Beta**: Available in earlier versions with feature gates

Always verify target cluster version before generating policies.
