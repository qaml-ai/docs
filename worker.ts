/**
 * Not used. Production is deployed via:
 *   bun run deploy
 * which runs open-mdx-docs (see DEPLOY.md).
 */
export default {
  async fetch() {
    return new Response('Use: bun run deploy (open-mdx-docs)\n', { status: 503 });
  },
};
