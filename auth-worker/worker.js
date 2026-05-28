// Decap CMS Auth Worker für Cloudflare
// Basiert auf: https://github.com/sterlingwes/netlify-cms-github-oauth-provider
// Ersetze CLIENT_ID und CLIENT_SECRET mit deinen GitHub OAuth App Werten

const CLIENT_ID = 'DEIN_GITHUB_CLIENT_ID';
const CLIENT_SECRET = 'DEIN_GITHUB_CLIENT_SECRET';
const ORIGIN = 'https://DEINE-SEITE.pages.dev'; // deine Cloudflare Pages URL

export default {
  async fetch(request) {
    const url = new URL(request.url);

    // CORS
    const corsHeaders = {
      'Access-Control-Allow-Origin': ORIGIN,
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Schritt 1: Browser → GitHub weiterleiten
    if (url.pathname === '/auth') {
      const params = new URLSearchParams({
        client_id: CLIENT_ID,
        scope: 'repo,user',
        state: crypto.randomUUID(),
      });
      return Response.redirect(
        `https://github.com/login/oauth/authorize?${params}`,
        302
      );
    }

    // Schritt 2: GitHub → Token tauschen
    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');
      if (!code) {
        return new Response('Kein Code erhalten', { status: 400 });
      }

      const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          client_id: CLIENT_ID,
          client_secret: CLIENT_SECRET,
          code,
        }),
      });

      const { access_token, error } = await tokenRes.json();

      if (error || !access_token) {
        return new Response(`Auth Fehler: ${error}`, { status: 400 });
      }

      // Token an CMS zurückgeben via postMessage
      const html = `<!DOCTYPE html>
<html>
<body>
<script>
  window.opener.postMessage(
    'authorization:github:success:${JSON.stringify({ token: access_token, provider: 'github' })}',
    '${ORIGIN}'
  );
  window.close();
</script>
</body>
</html>`;

      return new Response(html, {
        headers: { 'Content-Type': 'text/html', ...corsHeaders },
      });
    }

    return new Response('Nicht gefunden', { status: 404 });
  },
};
