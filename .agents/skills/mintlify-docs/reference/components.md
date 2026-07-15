# Mintlify Components Reference

## Card

Linked content block with icon, image, or CTA.

```mdx
<Card title="Getting Started" icon="rocket" href="/quickstart">
  Learn how to set up your project.
</Card>
```

| Prop | Type | Description |
|------|------|-------------|
| `title` | string (required) | Card heading |
| `icon` | string | Icon name, URL, path, or inline SVG |
| `iconType` | string | FontAwesome style: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands` |
| `color` | string | Icon color as hex |
| `href` | string | Click destination URL |
| `horizontal` | boolean | Compact horizontal layout |
| `img` | string | Image URL/path at top of card |
| `cta` | string | Custom action button text |
| `arrow` | boolean | Show/hide link arrow icon |

## Columns (formerly CardGroup)

Grid layout container for cards or other content.

```mdx
<Columns cols={3}>
  <Card title="One" icon="1" />
  <Card title="Two" icon="2" />
  <Card title="Three" icon="3" />
</Columns>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `cols` | number | 2 | Columns per row (1-4) |

## Tabs / Tab

Tabbed content sections.

```mdx
<Tabs>
  <Tab title="Node.js" icon="node-js">
    Node content here.
  </Tab>
  <Tab title="Python" icon="python">
    Python content here.
  </Tab>
</Tabs>
```

**Tabs props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `sync` | boolean | true | Sync tab selection across page |

**Tab props:**

| Prop | Type | Description |
|------|------|-------------|
| `title` | string (required) | Tab label |
| `id` | string | Custom anchor ID |
| `icon` | string | Icon name/URL/path |
| `iconType` | string | FontAwesome style variant |
| `borderBottom` | boolean | Add bottom border/padding |

## Accordion / AccordionGroup

Collapsible content sections.

```mdx
<AccordionGroup>
  <Accordion title="FAQ Item 1" defaultOpen>
    Answer content here.
  </Accordion>
  <Accordion title="FAQ Item 2">
    Answer content here.
  </Accordion>
</AccordionGroup>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | string (required) | Preview heading |
| `description` | string | — | Subtitle in preview |
| `defaultOpen` | boolean | false | Auto-expand on load |
| `id` | string | — | Custom anchor ID |
| `icon` | string | — | Icon name/URL/path/SVG |
| `iconType` | string | — | FontAwesome style variant |

## CodeGroup

Multiple code blocks with language tabs.

````mdx
<CodeGroup>
```python Python
print("hello")
```
```javascript JavaScript
console.log("hello")
```
</CodeGroup>
````

| Prop | Type | Description |
|------|------|-------------|
| `dropdown` | boolean | Use dropdown menu instead of tabs |
| `theme` | null | Set to null to disable theme and inherit global styling |

## Steps / Step

Sequential numbered instructions.

```mdx
<Steps>
  <Step title="Install dependencies">
    Run `npm install` in your project directory.
  </Step>
  <Step title="Configure settings">
    Edit `docs.json` with your project details.
  </Step>
</Steps>
```

**Steps props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `titleSize` | string | `p` | Step title heading level: `p`, `h2`, `h3`, `h4` |

**Step props:**

| Prop | Type | Description |
|------|------|-------------|
| `title` | string | Step label |
| `icon` | string | Icon name |
| `iconType` | string | FontAwesome style variant |
| `stepNumber` | number | Explicit step number override |
| `titleSize` | string | Heading level override (`p`, `h2`, `h3`, `h4`) |
| `id` | string | Custom anchor ID |
| `noAnchor` | boolean | Hide anchor link |

## Callouts

Six built-in callout types, all accept children content:

```mdx
<Note>General informational note.</Note>
<Warning>Caution alert — something could go wrong.</Warning>
<Info>Informational highlight.</Info>
<Tip>Helpful suggestion.</Tip>
<Check>Success or confirmation message.</Check>
<Danger>Danger alert — destructive action.</Danger>
```

**Custom Callout:**

```mdx
<Callout icon="star" color="#FFD700">
  Custom callout with icon and color.
</Callout>
```

| Prop | Type | Description |
|------|------|-------------|
| `icon` | string | Icon name |
| `color` | string | Background color hex |
| `iconType` | string | Icon style variant |

## Tooltip

Hover-triggered informational overlay.

```mdx
Hover over <Tooltip tip="This is the tooltip text">this text</Tooltip> for more info.
```

| Prop | Type | Description |
|------|------|-------------|
| `tip` | string (required) | Tooltip text |
| `headline` | string | Bold text above tip |
| `cta` | string | Call-to-action link text |
| `href` | string | CTA link URL |

## Frame

Wrapper for images/content with optional caption.

```mdx
<Frame caption="Dashboard overview">
  ![Dashboard](/images/dashboard.png)
</Frame>
```

| Prop | Type | Description |
|------|------|-------------|
| `caption` | string | Centered text below content (supports markdown) |
| `hint` | string | Text preceding the frame |

## Icon

Inline icon from the configured library.

```mdx
<Icon name="check" /> All done!
```

| Prop | Type | Description |
|------|------|-------------|
| `name` | string | Icon name from configured library |
| `type` | string | FontAwesome style variant |

## Expandable

Expandable section for parameter/field details.

```mdx
<Expandable title="properties" defaultOpen>
  <ResponseField name="id" type="string">
    The unique identifier.
  </ResponseField>
</Expandable>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | string | — | Object name |
| `defaultOpen` | boolean | false | Expand on page load |

## ParamField

Documents API parameters.

```mdx
<ParamField body="name" type="string" required>
  The user's display name.
</ParamField>
```

| Prop | Type | Description |
|------|------|-------------|
| `body` / `path` / `query` / `header` | string | Parameter name and location |
| `type` | string | Parameter type |
| `required` | boolean | Whether required |

## ResponseField

Documents API response fields.

```mdx
<ResponseField name="id" type="string" required>
  Unique identifier for the resource.
</ResponseField>
```

| Prop | Type | Description |
|------|------|-------------|
| `name` | string | Field name |
| `type` | string | Field type |
| `required` | boolean | Whether required |
