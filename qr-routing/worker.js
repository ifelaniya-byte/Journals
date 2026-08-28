/*
 * Buyer-controlled redirect reference for go.<your-domain>.
 *
 * Deploy this only after the business owns the domain. Bind the Worker to
 * go.<your-domain>/* and set LANDING_ORIGIN (e.g. https://www.example.com).
 * Keep the external printed URL on the owned go subdomain even if the
 * destination hosting provider changes.
 */
const ROUTES = {
  '/arrive':  '/listen/arrive/',
  '/soften':  '/listen/soften/',
  '/harbor':  '/listen/harbor/',
  '/settle':  '/listen/settle/',
  '/enough':  '/listen/enough/',
  '/clarity': '/listen/clarity/'
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const destination = ROUTES[url.pathname];
    if (!destination) return new Response('Not found.', { status: 404 });
    const origin = (env.LANDING_ORIGIN || '').replace(/\/$/, '');
    if (!/^https:\/\//.test(origin)) {
      return new Response('Redirect is not configured.', { status: 503 });
    }
    return Response.redirect(origin + destination, 302);
  }
};
