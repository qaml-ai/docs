/**
 * DEPRECATED: This Mintlify reverse-proxy Worker is no longer used.
 *
 * Production docs at https://camelai.com/docs are served by open-mdx-docs:
 *   https://github.com/Vercantez/open-mdx-docs
 *
 * Deploy from that repo:
 *   BASE_PATH=/docs DOCS_DIR=/path/to/this/repo bun run build
 *   wrangler deploy -c wrangler.camelai.jsonc
 *
 * Kept as a stub so accidental `wrangler deploy` from this repo fails loudly
 * instead of restoring the Mintlify proxy.
 */

export default {
	async fetch(): Promise<Response> {
		return new Response(
			[
				'camelai-docs is no longer the Mintlify proxy.',
				'',
				'Deploy open-mdx-docs instead:',
				'https://github.com/Vercantez/open-mdx-docs',
				'',
				'Content still lives in this repo (docs.json + MDX).',
			].join('\n'),
			{
				status: 503,
				headers: { 'content-type': 'text/plain; charset=utf-8' },
			},
		);
	},
};
