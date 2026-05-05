---
name: mintlify-docs
description: Write and maintain Mintlify documentation sites. Use when creating or editing MDX pages, configuring docs.json, using Mintlify components, setting up navigation, or working with OpenAPI specs in a Mintlify project.
---

# Mintlify Documentation

## Working Relationship

- Push back on ideas when it leads to better documentation. Cite sources and explain reasoning.

## Project Context

- Format: MDX files with YAML frontmatter
- Config: `docs.json` for navigation, theme, settings
- Schema reference: `https://mintlify.com/docs.json`

## Content Strategy

- Document just enough for user success — not too much, not too little
- Prioritize accuracy and usability
- Make content evergreen when possible
- Search for existing content before adding anything new. Avoid duplication unless strategic
- Check existing patterns for consistency
- Start by making the smallest reasonable changes

## Frontmatter

Every MDX page requires frontmatter. Common fields:

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Clear, descriptive page title |
| `description` | Yes | Concise summary for SEO/navigation |
| `sidebarTitle` | No | Abbreviated sidebar label |
| `icon` | No | Sidebar icon name |
| `mode` | No | Layout: `default`, `wide`, `custom`, `frame`, `center` |
| `api` | No | API endpoint for playground (e.g., `POST /users`) |
| `openapi` | No | OpenAPI spec reference |
| `hidden` | No | Hide from sidebar (URL still works) |
| `slug` | No | Custom URL path |

Full frontmatter reference: [reference/frontmatter.md](reference/frontmatter.md)

## Writing Standards

- Second-person voice ("you")
- Prerequisites at start of procedural content
- Test all code examples before publishing
- Match style and formatting of existing pages
- Include both basic and advanced use cases
- Language tags on all code blocks
- Alt text on all images
- Relative paths for internal links

## Linking to Sections (Anchors)

Mintlify auto-generates an anchor slug from each heading's text — apostrophes and commas are **kept** in the slug (URL-encoded as `%E2%80%99` and `%2C`), not stripped. Don't guess the slug from the heading text.

For any heading you intend to deep-link to, set an explicit, stable anchor with `{#custom-id}` syntax:

```mdx
## Using a provider we don't support directly (Azure, Vertex, etc.) {#unsupported-providers}
```

Then link with the clean slug:

```mdx
[See unsupported providers](#unsupported-providers)
[See unsupported providers](/plans/model-providers#unsupported-providers)
```

Benefits: short URLs, stable links if heading text changes later, no encoding gotchas with punctuation.

## Do Not

- Skip frontmatter on any MDX file
- Use absolute URLs for internal links
- Include untested code examples

## Components

Use Mintlify's built-in components. Quick reference for the most common ones:

| Component | Use For |
|-----------|---------|
| `<Card>` | Linked content blocks with icon/image |
| `<Columns cols={N}>` | Grid layout (1-4 columns) |
| `<Tabs>` / `<Tab>` | Tabbed content sections |
| `<Accordion>` | Collapsible content |
| `<CodeGroup>` | Multiple code blocks with tabs |
| `<Steps>` / `<Step>` | Sequential instructions |
| `<Note>`, `<Warning>`, `<Info>`, `<Tip>`, `<Check>`, `<Danger>` | Callout boxes |
| `<Tooltip>` | Hover text |
| `<Frame>` | Image wrapper with caption |
| `<Expandable>` | Expandable parameter details |

Full component reference with props: [reference/components.md](reference/components.md)

## docs.json Structure

The `docs.json` file controls site-wide configuration. Key sections:

- **`theme`** — Layout theme (`mint`, `maple`, `palm`, `willow`, `linden`, `almond`, `aspen`, `sequoia`, `luma`)
- **`name`** — Project name
- **`colors`** — `primary`, `light`, `dark` hex values
- **`logo`** — Light/dark mode logo paths
- **`navigation`** — Tabs, groups, pages, anchors, dropdowns
- **`navbar`** — Top nav links and primary CTA button
- **`footer`** — Social links and footer columns
- **`api`** — OpenAPI specs, playground settings, auth config

Full docs.json reference: [reference/docs-json.md](reference/docs-json.md)

## Navigation

Navigation is a recursive structure in `docs.json`. Building blocks:

- **Pages** — Array of file path strings (e.g., `"getting-started/overview"`)
- **Groups** — Collapsible sidebar sections with `group`, `pages`, optional `icon`/`tag`/`expanded`/`root`
- **Tabs** — Top-level horizontal sections with `tab` and nested `groups`
- **Anchors** — Persistent sidebar items with `anchor`, `href`, `icon`
- **Dropdowns** — Expandable top-sidebar menus
- **Versions** — Version-specific partitions
- **Products** — Separate product documentation areas

These can be arbitrarily mixed and nested. Full details: [reference/navigation.md](reference/navigation.md)

## Code Blocks

````mdx
```python title="example.py" highlight={2} lines
import os
key = os.getenv("API_KEY")  # this line is highlighted
```
````

Features: `lines` (line numbers), `highlight={1-2,5}`, `focus={2,4-5}`, `title="Label"`, `wrap`, `expandable`.

Visual diffs in code: `// [!code ++]` and `// [!code --]` comments.

Use `<CodeGroup>` to show multiple languages:

```mdx
<CodeGroup>
```python Python
print("hello")
```
```javascript JavaScript
console.log("hello")
```
</CodeGroup>
```

## Reusable Snippets

Place reusable MDX in `/snippets/` (not rendered as pages). Import and use:

```mdx
import MySnippet from "/snippets/my-snippet.mdx";

<MySnippet />
```

Snippets support props for parameterized content.

## API Documentation

Three approaches for OpenAPI-based API docs:

1. **Auto-generate from spec** — Set `"openapi": "spec.json"` at group level in navigation
2. **Selective endpoints** — Use `"METHOD /path"` strings in `pages` array
3. **Custom MDX pages** — Use `openapi` frontmatter field

Full API docs reference: [reference/api-docs.md](reference/api-docs.md)

## Images and Assets

- Store anywhere in repo; path maps to URL
- Reference: `![alt text](/images/my-image.png)` or wrap with `<Frame caption="...">`
- Max file size: 20 MB for images, 100 MB for other files
- Supported: PNG, JPG, GIF, WebP, SVG, ICO, MP4, WebM, MP3, WAV, JSON, YAML, CSS, JS, WOFF/WOFF2/TTF

## Variables

Define in `docs.json` under `variables`, use as `{{variableName}}` anywhere in content.

## Deployment

Push to GitHub with the Mintlify GitHub App installed. Deploys are automatic — no build steps needed.
