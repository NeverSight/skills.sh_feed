---
name: spring-boot-full-stack
version: 1.0.0
description: |
  Complete Java Spring Boot skill set for building enterprise applications.
  Includes modular architecture with optional components:
  - PostgreSQL database with JPA/Hibernate + Flyway migration
  - Redis caching (optional)
  - Kafka/RabbitMQ messaging (optional, choose one)
  - JWT + OAuth2 authentication (optional OAuth2)
  - RBAC authorization (optional)
  - TDD with Mockito
  - Spec-First Development with OpenSpec

author: Expert Panel (AI Generated)
tags:
  - java
  - spring-boot
  - postgresql
  - redis
  - kafka
  - rabbitmq
  - authentication
  - security
  - tdd
  - openspec

triggers:
  - "spring boot project"
  - "java backend"
  - "microservice"
  - "api development"
  - "enterprise application"

dependencies: []
---

# Spring Boot Full Stack Skill

## Overview

This skill provides a complete, modular framework for building Java Spring Boot applications with enterprise-grade features.

## Quick Start

```bash
# Minimal setup (PostgreSQL + JWT only)
mvn clean install -Pminimal

# With Redis caching
mvn clean install -Dmodule.redis.enabled=true

# Full stack (all modules)
mvn clean install -Pfull-stack

# Run application
mvn spring-boot:run -Dspring-boot.run.profiles=local
```

## Module Selection

| Module | Default | Enable Flag |
|--------|---------|-------------|
| PostgreSQL | ON | `-Dmodule.postgresql.enabled=true` |
| Redis | OFF | `-Dmodule.redis.enabled=true` |
| Kafka | OFF | `-Dmodule.kafka.enabled=true` |
| RabbitMQ | OFF | `-Dmodule.rabbitmq.enabled=true` |
| OAuth2 | OFF | `-Dmodule.oauth2.enabled=true` |

## Development Workflow

1. **Spec First**: Define specifications in `openspec/specs/`
2. **TDD**: Write tests first (RED)
3. **Implement**: Write minimal code (GREEN)
4. **Refactor**: Improve code quality
5. **Archive**: Update specs after implementation

## Docker Options

```bash
# Without Docker (services installed locally)
make dev

# With Docker infrastructure
make dev-docker

# Full Docker deployment
docker compose --profile with-app up -d
```

## Skills Included

### Core (Always enabled)
- `spring-project-init` - Project initialization
- `spring-maven-modular` - Maven profiles & BOM
- `spring-error-handling` - Global exception handling
- `spring-validation` - Request validation
- `spring-logging` - Structured logging
- `spring-testing` - Unit + Integration testing
- `spring-tdd-mockito` - TDD with Mockito
- `spring-openspec` - Spec-First Development

### Optional
- `spring-redis` - Redis caching
- `spring-kafka` - Kafka messaging
- `spring-rabbitmq` - RabbitMQ messaging
- `spring-oauth2` - OAuth2/OIDC
- `spring-rbac` - Role-based access control
- `spring-docker` - Docker containerization
- `spring-api-docs` - OpenAPI/Swagger
- `spring-monitoring` - Actuator + Prometheus

## File Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/company/app/
│   │       ├── config/           # Configuration classes
│   │       ├── controller/       # REST controllers
│   │       ├── service/          # Business logic
│   │       ├── repository/       # Data access
│   │       ├── domain/           # Entities
│   │       ├── dto/              # Data transfer objects
│   │       ├── exception/        # Custom exceptions
│   │       └── security/         # Security configuration
│   └── resources/
│       ├── application.yml
│       ├── application-local.yml
│       ├── application-dev.yml
│       ├── application-prod.yml
│       └── db/migration/         # Flyway migrations
├── test/
│   └── java/
│       └── com/company/app/
│           ├── unit/             # Unit tests
│           └── integration/      # Integration tests
└── openspec/
    ├── AGENTS.md
    ├── specs/                    # Feature specifications
    └── changes/                  # Proposed changes
```

## References

- [Anthropic Skills Specification](https://agentskills.io)
- [OpenSpec - Spec-Driven Development](https://github.com/Fission-AI/OpenSpec)
- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
