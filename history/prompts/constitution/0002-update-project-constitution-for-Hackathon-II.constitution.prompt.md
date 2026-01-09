---
id: 0002
title: Update project constitution for Hackathon II
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4
feature: none
branch: main
user: qwen
command: /sp.constitution
labels: [constitution, hackathon, evolution-of-todo, spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution 

Hackathon II: The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI
(Organized by Panaversity, an AI education initiative focused on agentic AI, cloud-native technologies, modern Python, and distributed AI systems; closely linked with programs like PIAIC and GIAIC)
Core Concept & Philosophy
The hackathon teaches the shift from traditional coding to AI-native, spec-driven development, where engineers act as system architects overseeing AI agents (especially using Claude Code) that generate implementation code. Developers write high-level specifications (Markdown-based "Constitution" + detailed specs), iteratively refine them, and let AI produce correct, production-ready code — no manual coding is allowed. The process follows the Nine Pillars of AI-Driven Development and emphasizes Reusable Intelligence (agent skills, subagents).
Project: "Evolution of Todo"
Participants build the same Todo application through five progressive phases, starting from a basic console app and ending as a fully distributed, event-driven, cloud-native AI chatbot system.
Phase Structure & Progression

Phase I (100 pts) — In-memory Python console Todo app (basic CRUD) using Claude Code + Spec-Kit Plus
Phase II (150 pts) — Full-stack web app: Next.js frontend, FastAPI + SQLModel backend, Neon serverless PostgreSQL, user authentication (Better Auth + JWT), monorepo with structured specs
Phase III (200 pts) — AI-powered conversational chatbot using natural language: OpenAI ChatKit UI, OpenAI Agents SDK, Official MCP SDK (tools for task operations), stateless architecture with DB-persisted conversation history
Phase IV (250 pts) — Local cloud-native deployment: Docker, Minikube, Helm charts, AI-assisted K8s tools (kubectl-ai, kagent), Gordon (Docker AI agent)
Phase V (300 pts) — Advanced cloud deployment + intelligent features: Intermediate & Advanced Todo features (priorities/tags, search/filter/sort, recurring tasks, due dates/reminders), event-driven architecture with Kafka (or Redpanda), Dapr sidecars (pub/sub, state, jobs/scheduler, secrets), deployment on DigitalOcean Kubernetes (DOKS), AKS, GKE or Oracle OKE

Total scoring: 1,000 points + up to 600 bonus points
Bonus features: Reusable Intelligence / Cloud-Native Blueprints (+200 each), Urdu language support (+100), Voice commands (+200)
Key Technical & Methodological Requirements

Strict Spec-Driven Development using Spec-Kit Plus + Claude Code throughout (specs → plan → tasks → AI implementation)
Monorepo structure with /specs/, layered CLAUDE.md files, and organized feature/API/database/UI specs
Agentic workflow emphasis: AI agents use MCP tools to interact with the application logic
Stateless, scalable backend design (especially in chatbot & cloud phases)
Focus on AIOps, infrastructure-as-spec/blueprints, and governing AI agents in cloud-native environments

Timeline (2025–2026)

Started: Dec 1, 2025
Phase deadlines: Sundays Dec 7 → Jan 18, 2026
Final submission: Jan 18, 2026
Weekly live Zoom presentations (top submissions invited)

Rewards & Opportunity
Exceptional performers may receive invitations to:

Join the Panaversity core team
Interview to become a startup founder within the Panaversity ecosystem
Teach at Panaversity, PIAIC, or GIAIC
Work directly with founders (Zia, Rehan, Junaid, Wania mentioned)

Submission format (each phase)

Public GitHub repo (with specs history, CLAUDE.md files, code)
Deployed app link (Vercel for Phase II, chatbot URL later)
Short demo video ≤ 90 seconds
WhatsApp number (for potential live presentation invite)

In one sentence
This is an intensive, highly structured individual hackathon that trains participants in modern AI-agent-driven software engineering by evolving a simple Todo app into a production-grade, Kubernetes-orchestrated, event-driven AI chatbot — using spec-driven development, Claude Code, MCP, Dapr, Kafka, and cloud-native practices — with strong emphasis on process discipline and potential career opportunities in the Panaversity AI education/startup ecosystem.

## Response snapshot

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

## Outcome

- ✅ Impact: Created new constitution for Hackathon II project with 6 core principles and governance guidelines
- 🧪 Tests: No tests required for this documentation update
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: None needed at this time
- 🧠 Reflection: Successfully transformed the template constitution with specific details for the hackathon

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): N/A