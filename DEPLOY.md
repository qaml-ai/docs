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

Cloudflare Workers Builds uses the generated config for production and preview
deployments:

```bash
npm run ci:deploy
npm run ci:preview
```

`ci:preview` uploads a Worker version and creates a preview URL without
promoting that version to production traffic.

Verified in Cloudflare on October 13, 2026: Workers Builds is connected to
`qaml-ai/docs`, with `main` as the production branch and non-production builds
enabled. It runs `npm run build`, then `npm run ci:deploy` for `main` or
`npm run ci:preview` for other branches. Merging into `main` deploys production
automatically; a second manual deploy is not needed. Branch previews only
upload a version and do not change production traffic.

## How it works

| Piece | Location |
| --- | --- |
| MDX + `docs.json` | this repo |
| App / CLI | `open-mdx-docs` package |
| Build output | `.open-mdx-docs/` (gitignored) |

`open-mdx-docs` reads this directory as content (`docsDir: "."`), mounts at `/docs`, and deploys the Worker.

## Cancel Mintlify

Already off the Mintlify proxy. Safe to cancel the Mintlify plan once you’ve confirmed https://camelai.com/docs.
