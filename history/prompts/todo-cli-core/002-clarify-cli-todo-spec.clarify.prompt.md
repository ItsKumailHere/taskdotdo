---
id: 002
title: Clarify CLI todo spec
stage: clarify
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-cli-core
branch: 001-todo-cli-core
user: user
command: /sp.clarify
labels: ["cli","todo","clarification","phase1"]
links:
  spec: specs/001-todo-cli-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-cli-core/spec.md
  - specs/001-todo-cli-core/checklists/requirements.md
tests: []
---

## Prompt

(No additional input - /sp.clarify runs on current feature specification)

## Response snapshot

Resolved 4 ambiguities in CLI todo application specification:

1. **Task Identifier Format**: UUIDs (e.g., "a1b2c3d4-e5f6-7890-abcd-ef1234567890")
   - Rationale: Compatible with PostgreSQL UUID type for future NeonDB integration

2. **Empty Task Description Handling**: Reject with error message "Tasks cannot be created without descriptions"
   - Constraint: CLI remains running (no exit on error)

3. **Configuration File Format**: JSON only
   - Path: `~/.config/todo/config.json`

4. **Data Limits**: 255 chars max for description, 20 chars max per tag

Updated sections:
- Key Entities (Task.id format)
- Edge Cases (empty input, length limits)
- Configuration (JSON format path)
- Created Clarifications section with session record

## Outcome

- ✅ Impact: Specification clarified with 4 resolved ambiguities
- 🧪 Tests: None - clarification phase
- 📁 Files: 2 files updated (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: All critical ambiguities resolved, spec ready for architecture planning

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All checklist items PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
