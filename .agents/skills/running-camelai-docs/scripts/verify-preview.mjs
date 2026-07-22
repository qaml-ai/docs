const requestedUrl =
	process.argv[2] ??
	`http://localhost:${process.env.CONDUCTOR_PORT || '3000'}/docs/`;

async function fetchOk(url, label) {
	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`${label} returned HTTP ${response.status}: ${response.url}`);
	}
	return response;
}

const page = await fetchOk(requestedUrl, 'Docs page');
const html = await page.text();

if (!new URL(page.url).pathname.startsWith('/docs/')) {
	throw new Error(`Preview escaped the /docs/ base path: ${page.url}`);
}

if (!/<title>[^<]*camelAI Documentation<\/title>/.test(html)) {
	throw new Error('Preview did not render the camelAI Documentation title.');
}

const clientPath = html.match(
	/<link[^>]+href="([^"]*entry\.client\.tsx[^"]*)"[^>]*>/,
)?.[1];
const criticalCssPath = html.match(
	/<link[^>]+data-react-router-critical-css=""[^>]+href="([^"]+)"[^>]*>/,
)?.[1];

if (!clientPath || !criticalCssPath) {
	throw new Error('Preview HTML is missing expected React Router client assets.');
}

const client = await fetchOk(new URL(clientPath, page.url), 'Client entry module');
const criticalCss = await fetchOk(
	new URL(criticalCssPath.replaceAll('&amp;', '&'), page.url),
	'Critical CSS',
);

console.log(`Verified camelAI docs preview: ${page.url}`);
console.log(
	`HTTP ${page.status} page, ${client.status} client entry, ${criticalCss.status} critical CSS.`,
);
