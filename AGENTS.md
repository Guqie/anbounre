# Repository Guidelines

## Project Structure & Module Organization

This repository is a Markdown-first knowledge base with a structured engineering documentation layer.

### Content Modules (Obsidian Vault)

Core content lives in numbered top-level folders organized by workflow stage and domain. Use `00-每日工作区` for active work, `02-政策于宏观库` and `03-行业研究库` for domain research, and `07-完成归档` for finalized outputs. Reusable templates are under `templates/obsidian`. Automation scripts live in `tools/` (currently `tools/kb_audit.ps1`). Hidden folders such as `.obsidian`, `.spec-workflow`, `.trae`, and `.claude` are environment/config folders and should only be changed intentionally.

### Engineering Documentation (`docs/`)

All engineering design documents are centralized under `docs/`:

```
docs/
├── architecture/    # System overview + Mermaid diagrams
├── design/          # Subagent arch, Gateway/Scheduler, constitution, memory governance
├── guides/          # Implementation roadmap, engineering guide
└── reference/        # Context injection contract
```

Use `docs/README.md` as the entry point for all engineering documentation.

## Build, Test, and Development Commands

There is no compile/build pipeline. Use these commands for maintenance:

- `pwsh -File tools/kb_audit.ps1 -Root .`
 Runs a full knowledge-base audit and writes a dated report.
- `pwsh -File tools/kb_audit.ps1 -Root . -OutFile kb-audit-report.md -CsvFile tools/kb-audit-history.csv`
 Runs audit with explicit report/history paths.
- `rg --files "00-每日工作区" -g "*.md"`
 Fast file discovery when reviewing or refactoring notes.

## Coding Style & Naming Conventions

Use UTF-8 Markdown with clear heading hierarchy (`#`, `##`, `###`) and concise sections.
Prefer YAML frontmatter for structured notes. Existing conventions include tag namespaces like `类型/...` and `状态/...`, plus fields such as `created` and `description`. Naming patterns to follow:

- MOC index files: `_MOC-<主题>.md`
- Daily notes: `YYYY-MM-DD.md`
- Draft workflow docs: suffixes like `_草稿` or `_工作版`
- Engineering docs: numbered prefix for ordering (e.g., `01-subagent-architecture.md`)

## Testing Guidelines

No automated unit-test framework is configured. Validation is content-quality based:

- Run `kb_audit.ps1` before opening a PR.
- Check report sections for missing frontmatter/tags and orphan docs.
- Verify internal wiki links (`[[...]]`) resolve and new notes are reachable from a relevant MOC page.
- For engineering docs: verify Mermaid diagrams render correctly in Obsidian.

## Commit & Pull Request Guidelines

Current history uses prefixed summaries (example: `Fix: Correct remote and initial commit`). Follow `<Type>: <short summary>` (for example, `Docs: update policy MOC links`, `Refactor: move engineering docs to docs/`). PRs should include: purpose, affected directories, notable file additions/moves, and screenshots only for visual/html output changes.

## Security & Configuration Tips

Treat notes as sensitive by default: avoid committing private data, credentials, or client-confidential raw materials. Do not modify workspace/tooling config files unless the PR explicitly targets configuration behavior.
