# Mintlify Frontmatter Reference

Every MDX page must have YAML frontmatter. Full list of supported fields:

## Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title (required) |
| `description` | string | SEO/preview text (required) |
| `sidebarTitle` | string | Abbreviated sidebar label |
| `icon` | string | Sidebar icon (FontAwesome, Lucide, Tabler, URL, or path) |
| `iconType` | string | FontAwesome style variant |
| `tag` | string | Badge label next to sidebar title |

## Visibility & SEO

| Field | Type | Description |
|-------|------|-------------|
| `hidden` | boolean | Remove from sidebar (URL still works) |
| `noindex` | boolean | Prevent search engine indexing |
| `deprecated` | boolean | Show deprecation label |
| `slug` | string | Custom URL path |
| `url` | string | External link destination |
| `keywords` | array | Internal search terms (not displayed) |
| `og:title` | string | Open Graph title |
| `og:image` | string | Open Graph image |

## Layout

| Field | Type | Description |
|-------|------|-------------|
| `mode` | string | `default`, `wide`, `custom`, `frame`, or `center` |
| `timestamp` | boolean | Override global last-modified timestamp setting |

## API-Specific

| Field | Type | Description |
|-------|------|-------------|
| `api` | string | API endpoint for playground (e.g., `POST /users`) |
| `openapi` | string | OpenAPI spec reference (e.g., `openapi.json GET /users`) |
| `openapi-schema` | string | Reference data models from `components.schemas` |
| `asyncapi` | string | AsyncAPI channel reference |
| `playground` | string | Override playground display: `interactive`, `simple`, `none`, `auth` |
| `authMethod` | string | Auth type: `bearer`, `basic`, `key`, `none` |

## Access Control

| Field | Type | Description |
|-------|------|-------------|
| `groups` | array | Access control grouping |
| `version` | string | API/feature version |
| `public` | boolean | Access control flag |

## Example

```yaml
---
title: Quick Start Guide
description: Get up and running with camelAI in under 5 minutes.
sidebarTitle: Quick Start
icon: rocket
mode: wide
---
```
