# Deploying camelAI docs

Content lives in this repo. Rendering is **[open-mdx-docs](https://github.com/Vercantez/open-mdx-docs)** (npm/git dependency).

## Setup

```bash
bun install
bun run doctor
bun run dev
```

## Production

- **URL:** https://camelai.com/docs
- **Worker:** `camelai-docs` (`camelai.com/docs*`)
- **Config:** `open-mdx-docs.config.json`

```bash
# Real Node on PATH (wrangler does not like bun-as-node)
bun run deploy
```

## How it works

| Piece | Location |
| --- | --- |
| MDX + `docs.json` | this repo |
| App / CLI | `open-mdx-docs` package |
| Build output | `.open-mdx-docs/` (gitignored) |

`open-mdx-docs` reads this directory as content (`docsDir: "."`), mounts at `/docs`, and deploys the Worker.

## Cancel Mintlify

Already off the Mintlify proxy. Safe to cancel the Mintlify plan once you’ve confirmed https://camelai.com/docs.
