# Deploying camelAI docs

This repo is **content only** (`docs.json` + MDX). Rendering and hosting moved off Mintlify to [open-mdx-docs](https://github.com/Vercantez/open-mdx-docs).

## Production

- **URL:** https://camelai.com/docs
- **Worker:** `camelai-docs` (route `camelai.com/docs*`)
- **Renderer:** open-mdx-docs with `BASE_PATH=/docs`

## Deploy a content update

```bash
git clone https://github.com/Vercantez/open-mdx-docs.git
cd open-mdx-docs
bun install

# Point at this content repo (or a checkout path)
export DOCS_DIR=/path/to/qaml-ai/docs
export BASE_PATH=/docs

# Optional: only ship nav-linked pages (recommended)
# or set DOCS_DIR to a cleaned content tree

bun run build
# Use a Node binary (not Bun-as-node) for wrangler:
PATH="$(dirname $(which node | head -1)):$PATH" \
  npx wrangler deploy -c wrangler.camelai.jsonc --keep-vars
```

Or from a machine that already has both repos:

```bash
cd open-mdx-docs
BASE_PATH=/docs DOCS_DIR=../docs bun run build
npx wrangler deploy -c wrangler.camelai.jsonc --keep-vars
```

## Local preview

```bash
cd open-mdx-docs
BASE_PATH=/docs DOCS_DIR=/path/to/qaml-ai/docs bun run dev
# open http://localhost:3000/docs
```

## Cancel Mintlify

1. Confirm https://camelai.com/docs is the new site (no Mintlify chrome).
2. In the Mintlify dashboard, remove the `camelai` / camelAI docs project (or cancel the plan).
3. DNS: you do **not** need a Mintlify CNAME — Cloudflare Worker route owns `camelai.com/docs*`.
4. Do not run `wrangler deploy` from this content repo (scripts are disabled).

## AI Search (optional upgrade)

Create a Cloudflare AI Search instance with a **website** source on `https://camelai.com/docs`, name it `camelai-docs`, then uncomment `ai_search_namespaces` in open-mdx-docs `wrangler.camelai.jsonc` and redeploy.
