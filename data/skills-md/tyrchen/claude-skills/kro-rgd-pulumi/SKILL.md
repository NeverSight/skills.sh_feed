---
name: kro-rgd-pulumi
description: Create production-ready KRO ResourceGraphDefinitions using Pulumi TypeScript. Use when users need to define custom Kubernetes APIs, compose resources with KRO, integrate AWS ACK resources, or build platform abstractions using Pulumi infrastructure as code.
---

# KRO ResourceGraphDefinition with Pulumi TypeScript

Generate production-ready Kubernetes Resource Orchestrator (KRO) ResourceGraphDefinitions using Pulumi TypeScript for creating custom Kubernetes APIs and composing resources with AWS ACK integration.

## When to Use This Skill

Use this skill when the user wants to:

- **Create custom Kubernetes APIs** using KRO ResourceGraphDefinitions
- **Compose multiple K8s resources** as a single declarative unit
- **Integrate AWS resources via ACK** (S3, RDS, DynamoDB, etc.) with KRO
- **Build platform abstractions** for developer self-service
- **Generate Pulumi TypeScript code** for KRO resources
- **Define resource dependencies** with automatic orchestration
- **Create reusable application templates** with CEL expressions (use CEL skill when necessary)

## Overview

### What is KRO?

**KRO (Kube Resource Orchestrator)** is an open-source Kubernetes-native project that allows you to:

- Define custom Kubernetes APIs without writing Go controllers
- Compose multiple resources as a directed acyclic graph (DAG)
- Automatically manage resource dependencies and ordering
- Use CEL expressions for dynamic configuration
- Provide lifecycle management with drift detection

### What is ResourceGraphDefinition (RGD)?

An **RGD** is KRO's core custom resource that:

- Defines a schema for your custom API (apiVersion, kind, spec, status)
- Lists resources to create with CEL expression templating
- Automatically generates a CRD when applied
- Deploys a microcontroller to manage instances

### Pulumi Integration

Using Pulumi TypeScript to deploy KRO resources provides:

- **Type safety** for resource definitions
- **IDE support** with autocomplete and error checking
- **Programmatic logic** for complex configurations
- **GitOps-friendly** workflow
- **Multi-stack architecture** for separation of concerns

## Prerequisites

### Required Components

```bash
# 1. Kubernetes cluster (1.25+ for CEL support)
kubectl version

# 2. KRO installed in cluster
helm install kro oci://ghcr.io/kubernetes-sigs/kro/charts/kro \
  --namespace kro-system \
  --create-namespace

# 3. ACK controllers (if using AWS resources)
helm install ack-s3-controller \
  oci://public.ecr.aws/aws-controllers-k8s/s3-chart \
  --namespace ack-system \
  --create-namespace

# 4. Pulumi CLI and Node.js
pulumi version
node --version
```

### Pulumi Project Setup

```bash
# Create new Pulumi project
mkdir my-kro-project && cd my-kro-project
pulumi new kubernetes-typescript

# Install dependencies
npm install @pulumi/kubernetes @pulumi/pulumi
```

## Instructions

### Step 1: Understand the Requirements

Before generating code, gather:

1. **Custom API design**: What kind/apiVersion? What fields in spec?
2. **Resources to compose**: Deployments, Services, ConfigMaps, ACK resources?
3. **Dependencies**: Which resources depend on others?
4. **Conditions**: Any conditional resource creation (includeWhen)?
5. **Status fields**: What status to expose to users?

### Step 2: Design the Schema

Define the user-facing API:

```typescript
// Schema design principles:
// - Use descriptive field names
// - Provide sensible defaults
// - Group related fields in nested objects
// - Add validation rules for constraints
```

### Step 3: Generate Pulumi TypeScript Code

Use this structure for KRO RGD:

```typescript
import * as k8s from "@pulumi/kubernetes";
import * as pulumi from "@pulumi/pulumi";

// Create the ResourceGraphDefinition
const rgd = new k8s.apiextensions.CustomResource("my-app-rgd", {
    apiVersion: "kro.run/v1alpha1",
    kind: "ResourceGraphDefinition",
    metadata: {
        name: "my-application",
        namespace: "default",
    },
    spec: {
        schema: {
            apiVersion: "v1alpha1",
            kind: "Application",
            spec: {
                // Define user-configurable fields
                name: "string",
                image: "string | default=\"nginx:latest\"",
                replicas: "integer | default=3",
            },
            status: {
                // Auto-populated status fields
                ready: "${deployment.status.conditions.exists(c, c.type == 'Available' && c.status == 'True')}",
                availableReplicas: "${deployment.status.availableReplicas}",
            },
            validation: [
                {
                    expression: "self.replicas >= 1 && self.replicas <= 100",
                    message: "Replicas must be between 1 and 100",
                },
            ],
        },
        resources: [
            {
                id: "deployment",
                template: {
                    apiVersion: "apps/v1",
                    kind: "Deployment",
                    metadata: {
                        name: "${schema.spec.name}",
                    },
                    spec: {
                        replicas: "${schema.spec.replicas}",
                        selector: {
                            matchLabels: {
                                app: "${schema.spec.name}",
                            },
                        },
                        template: {
                            metadata: {
                                labels: {
                                    app: "${schema.spec.name}",
                                },
                            },
                            spec: {
                                containers: [
                                    {
                                        name: "app",
                                        image: "${schema.spec.image}",
                                    },
                                ],
                            },
                        },
                    },
                },
                readyWhen: [
                    "${deployment.status.conditions.exists(c, c.type == 'Available' && c.status == 'True')}",
                ],
            },
            {
                id: "service",
                template: {
                    apiVersion: "v1",
                    kind: "Service",
                    metadata: {
                        name: "${schema.spec.name}-service",
                    },
                    spec: {
                        selector: {
                            app: "${schema.spec.name}",
                        },
                        ports: [
                            {
                                port: 80,
                                targetPort: 8080,
                            },
                        ],
                    },
                },
            },
        ],
    },
});

export const rgdName = rgd.metadata.name;
```

### Step 4: Add ACK Resources (AWS Integration)

For AWS resources via ACK:

```typescript
const rgdWithAws = new k8s.apiextensions.CustomResource("app-with-aws-rgd", {
    apiVersion: "kro.run/v1alpha1",
    kind: "ResourceGraphDefinition",
    metadata: {
        name: "application-with-storage",
    },
    spec: {
        schema: {
            apiVersion: "v1alpha1",
            kind: "AppWithStorage",
            spec: {
                name: "string",
                image: "string",
                bucketName: "string",
            },
            status: {
                bucketArn: "${bucket.status.ackResourceMetadata.arn}",
                ready: "${deployment.status.conditions.exists(c, c.type == 'Available' && c.status == 'True')}",
            },
        },
        resources: [
            // ACK S3 Bucket
            {
                id: "bucket",
                template: {
                    apiVersion: "s3.services.k8s.aws/v1alpha1",
                    kind: "Bucket",
                    metadata: {
                        name: "${schema.spec.bucketName}",
                    },
                    spec: {
                        name: "${schema.spec.bucketName}",
                        tagging: {
                            tagSet: [
                                {
                                    key: "ManagedBy",
                                    value: "KRO",
                                },
                            ],
                        },
                    },
                },
                readyWhen: [
                    "${bucket.status.ackResourceMetadata.?arn != null}",
                ],
            },
            // Deployment referencing bucket
            {
                id: "deployment",
                template: {
                    apiVersion: "apps/v1",
                    kind: "Deployment",
                    metadata: {
                        name: "${schema.spec.name}",
                    },
                    spec: {
                        replicas: 3,
                        selector: {
                            matchLabels: {
                                app: "${schema.spec.name}",
                            },
                        },
                        template: {
                            metadata: {
                                labels: {
                                    app: "${schema.spec.name}",
                                },
                            },
                            spec: {
                                containers: [
                                    {
                                        name: "app",
                                        image: "${schema.spec.image}",
                                        env: [
                                            {
                                                name: "S3_BUCKET",
                                                value: "${schema.spec.bucketName}",
                                            },
                                            {
                                                name: "S3_BUCKET_ARN",
                                                value: "${bucket.status.ackResourceMetadata.arn}",
                                            },
                                        ],
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        ],
    },
});
```

### Step 5: Deploy and Test

```bash
# Deploy the RGD
pulumi up

# Verify RGD is active
kubectl get resourcegraphdefinition
kubectl describe resourcegraphdefinition my-application

# Check generated CRD
kubectl get crd | grep kro

# Create an instance of your custom API
kubectl apply -f - <<EOF
apiVersion: v1alpha1
kind: Application
metadata:
  name: my-test-app
spec:
  name: my-test-app
  image: nginx:1.21
  replicas: 5
EOF

# Monitor instance
kubectl get application
kubectl describe application my-test-app
```

## CEL Expression Reference

### Referencing Schema Fields

```cel
${schema.spec.name}              // User-provided spec field
${schema.metadata.name}          // Instance name
${schema.metadata.namespace}     // Instance namespace
${schema.metadata.uid}           // Unique ID
```

### Referencing Other Resources

```cel
${deployment.metadata.name}      // Resource name
${deployment.spec.replicas}      // Spec field
${deployment.status.?endpoint}   // Optional status field (use ? for null safety)
```

### Operators and Functions

```cel
// Ternary conditional
${schema.spec.env == 'prod' ? 10 : 3}

// String concatenation
${"prefix-" + schema.spec.name}

// Null coalescing
${deployment.status.?ready ?? false}

// List operations
${deployment.status.conditions.exists(c, c.type == 'Available' && c.status == 'True')}
${schema.spec.containers.map(c, c.name)}

// Type conversion
${string(schema.spec.replicas)}
${int(schema.spec.replicasString)}
```

### Conditional Resource Inclusion

```yaml
resources:
  - id: ingress
    includeWhen:
      - ${schema.spec.ingress.enabled}
    template:
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      # ...
```

## Common Patterns

### Pattern 1: Web Application Stack

```typescript
// Creates: Deployment + Service + optional Ingress + optional HPA
const webAppRgd = createWebAppRgd({
    name: "webapp",
    supportsIngress: true,
    supportsAutoscaling: true,
});
```

### Pattern 2: Database Application

```typescript
// Creates: ACK RDS Instance + Secret + ConfigMap + Deployment
const dbAppRgd = createDatabaseAppRgd({
    name: "dbapp",
    dbEngine: "postgres",
    withBackup: true,
});
```

### Pattern 3: Microservices Bundle

```typescript
// Creates: Multiple Deployments + Services + NetworkPolicies
const microservicesRgd = createMicroservicesRgd({
    name: "platform",
    services: ["api", "worker", "scheduler"],
});
```

### Pattern 4: Multi-Environment App

```typescript
// Creates environment-specific resources with quotas
const envAppRgd = createEnvironmentAppRgd({
    name: "envapp",
    environments: ["dev", "staging", "prod"],
});
```

## ACK Resource Integration

### Supported ACK Resources

| Service     | Resource Types                       | ACK Controller           |
|-------------|--------------------------------------|--------------------------|
| S3          | Bucket                               | `s3-controller`          |
| RDS         | DBInstance, DBCluster, DBSubnetGroup | `rds-controller`         |
| DynamoDB    | Table, GlobalTable                   | `dynamodb-controller`    |
| SQS         | Queue                                | `sqs-controller`         |
| SNS         | Topic, Subscription                  | `sns-controller`         |
| Lambda      | Function                             | `lambda-controller`      |
| ElastiCache | CacheCluster, ReplicationGroup       | `elasticache-controller` |

### ACK Status Fields

```cel
// Common ACK status patterns
${bucket.status.ackResourceMetadata.arn}           // AWS ARN
${bucket.status.ackResourceMetadata.ownerAccountID} // AWS Account
${dbinstance.status.endpoint.address}               // RDS endpoint
${dbinstance.status.endpoint.port}                  // RDS port
${queue.status.queueURL}                            // SQS URL
```

## Best Practices

### 1. Schema Design

```yaml
# Good: Clear, intuitive fields with defaults
spec:
  name: string
  image: string | default="nginx:latest"
  replicas: integer | default=3
  environment: string | default="dev"

# Bad: Cryptic field names, no defaults
spec:
  n: string
  i: string
  r: integer
```

### 2. Validation Rules

```yaml
validation:
  - expression: "self.replicas >= 1 && self.replicas <= 100"
    message: "Replicas must be between 1 and 100"
  - expression: "self.environment in ['dev', 'staging', 'prod']"
    message: "Environment must be dev, staging, or prod"
  - expression: "self.environment == 'prod' ? self.replicas >= 3 : true"
    message: "Production requires at least 3 replicas"
```

### 3. Readiness Conditions

```yaml
readyWhen:
  - ${deployment.status.conditions.exists(c, c.type == 'Available' && c.status == 'True')}
  - ${deployment.status.readyReplicas == deployment.spec.replicas}
```

### 4. Status Exposure

```yaml
status:
  ready: ${deployment.status.conditions.exists(c, c.type == 'Available' && c.status == 'True')}
  availableReplicas: ${deployment.status.availableReplicas}
  endpoint: ${service.spec.clusterIP}
  bucketArn: ${bucket.status.ackResourceMetadata.?arn ?? 'pending'}
```

### 5. Naming Conventions

```yaml
# Consistent naming pattern
metadata:
  name: ${schema.spec.name}
  labels:
    app.kubernetes.io/name: ${schema.spec.name}
    app.kubernetes.io/managed-by: kro
```

## Reference Files

- **[KRO Schema Reference](./references/kro_schema.md)** - Complete RGD schema documentation
- **[ACK Resources Reference](./references/ack_resources.md)** - ACK resource definitions and status fields
- **[CEL Expressions Reference](./references/cel_expressions.md)** - CEL syntax and functions
- **[Templates](./templates/)** - Production-ready Pulumi TypeScript templates

## Current Status

**KRO Status:** v1alpha1 (Alpha)

- Not yet production-ready
- Breaking changes may occur
- Kubernetes 1.25+ required
- Latest release: v0.7.1 (December 2025)

**Recommendation:** Use in development/testing environments while awaiting v1beta1 for production readiness.

## Output Format

When generating KRO RGD with Pulumi, always provide:

1. **Complete Pulumi TypeScript code** with proper types
2. **RGD specification** with schema, resources, and validations
3. **Example instance YAML** showing how to use the custom API
4. **Deployment instructions** for both Pulumi and kubectl
5. **Testing commands** to verify the deployment
