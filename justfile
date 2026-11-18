set positional-arguments

# List available commands.
default:
    @just --list

# Install development dependencies from uv.lock.
setup:
    uv sync --locked

# Run the fast software tests and style and lock checks.
check: lint format-check lock-check test-fast

# Check Python code style.
lint:
    uv run --frozen ruff check .

# Format Python code.
format:
    uv run --frozen ruff format .

# Check Python formatting without changing files.
format-check:
    uv run --frozen ruff format --check .

# Check that uv.lock matches the project configuration.
lock-check:
    uv lock --check

# Run the fast software tests. Extra arguments go to pytest.
test-fast *args:
    uv run --frozen pytest -m "not slow and not paper" "$@"

# Run the full software suite or selected tests.
test *args:
    uv run --frozen pytest "$@"

# Check documentation vocabulary and prose against the baseline.
docs-check:
    uv run --frozen python scripts/check_vocabulary.py
    uv run --frozen python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict
