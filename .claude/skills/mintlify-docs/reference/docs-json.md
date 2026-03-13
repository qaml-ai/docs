# docs.json Configuration Reference

The `docs.json` file is the central configuration for a Mintlify site. Schema: `https://mintlify.com/docs.json`

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `theme` | string | Layout theme: `mint`, `maple`, `palm`, `willow`, `linden`, `almond`, `aspen`, `sequoia`, `luma` |
| `name` | string | Project/org name |
| `colors.primary` | string | Primary hex color |
| `navigation` | object | Content structure |

## Branding

```json
{
  "name": "My Docs",
  "logo": { "light": "/logo/light.png", "dark": "/logo/dark.png" },
  "favicon": "/favicon.png",
  "colors": {
    "primary": "#3F60C1",
    "light": "#5F83F0",
    "dark": "#3F60C1"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `logo` | object/string | Light/dark mode logo paths, optional `href` |
| `favicon` | object/string | Light/dark favicon paths |
| `colors.light` | string | Emphasis color for dark mode |
| `colors.dark` | string | Button/hover color for both modes |

## Appearance

| Field | Type | Description |
|-------|------|-------------|
| `appearance.default` | string | `system`, `light`, or `dark` |
| `appearance.strict` | boolean | Hide light/dark mode toggle |
| `background.decoration` | string | `gradient`, `grid`, or `windows` |
| `background.color` | object | Custom `light`/`dark` background hex colors |
| `background.image` | object/string | Light/dark background images |

## Fonts

```json
{
  "fonts": {
    "heading": { "family": "Inter", "weight": 700 },
    "body": { "family": "Inter", "weight": 400 }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `fonts.family` | string | Google Font or custom font name |
| `fonts.weight` | number | Font weight |
| `fonts.source` | string | URL or path to font file |
| `fonts.format` | string | `woff` or `woff2` |
| `fonts.heading` / `fonts.body` | object | Separate heading/body overrides |

## Styling

| Field | Type | Description |
|-------|------|-------------|
| `styling.eyebrows` | string | `section` or `breadcrumbs` |
| `styling.latex` | boolean | Force-load or prevent LaTeX |
| `styling.codeblocks` | object/string | `system`, `dark`, or custom Shiki theme |
| `icons.library` | string | `fontawesome`, `lucide`, or `tabler` |

## Navbar

```json
{
  "navbar": {
    "links": [{ "label": "Support", "href": "mailto:support@example.com" }],
    "primary": { "type": "button", "label": "Get Started", "href": "/signup" }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `navbar.links` | array | External links with `label` and `href` |
| `navbar.primary` | object | Primary button: `type` (`button`, `github`, `discord`), `label`, `href` |

## Footer

```json
{
  "footer": {
    "socials": { "github": "https://github.com/org", "x": "https://x.com/org" },
    "links": [{ "header": "Resources", "items": [{ "label": "Blog", "href": "/blog" }] }]
  }
}
```

Social keys: `x`, `facebook`, `youtube`, `github`, `linkedin`, `slack`, `discord`, `instagram`, `hacker-news`, `medium`, `website`.

## API Configuration

```json
{
  "api": {
    "openapi": "openapi.json",
    "playground": { "display": "interactive" },
    "params": { "expanded": "all" },
    "examples": { "languages": ["python", "javascript", "curl"] }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `api.openapi` | string/array/object | OpenAPI spec file(s) or directory |
| `api.playground.display` | string | `interactive`, `simple`, `none`, or `auth` |
| `api.playground.proxy` | boolean | Proxy requests through Mintlify |
| `api.params.expanded` | string | `all` or `closed` |
| `api.examples.languages` | array | Code example languages |
| `api.examples.autogenerate` | boolean | Generate samples from spec |
| `api.mdx.server` | string/array | Base URL for relative paths |
| `api.mdx.auth.method` | string | `bearer`, `basic`, `key`, or `cobo` |

## SEO

| Field | Type | Description |
|-------|------|-------------|
| `seo.metatags` | object | Custom meta tags |
| `seo.indexing` | string | `navigable` or `all` |

## Other Settings

| Field | Type | Description |
|-------|------|-------------|
| `variables` | object | Key-value pairs for `{{variableName}}` replacement |
| `banner.content` | string | Top-of-page banner (supports MDX) |
| `banner.dismissible` | boolean | Show dismiss button on banner |
| `metadata.timestamp` | boolean | Enable last-modified dates |
| `search.prompt` | string | Search bar placeholder text |
| `redirects` | array | Objects with `source`, `destination`, `permanent` |

## Analytics Integrations

Supported under `integrations`:
- `ga4.measurementId` — Google Analytics 4
- `gtm.tagId` — Google Tag Manager
- `posthog.apiKey` — PostHog (with optional `sessionRecording`)
- `amplitude.apiKey` — Amplitude
- `segment` — Segment
- `mixpanel` — Mixpanel
- `hotjar` — Hotjar
- `clarity` — Microsoft Clarity
- `fathom` — Fathom
- `heap` — Heap
- `logrocket` — LogRocket
- `plausible` — Plausible
- `intercom` — Intercom
