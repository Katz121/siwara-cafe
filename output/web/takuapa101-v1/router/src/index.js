/* Puts the Pages deployment on the main domain.
   siwaracafe.com/takuapa/*      -> the Pages site
   siwaracafe.com/takuapa/api/*  -> the news Worker, same origin so no CORS */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const base = env.BASE_PATH || '/takuapa';

    if (url.pathname === base) {
      return Response.redirect(url.origin + base + '/', 301);
    }
    if (!url.pathname.startsWith(base + '/')) {
      return new Response('ไม่พบหน้านี้', { status: 404 });
    }

    const rest = url.pathname.slice(base.length) || '/';

    // News API is served from the same origin as the site.
    if (rest.startsWith('/api/')) {
      const target = new URL(env.NEWS_WORKER);
      target.pathname = rest;
      target.search = url.search;
      const upstream = await fetch(target.toString(), {
        method: request.method,
        headers: { 'User-Agent': 'takuapa101-router/1.0' },
      });
      const headers = new Headers(upstream.headers);
      headers.delete('access-control-allow-origin');
      return new Response(upstream.body, { status: upstream.status, headers });
    }

    // Everything else comes from Pages. The site is built with /takuapa in its
    // links, so the prefix is stripped before asking Pages for the file.
    const target = new URL(env.PAGES_ORIGIN);
    target.pathname = rest;
    target.search = url.search;

    const upstream = await fetch(target.toString(), {
      method: request.method,
      headers: request.headers,
      redirect: 'manual',
    });

    const headers = new Headers(upstream.headers);
    // Pages may redirect to a path without the prefix; put it back.
    const loc = headers.get('location');
    if (loc && loc.startsWith('/') && !loc.startsWith(base + '/')) {
      headers.set('location', base + loc);
    }
    headers.set('x-served-by', 'takuapa101-router');
    return new Response(upstream.body, { status: upstream.status, headers });
  },
};
