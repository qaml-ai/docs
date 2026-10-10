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

	await writeFile(filename, source.replace(edit.original, edit.patched));
	changed += 1;
}

console.log(
	changed === 0
		? 'open-mdx-docs patches (preview compatibility, redirects) already applied.'
		: `Applied open-mdx-docs patches (preview compatibility, redirects) to ${changed} files.`,
);
