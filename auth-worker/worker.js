const CLIENT_ID = 'DEIN_GITHUB_CLIENT_ID';
const CLIENT_SECRET = 'DEIN_GITHUB_CLIENT_SECRET';
const ORIGIN = 'https://naddis-keramik.pages.dev';

export default {
  async fetch(request) {
    const url = new URL(request.url);

    const corsHeaders = {
      'Access-Control-Allow-Origin': ORIGIN,
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Schritt 1: Weiterleitung zu GitHub
    if (url.pathname === '/auth') {
      const params = new URLSearchParams({
        client_id: CLIENT_ID,
        scope: 'repo,user',
      });
      return Response.redirect(
        `https://github.com/login/oauth/authorize?${params}`,
        302
      );
    }

    // Schritt 2: Callback — Code gegen Token tauschen
    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');

      if (!code) {
        return new Response('Kein Code erhalten', { status: 400 });
      }

      try {
        const tokenRes = await fetch(
          'https://github.com/login/oauth/access_token',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Accept: 'application/json',
            },
            body: JSON.stringify({
              client_id: CLIENT_ID,
              client_secret: CLIENT_SECRET,
              code: code,
            }),
          }
        );

        const tokenData = await tokenRes.json();
        const token = tokenData.access_token;

        if (!token) {
          const errHtml = renderMessage('error', 'github', 
            'Kein Token erhalten: ' + JSON.stringify(tokenData));
          return new Response(errHtml, {
            headers: { 'Content-Type': 'text/html', ...corsHeaders },
          });
        }

        const successHtml = renderMessage('success', 'github', token);
        return new Response(successHtml, {
          headers: { 'Content-Type': 'text/html', ...corsHeaders },
        });

      } catch (err) {
        const errHtml = renderMessage('error', 'github', err.message);
        return new Response(errHtml, {
          status: 500,
          headers: { 'Content-Type': 'text/html', ...corsHeaders },
        });
      }
    }

    return new Response('Not found', { status: 404 });
  },
};

function renderMessage(status, provider, content) {
  const message = status === 'success'
    ? JSON.stringify({ token: content, provider: provider })
    : content;

  return `<!DOCTYPE html>
<html>
<head><title>Authenticating...</title></head>
<body>
<p>Authentifizierung läuft...</p>
<script>
  (function() {
    function receiveMessage() {
      var data = 'authorization:${provider}:${status}:' + ${
        status === 'success'
          ? 'JSON.stringify({ token: "' + content + '", provider: "' + provider + '" })'
          : '"' + content + '"'
      };
      if (window.opener) {
        window.opener.postMessage(data, '${ORIGIN}');
        setTimeout(function() { window.close(); }, 500);
      }
    }
    window.addEventListener('load', receiveMessage);
  })();
</script>
</body>
</html>`;
}
