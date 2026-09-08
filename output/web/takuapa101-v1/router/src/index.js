/* siwaracafe.com/takuapa/* -> takuapa101.com
 *
 * The guide moved to its own domain. Anyone who saved or shared the old path
 * still lands on the right page, and a 301 tells search engines to move the
 * ranking across rather than treat the two as duplicates.
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const base = env.BASE_PATH || '/takuapa';
    const target = (env.SITE_ORIGIN || 'https://takuapa101.com').replace(/\/$/, '');

    if (!url.pathname.startsWith(base)) {
      return new Response('ไม่พบหน้านี้', { status: 404 });
    }

    // /takuapa -> /, /takuapa/places/ -> /places/
    const rest = url.pathname.slice(base.length) || '/';
    const dest = target + (rest.startsWith('/') ? rest : '/' + rest) + url.search;

    return new Response(null, {
      status: 301,
      headers: {
        Location: dest,
        'Cache-Control': 'public, max-age=3600',
        'x-moved-by': 'takuapa101-router',
      },
    });
  },
};
