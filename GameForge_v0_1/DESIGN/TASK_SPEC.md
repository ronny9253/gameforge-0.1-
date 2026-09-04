# GameForge Task Contract v0.1

Every agent task must be independently understandable, bounded, testable and reversible.

## Required fields

- `task_id`
- `title`
- `objective`
- `scope`
- `requirements`
- `constraints`
- `dependencies`
- `allowed_paths`
- `forbidden_paths`
- `acceptance_criteria`
- `tests`
- `expected_outputs`

## Execution lifecycle

```text
READY -> IN_PROGRESS -> TESTING -> PASS -> COMMIT -> DONE
                              \-> FAIL -> FIX -> TESTING
```

## Rules

1. An agent may not broaden scope without a new task.
2. An agent may not modify forbidden paths.
3. Acceptance criteria must be observable.
4. Tests must be executable or manually verifiable.
5. A task is not DONE because code compiles; it is DONE when acceptance criteria pass.
