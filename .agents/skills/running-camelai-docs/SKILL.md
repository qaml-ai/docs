---
name: running-camelai-docs
description: Runs and verifies the camelAI documentation site locally with open-mdx-docs. Use when asked to start, run, open, preview, test, or troubleshoot the docs server, especially inside a Conductor workspace or when choosing between open-mdx-docs and the legacy Mintlify CLI.
---

# Run camelAI docs

Use `open-mdx-docs`, which is the current renderer. The repository keeps a Mintlify-compatible `docs.json` and MDX structure, but `mint dev` and `mintlify dev` launch the retired Mintlify experience and must not be used.

## Start the preview

Run from the repository root:

```bash
bun install --frozen-lockfile
bun run dev -- --port "${CONDUCTOR_PORT:-3000}"
```

Keep the dev command alive in a long-running terminal session. Wait for the `Local` URL before reporting success.

Open the exact base-path URL, including `/docs/`:

```text
http://localhost:<port>/docs/
```

In Conductor, always prefer its allocated `CONDUCTOR_PORT`; do not fall back to a fixed port when that variable is present.

## Verify the preview

Run the bundled verifier while the server is running:

```bash
node .agents/skills/running-camelai-docs/scripts/verify-preview.mjs \
  "http://localhost:${CONDUCTOR_PORT:-3000}/docs/"
```

Do not treat an HTML `200` alone as sufficient. The verifier also checks the client entry module and generated critical CSS, catching a server that renders initial HTML but fails to hydrate in the browser.

## Troubleshoot

- If dependencies are missing, run `bun install --frozen-lockfile`; the repository's `postinstall` script applies the required local renderer compatibility fix.
- If the server reports a React Router `basename`/Vite `base` mismatch, rerun `bun install --frozen-lockfile` and confirm the postinstall patch succeeds. Do not edit `node_modules` by hand.
- If the page resembles the old Mintlify site, stop that process and confirm the running command is `open-mdx-docs dev` and the URL ends in `/docs/`.
- Ignore React Router future-flag and `vite-tsconfig-paths` warnings when the verifier passes.
- Read `open-mdx-docs.config.json` and `DEPLOY.md` before changing the base path or deployment behavior.

End with the verified URL and leave the requested server running.
