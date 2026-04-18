/**
 * Request indexing via Google Search Console API (Indexing API)
 * Submits each new blog URL to Google's indexing queue.
 *
 * Requires GSC_SERVICE_ACCOUNT_JSON secret (service account credentials).
 * The service account must be added as an owner in GSC for zeniapartners.com.
 */

const { google } = require('googleapis');
const { execSync } = require('child_process');

async function main() {
  const credentials = JSON.parse(process.env.GSC_SERVICE_ACCOUNT_JSON);

  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: ['https://www.googleapis.com/auth/indexing']
  });

  const authClient = await auth.getClient();
  const indexing = google.indexing({ version: 'v3', auth: authClient });

  // Get new blog files from last commit
  const diff = execSync('git diff --name-only --diff-filter=A HEAD~1 HEAD', { encoding: 'utf-8' });
  const newFiles = diff.split('\n').filter(f => /^blog\/[^/]+\.html$/.test(f) && f !== 'blog/index.html');

  if (newFiles.length === 0) {
    console.log('No new blog posts to submit.');
    return;
  }

  console.log(`Submitting ${newFiles.length} URL(s) to GSC Indexing API:`);

  for (const file of newFiles) {
    const url = `https://zeniapartners.com/${file}`;
    try {
      const res = await indexing.urlNotifications.publish({
        requestBody: {
          url,
          type: 'URL_UPDATED'
        }
      });
      console.log(`  ✓ ${url} submitted: ${res.data.urlNotificationMetadata?.url || 'ok'}`);
    } catch (e) {
      console.error(`  ✗ ${url} error: ${e.message}`);
    }
  }
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
