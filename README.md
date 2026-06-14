# XHS Content Agent

A CLI-first content studio for Xiaohongshu / RedNote creators.

This project helps turn raw ideas, transcripts, product notes, and daily logs into publish-ready note drafts. It is designed as a safe AI agent workflow: plan, draft, review, package, and track content without spam, engagement manipulation, or platform-policy evasion.

## What It Does

- Creates Xiaohongshu-style note drafts from local source material
- Generates titles, hooks, body copy, hashtags, and image prompts
- Builds a lightweight content calendar
- Exports publish packages for manual review
- Keeps structured artifacts for later evaluation and iteration

## What It Does Not Do

- It does not fake engagement, views, likes, follows, or comments
- It does not bypass login, captcha, rate limits, or platform controls
- It does not mass-post without human review
- It does not scrape private or restricted content

The product direction is simple: make a creator faster and more consistent while keeping the account safe.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[openai]"
```

For local development:

```bash
pip install -e ".[dev,openai]"
```

Check local readiness before using the OpenAI generator:

```bash
xhs-content-agent doctor
xhs-content-agent doctor --json
```

## Quick Start

Generate a draft from a local idea file:

```bash
xhs-content-agent draft examples/idea.md --out runs/first-note
```

Generate an offline draft without API calls:

```bash
xhs-content-agent draft examples/idea.md --generator template --out runs/template-note
```

Check whether the OpenAI path is ready before running it:

```bash
xhs-content-agent doctor
xhs-content-agent draft examples/idea.md --generator openai --out runs/openai-note
```

Create a 7-day content calendar:

```bash
xhs-content-agent calendar examples/topics.txt --days 7 --out runs/calendar
```

Validate a publish package:

```bash
xhs-content-agent check runs/template-note/note.json
xhs-content-agent check runs/template-note/note.json --json
xhs-content-agent check runs/template-note/note.json --json --strict
```

Inspect a draft artifact before publishing or after edits:

```bash
xhs-content-agent inspect runs/template-note/note.json
xhs-content-agent inspect runs/template-note/note.json --json
```

That command writes:

```text
runs/check/
  quality-report.json
  quality-report.md
```

## Output

Each draft run writes:

```text
runs/template-note/
  note.json
  note.md
  publish-checklist.md
  quality-report.json
  quality-report.md
```

The checklist is intentionally manual. It helps a human review tone, claims, hashtags, images, and timing before publishing. The quality report gives both a machine-readable artifact for future evaluation work and a readable Markdown summary for everyday editing.

The `inspect` command is the fastest read-only checkpoint. It reports title length, hook coverage, body size, paragraph count, hashtag and image-prompt counts, call-to-action coverage, spammy terms, and the current quality warnings without creating a new output directory.

The `check` command can also run in a read-only automation mode with `--json`, which prints the full quality gate result to stdout instead of creating a `runs/check` directory. Add `--strict` when you want warnings to fail CI or a local harness with a non-zero exit code.

The `doctor` command is a read-only preflight check for local runtime readiness. It reports the current Python version, whether the optional `openai` package is installed, whether `OPENAI_API_KEY` is configured, and which draft generators are currently available.

The quality gate now catches a few common packaging mistakes before publish review:

- missing hooks or oversized opening hooks that weaken the first screen
- duplicate hashtags that make a note look repetitive
- oversized bodies that are hard to scan on mobile
- single-block bodies that need paragraph breaks
- missing source summaries that make later edits drift from the original material

## Positioning

This is part of a broader AI Agent / Harness Engineering portfolio. The project treats content operations as an inspectable workflow:

```text
source material -> content brief -> draft -> quality checks -> publish package -> review
```

Future versions may add browser-assisted publishing, but only with a clear human approval step.

## Roadmap

- OpenAI generator with structured JSON output
- Creator voice profiles
- Post performance log imports
- A/B title variants
- Image prompt packs
- Manual browser-fill assistant
- Evaluation fixtures for note quality

## License

MIT
