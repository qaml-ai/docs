# Mintlify API Documentation Reference

## OpenAPI Support

Mintlify supports OpenAPI 3.0 and 3.1 specs in JSON or YAML format.

## Three Approaches

### 1. Auto-generate from spec

Reference the spec at a navigation group level. All endpoints are auto-generated as pages.

```json
{
  "group": "API Reference",
  "openapi": "openapi.json"
}
```

The spec can be a local file path, URL, or directory of spec files.

### 2. Selective endpoints

List specific endpoints in the `pages` array using `"METHOD /path"` notation:

```json
{
  "group": "Users",
  "pages": ["GET /users", "POST /users", "DELETE /users/{id}"]
}
```

### 3. Custom MDX pages

Create MDX files with `openapi` frontmatter for full control over page content:

```yaml
---
title: List Users
openapi: openapi.json GET /users
---
```

## Spec Cascading

Child navigation elements inherit the parent's spec. Override at any level:

```json
{
  "tab": "API",
  "groups": [
    { "group": "v1", "openapi": "v1.json", "pages": [...] },
    { "group": "v2", "openapi": "v2.json", "pages": [...] }
  ]
}
```

## x-mint Extension

Custom Mintlify metadata within OpenAPI specs:

| Field | Description |
|-------|-------------|
| `x-mint.metadata.title` | Override page title |
| `x-mint.metadata.description` | Override page description |
| `x-mint.metadata.playground` | Override playground display |
| `x-mint.content` | Add MDX content before auto-generated docs |
| `x-mint.href` | Custom page URL |
| `x-hidden` | Creates undocumented but accessible pages |
| `x-excluded` | Completely removes endpoints from docs |
| `x-codeSamples` | SDK examples with `lang`, `label`, `source` |

## Authentication

Define `securitySchemes` in the OpenAPI spec's `components` section. Mintlify supports:
- API Keys (header, query, or cookie)
- Bearer tokens
- Basic auth

Configure the playground auth method in `docs.json`:

```json
{
  "api": {
    "mdx": {
      "auth": { "method": "bearer" }
    }
  }
}
```

## Auto-Generate MDX from Spec

Use the Mintlify CLI to scaffold MDX files from an OpenAPI spec:

```bash
npx @mintlify/scraping@latest openapi-file <path-to-spec> -o <output-folder>
```

## Playground Configuration

Control the API playground behavior in `docs.json`:

```json
{
  "api": {
    "playground": {
      "display": "interactive",
      "proxy": true
    },
    "params": { "expanded": "all" },
    "examples": {
      "languages": ["python", "javascript", "curl"],
      "autogenerate": true
    }
  }
}
```

Display options: `interactive` (full playground), `simple` (read-only), `none` (hidden), `auth` (auth only).
