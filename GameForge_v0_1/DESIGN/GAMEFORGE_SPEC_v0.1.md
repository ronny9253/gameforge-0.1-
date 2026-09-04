# GameForge Specification v0.1

## Mission
Build simple 2D mobile casual games with professional perceived quality through a reusable, AI-native production system.

## Design Envelope
- Unity 6
- Android + iOS
- 2D-first
- Portrait-first
- Touch-first
- Single-player
- One core mechanic
- Short sessions (30 sec–5 min)
- Low technical complexity, high polish

## Core Principle
Maximize perceived quality / development complexity.

## AI Routing
1. Script if deterministic automation can do it.
2. Local LLM for cheap repetitive reasoning/metadata/QA/documentation.
3. Specialized tools for specialized work (ComfyUI, FFmpeg, etc.).
4. Codex for architecture, gameplay, debugging, refactoring and difficult integration.

## Mandatory Project Contracts
- GAME_MANIFEST.json exists and validates.
- ASSET_MANIFEST.json exists and validates.
- GameForge core remains reusable and isolated from game-specific logic.
- Every agent task defines scope, acceptance criteria and allowed paths.
- Every meaningful change is tested and committed.

## Validation Target
`gameforge validate` must return a deterministic PASS/FAIL report for the project contracts.
