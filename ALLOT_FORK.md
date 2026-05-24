# Allot fork notes

This is the **Allot fork** of [BerriAI/litellm](https://github.com/BerriAI/litellm). It is consumed by exactly one project:

**Consumer:** `~/Project/management/ai/ai-gateway/` (remote: `git@gitlab.netonomy.co:RnD/ai-gateway-staging.git`, branch `develop`).

Pulled in via `make install-fork` in that repo, which runs:

```bash
uv pip install -e ~/Project/private/litellm-fork --no-deps
```

i.e. an **editable** install layered over the stock `litellm` already in `ai-gateway/.venv`. If `pip install` ever overwrites the package with a fresh stock release, re-run `make install-fork` to restore the editable overlay. The `ai-gateway/litellm_local/patches.py` module provides a runtime monkey-patch fallback (covers commit 2 below only) and self-skips when the fork is detected (canary: `MCPRequestHandler._make_delegated_user_api_key_auth`).

## Branch layout

- `allot/main` — working branch. Has the four Allot commits on top of an upstream merge.
- `main` / `upstream` — tracks `BerriAI/litellm`. Merge upstream into `allot/main`, do not rebase (the fork is installed editable into a live `.venv`, so a force-push would invalidate it).

## Allot commits (on `allot/main`, tagged `ALLOT-FORK:` in code for grep-ability)

All four address MCP observability gaps in the upstream proxy. Draft upstream PRs live at `ai-gateway/litellm_local/UPSTREAM_PR.md` in the consumer repo.

1. `feat(guardrails): add post_mcp_call GuardrailEventHook` — lets response-scrubbing guardrails surface in `/ui/?page=guardrails-monitor`. (UPSTREAM_PR.md PR 1)
2. `fix(mcp): skip user_api_key_auth on delegated-auth MCP requests` — stops the spurious 401 spend-log rows that hid OAuth-MCP activity from `/ui/?page=logs` and `/ui/?page=usage`. (UPSTREAM_PR.md PR 2)
3. `fix(mcp): assign synthetic identity to delegated-auth MCP requests` — paired with commit 2 so the recovery path attaches a usable identity instead of bare `UserAPIKeyAuth()`.
4. `feat(guardrails): expose litellm_logging_obj and propagate mcp_server_name for post_mcp_call` — adds `mcp_server_name` to the synthetic data dict so guardrails can scope per-MCP without parsing tool-name prefixes. (UPSTREAM_PR.md PR 3)

## When working in this fork

- Keep changes minimal and surgical — every line we carry is a line we have to rebase across upstream merges.
- New patches must include an `ALLOT-FORK:` marker comment near the change and a brief note in `ai-gateway/litellm_local/UPSTREAM_PR.md` describing the upstream submission.
- Do not edit upstream-owned docs (this repo's `CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/`) — that creates merge conflicts forever. Allot-specific notes go in *this* file, or in the consumer repo.
- Never push `allot/main` (or any branch with Allot commits) to `upstream` (`BerriAI/litellm`). Push only to `origin` (`PhilipKram/litellm`).
