<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Modified principles: N/A (new constitution)
- Added sections: All sections
- Removed sections: None
- Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md, .claude/commands/*.md
- Follow-up TODOs: None
-->

# Hackathon II: The Evolution of Todo Constitution

## Core Principles

### Spec-Driven Development
All development follows the Spec-Kit Plus methodology: Constitution → Spec → Plan → Tasks → Implementation.
Specifications must be complete and testable before any implementation begins. AI agents (Claude Code) implement
from specs, not ad-hoc coding.

### AI-Agent First Development
Engineers act as system architects, writing high-level specifications and letting AI agents generate
implementation code. Manual coding is prohibited - all code must be AI-generated from specs using Claude Code
or equivalent AI agents.

### Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle
strictly enforced. All features must have comprehensive test coverage before implementation.

### Progressive Evolution Architecture
Features must be built progressively across five phases: Console app → Full-stack web → AI chatbot →
Cloud-native deployment → Advanced cloud features. Each phase builds on the previous with increasing
complexity and capabilities.

### Monorepo Structure & Reusable Intelligence
All code organized in monorepo with /specs/ directory, layered CLAUDE.md files, and structured feature
specifications. Emphasis on creating reusable agent skills, subagents, and cloud-native blueprints for
future use.

### Cloud-Native & Stateless Design
Backend systems must be stateless, scalable, and cloud-native. Use containerization (Docker),
orchestration (Kubernetes), and modern cloud practices (Dapr, Kafka, event-driven architecture).

## Technical Requirements

Technology stack: Python 3.11, JavaScript/TypeScript (Next.js) + Next.js (App Router), FastAPI, SQLModel,
Neon Serverless Postgres, Better Auth (JWT-based). Advanced phases include OpenAI ChatKit UI, OpenAI Agents
SDK, Docker, Minikube, Helm charts, Kafka/Redpanda, Dapr sidecars.

## Development Workflow

Weekly deliverables on Sundays, public GitHub repo with specs history, deployed app links, demo videos ≤ 90
seconds. Strict adherence to Spec-Kit Plus process with AI agents implementing from specifications.

## Governance

All PRs/reviews must verify compliance with spec-driven development. Constitution supersedes all other
practices. Amendments require documentation and approval. Use CLAUDE.md files for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-01 | **Last Amended**: 2026-01-07