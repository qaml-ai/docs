import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const repositoryRoot = fileURLToPath(new URL('../', import.meta.url));
const packageRoot = path.join(repositoryRoot, 'node_modules', 'open-mdx-docs');

const edits = [
	{
		file: 'react-router.config.ts',
		original:
			"\treturn withSlash.endsWith('/') ? withSlash.slice(0, -1) : withSlash;",
		patched:
			"\treturn withSlash.endsWith('/') ? withSlash : `${withSlash}/`;",
	},
	{
		file: 'vite.config.ts',
		original: "\tserver: {\n\t\tport: 3000,\n\t},",
		patched:
			"\tserver: {\n\t\tport: 3000,\n\t\tfs: {\n\t\t\tallow: [process.cwd(), process.env.DOCS_DIR ?? process.cwd()],\n\t\t},\n\t},",
	},
	{
		// Redirects. open-mdx-docs has no redirect config, so they go at the top
		// of its Worker entry, which serves both `dev` and production. The
		// retired Stream docs (`/docs/stream` and everything under it) go to the
		// sales site's Stream page. See "Redirects" in CLAUDE.md.
		file: 'workers/app.ts',
		original:
			'\tasync fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {\n\t\tconst url = new URL(request.url);\n',
		patched:
			"\tasync fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {\n\t\tconst url = new URL(request.url);\n\t\tif (url.pathname === '/docs/stream' || url.pathname.startsWith('/docs/stream/')) {\n\t\t\treturn Response.redirect('https://camelai.com/stream', 301);\n\t\t}\n",
	},
	// Canonical URLs. Every page names its own URL, without a trailing slash, as
	// `<link rel="canonical">`, from docs.json's `url` (https://camelai.com) and
	// the base path, the same URL the sitemap lists. The page's Markdown twin
	// (`.md`, `.mdx`, or `Accept: text/markdown`) names it in a `Link` header.
	// See "Canonical URLs" in CLAUDE.md.
	{
		file: 'app/routes/docs-page.tsx',
		original: 'export function loader({ params }: Route.LoaderArgs) {',
		patched: 'export function loader({ params, request }: Route.LoaderArgs) {',
	},
	{
		file: 'app/routes/docs-page.tsx',
		original: "\t\tdescription: page.frontmatter.description ?? '',\n\t};\n}",
		patched:
			"\t\tdescription: page.frontmatter.description ?? '',\n\t\tcanonical: `${docsConfig.url ?? new URL(request.url).origin}${withBase(`/${slug}`)}`,\n\t};\n}",
	},
	{
		file: 'app/routes/docs-page.tsx',
		original:
			"\t\t...(data.description ? [{ name: 'description', content: data.description }] : []),\n\t];",
		patched:
			"\t\t...(data.description ? [{ name: 'description', content: data.description }] : []),\n\t\t{ tagName: 'link', rel: 'canonical', href: data.canonical },\n\t];",
	},
	{
		file: 'workers/app.ts',
		original:
			"import { redirectBareBasePath, stripBase } from '~/lib/base';\nimport { firstPageSlug } from '~/lib/docs';\nimport { negotiateMarkdown } from '~/lib/negotiation';",
		patched:
			"import { redirectBareBasePath, stripBase, withBase } from '~/lib/base';\nimport { docsConfig, firstPageSlug } from '~/lib/docs';\nimport { negotiateMarkdown, slugFromPathname } from '~/lib/negotiation';",
	},
	{
		file: 'workers/app.ts',
		original: '\t\tif (negotiated) return negotiated;\n',
		patched:
			"\t\tif (negotiated) {\n\t\t\tconst canonicalSlug = slugFromPathname(appPath)?.slug ?? firstPageSlug();\n\t\t\tconst headers = new Headers(negotiated.headers);\n\t\t\theaders.set('Link', `<${docsConfig.url ?? url.origin}${withBase(`/${canonicalSlug}`)}>; rel=\"canonical\"`);\n\t\t\treturn new Response(negotiated.body, { status: negotiated.status, headers });\n\t\t}\n",
	},
	// Sidebar titles. As in Mintlify, a page's `sidebarTitle` labels it in the
	// sidebar and the Previous/Next links, and `title` stays its heading, its
	// <title> and its name in search and llms.txt. See "Page titles" in CLAUDE.md.
	{
		file: 'app/lib/docs.ts',
		original:
			"\treturn page?.frontmatter.title ?? slug.split('/').pop() ?? slug;\n}\n\nfunction resolveNode(raw: NavEntryRaw): NavNode | null {\n\tif (typeof raw === 'string') {\n\t\tif (!allPages[raw]) return null;\n\t\tconst page: NavPage = { type: 'page', slug: raw, title: pageTitle(raw) };",
		patched:
			"\treturn page?.frontmatter.title ?? slug.split('/').pop() ?? slug;\n}\n\nexport function navTitle(slug: string): string {\n\tconst sidebarTitle = allPages[slug]?.frontmatter.sidebarTitle;\n\treturn typeof sidebarTitle === 'string' && sidebarTitle.trim() ? sidebarTitle : pageTitle(slug);\n}\n\nfunction resolveNode(raw: NavEntryRaw): NavNode | null {\n\tif (typeof raw === 'string') {\n\t\tif (!allPages[raw]) return null;\n\t\tconst page: NavPage = { type: 'page', slug: raw, title: navTitle(raw) };",
	},
	{
		file: 'app/lib/docs.ts',
		original:
			'\t\tprev: prev ? { slug: prev, title: pageTitle(prev) } : undefined,\n\t\tnext: next ? { slug: next, title: pageTitle(next) } : undefined,',
		patched:
			'\t\tprev: prev ? { slug: prev, title: navTitle(prev) } : undefined,\n\t\tnext: next ? { slug: next, title: navTitle(next) } : undefined,',
	},
];

let changed = 0;

for (const edit of edits) {
	const filename = path.join(packageRoot, edit.file);
	let source;

	try {
		source = await readFile(filename, 'utf8');
	} catch (error) {
		throw new Error(`Cannot patch ${filename}. Run bun install first.`, {
			cause: error,
		});
	}

	if (source.includes(edit.patched)) continue;
	if (!source.includes(edit.original)) {
		throw new Error(
			`Refusing to patch ${filename}: the expected open-mdx-docs source changed.`,
		);
	}

	// A function, so `$` in a patch is never read as a replacement pattern.
	await writeFile(filename, source.replace(edit.original, () => edit.patched));
	changed += 1;
}

console.log(
	changed === 0
		? 'open-mdx-docs patches (preview compatibility, redirects, canonical URLs, sidebar titles) already applied.'
		: `Applied ${changed} open-mdx-docs patches (preview compatibility, redirects, canonical URLs, sidebar titles).`,
);
