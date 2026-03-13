# Mintlify Navigation Reference

Navigation is configured in `docs.json` under the `navigation` key. It uses a recursive structure where building blocks can be arbitrarily nested.

## Building Blocks

### Pages

Array of file path strings (without `.mdx` extension). Paths are relative to the repo root.

```json
{ "pages": ["quickstart", "guides/getting-started"] }
```

### Groups

Collapsible sidebar sections.

```json
{
  "group": "Getting Started",
  "icon": "play",
  "tag": "NEW",
  "expanded": false,
  "root": "overview",
  "pages": ["quickstart", "installation"]
}
```

| Prop | Type | Description |
|------|------|-------------|
| `group` | string | Section name (required) |
| `pages` | array | Child pages/groups (required) |
| `icon` | string | Sidebar icon |
| `tag` | string | Badge label |
| `expanded` | boolean | Whether expanded by default |
| `root` | string | Main page path for the group |

### Tabs

Top-level horizontal navigation sections.

```json
{
  "tab": "API Reference",
  "icon": "square-terminal",
  "groups": [
    {
      "group": "Endpoints",
      "pages": ["api/users", "api/projects"]
    }
  ]
}
```

### Anchors

Persistent sidebar items (typically external links). Placed under `navigation.global.anchors`.

```json
{
  "anchor": "GitHub",
  "href": "https://github.com/org/repo",
  "icon": "github"
}
```

### Dropdowns

Expandable top-sidebar menus.

```json
{
  "dropdown": "Resources",
  "icon": "book-open",
  "pages": [...]
}
```

### Products

Separate product documentation areas within one site.

```json
{
  "product": "Core API",
  "description": "API documentation",
  "icon": "api",
  "groups": [...]
}
```

### Versions

Version-specific documentation partitions.

```json
{
  "version": "2.0.0",
  "default": true,
  "tag": "Latest",
  "groups": [...]
}
```

### Languages

Localization support (27+ languages).

```json
{
  "language": "es",
  "groups": [...]
}
```

## OpenAPI Auto-Generation

Set `openapi` at any navigation level to auto-generate API pages from a spec:

```json
{
  "group": "API Reference",
  "openapi": "openapi.json"
}
```

Child elements inherit the parent's spec unless overridden. For selective endpoints, use `"METHOD /path"` strings in the `pages` array:

```json
{
  "group": "Users",
  "pages": ["GET /users", "POST /users", "GET /users/{id}"]
}
```

## Typical Structure

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "groups": [
          {
            "group": "Getting Started",
            "pages": ["overview", "quickstart"]
          },
          {
            "group": "Guides",
            "pages": ["guides/setup", "guides/advanced"]
          }
        ]
      },
      {
        "tab": "API Reference",
        "groups": [
          {
            "group": "API Reference",
            "openapi": "openapi.json"
          }
        ]
      }
    ],
    "global": {
      "anchors": [
        { "anchor": "GitHub", "href": "https://github.com/org", "icon": "github" }
      ]
    }
  }
}
```
