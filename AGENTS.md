# Repository Guidelines

## Project Structure & Module Organization

`src/router.py` contains the local Laya decision and Codex CLI entry point. `tests/test_router.py` tests the tier-to-model mapping without downloading a checkpoint. `README.md` explains setup and the limits of routing an active Codex session. Keep new runtime code in `src/` and tests in `tests/`; avoid adding services or frameworks for this small learning project.

## Build, Test, and Development Commands

Create an environment with `uv venv --python 3.14`, then install Laya with `uv pip install -r requirements.txt`. Run a recommendation with `.venv/bin/python -m src.router "Rename this variable"`. Add `--launch` to start a new Codex CLI session using the selected model. Laya downloads a checkpoint on first prediction; no build step is needed.

## Coding Style & Naming Conventions

Use four spaces for Python indentation, `snake_case` for functions and variables, and `UPPER_CASE` for constants. Keep the Laya Choice question and the Codex model mapping readable in `src/router.py`. No formatter or linter is configured; follow standard Python style and avoid adding tooling unless the project grows.

## Testing Guidelines

Run `.venv/bin/python -m unittest discover -s tests -v`. Tests use Python's `unittest` and a small fake Laya result to check model selection and invalid input. Name new tests `test_<behavior>`. Keep default tests offline; no coverage threshold is set. Check actual Laya predictions manually with a few representative prompts before trusting a routing policy.

## Commit & Pull Request Guidelines

There are no commits yet from which to infer a convention. Use short imperative subjects such as `Add Laya routing example`. Keep pull requests focused, describe the behavior changed, and include verification commands and results. Link a related issue when one exists.

## Security & Configuration

Local Laya inference needs no API key. Do not commit Codex credentials or real user prompts. The `--launch` option passes the query to Codex; only use it for content you intend to send to that service. Keep local `.venv/` and `.env` files untracked.
