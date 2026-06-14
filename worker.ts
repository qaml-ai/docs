type Env = {
  MINTLIFY_HOST?: string;
  CUSTOM_HOST?: string;
};

const DEFAULT_MINTLIFY_HOST = "camelai.mintlify.dev";
const DEFAULT_CUSTOM_HOST = "camelai.com";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname.startsWith("/.well-known/")) {
      return fetch(request);
    }

    if (!url.pathname.startsWith("/docs")) {
      return fetch(request);
    }

    const mintlifyHost = env.MINTLIFY_HOST ?? DEFAULT_MINTLIFY_HOST;
    const customHost = env.CUSTOM_HOST ?? DEFAULT_CUSTOM_HOST;
    const proxyUrl = new URL(request.url);
    proxyUrl.hostname = mintlifyHost;

    const proxyRequest = new Request(proxyUrl, request);
    proxyRequest.headers.set("Host", mintlifyHost);
    proxyRequest.headers.set("X-Forwarded-Host", customHost);
    proxyRequest.headers.set("X-Forwarded-Proto", "https");

    const connectingIp = request.headers.get("CF-Connecting-IP");
    if (connectingIp) {
      proxyRequest.headers.set("CF-Connecting-IP", connectingIp);
    }

    return fetch(proxyRequest);
  }
};
