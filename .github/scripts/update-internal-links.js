/**
 * Aggressive internal linking.
 * For each new blog post, find 2-3 existing posts in the same cluster (vertical)
 * and append a link to the new post in their "Artículos relacionados" section.
 *
 * Runs automatically after each push that adds a new post.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BLOG_DIR = 'blog';
const TRACKER_PATH = 'blog/content-tracker.json';

// Detect cluster from slug/content
function detectCluster(slug, htmlContent) {
  const clusters = {
    gimnasios: ['gimnasio', 'fitness', 'gym', 'socios', 'retencion'],
    restaurantes: ['restaurante', 'reservas', 'gastro', 'hosteleria'],
    belleza: ['belleza', 'estetica', 'peluqueria', 'salon', 'unas'],
    retail: ['retail', 'tienda'],
    ecommerce: ['ecommerce', 'carritos', 'online', 'tienda-online'],
    wellness: ['wellness', 'spa', 'clinica', 'pacientes'],
    'servicios-profesionales': ['abogado', 'inmobiliaria', 'consultoria', 'academia']
  };

  const haystack = (slug + ' ' + htmlContent.substring(0, 3000)).toLowerCase();

  for (const [cluster, keywords] of Object.entries(clusters)) {
    if (keywords.some(kw => haystack.includes(kw))) {
      return cluster;
    }
  }
  return 'general';
}

// Extract H1 text from HTML (for link text)
function extractH1(html) {
  const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (!m) return null;
  // Strip nested tags like <span class="text-gradient">
  return m[1].replace(/<[^>]+>/g, '').trim();
}

// Extract short description from lead paragraph
function extractLead(html) {
  const m = html.match(/<p class="lead"[^>]*>([\s\S]*?)<\/p>/i);
  if (!m) return '';
  const text = m[1].replace(/<[^>]+>/g, '').trim();
  return text.substring(0, 100) + (text.length > 100 ? '...' : '');
}

function main() {
  // Get new blog files from last commit
  let newFiles;
  try {
    const diff = execSync('git diff --name-only --diff-filter=A HEAD~1 HEAD', { encoding: 'utf-8' });
    newFiles = diff.split('\n').filter(f => /^blog\/[^/]+\.html$/.test(f) && f !== 'blog/index.html');
  } catch (e) {
    console.log('Could not determine new files:', e.message);
    return;
  }

  if (newFiles.length === 0) {
    console.log('No new blog posts. Skipping internal linking.');
    return;
  }

  // For each new post, update related existing posts
  for (const newFile of newFiles) {
    const newSlug = path.basename(newFile, '.html');
    const newPath = newFile;
    const newHtml = fs.readFileSync(newPath, 'utf-8');

    const cluster = detectCluster(newSlug, newHtml);
    const newH1 = extractH1(newHtml);
    const newLead = extractLead(newHtml);
    const newUrl = `/${newFile}`;

    console.log(`\nNew post: ${newSlug} (cluster: ${cluster})`);

    if (!newH1) {
      console.log('  Could not extract H1. Skipping.');
      continue;
    }

    // Find existing posts in same cluster
    const existingFiles = fs.readdirSync(BLOG_DIR)
      .filter(f => f.endsWith('.html') && f !== 'index.html' && f !== path.basename(newFile))
      .map(f => path.join(BLOG_DIR, f));

    const candidates = [];
    for (const file of existingFiles) {
      try {
        const html = fs.readFileSync(file, 'utf-8');
        const fileCluster = detectCluster(path.basename(file, '.html'), html);
        if (fileCluster === cluster) {
          candidates.push({ file, html });
        }
      } catch (e) { /* skip */ }
    }

    // Pick 2-3 random candidates to update (to avoid always hitting the same)
    const shuffled = candidates.sort(() => Math.random() - 0.5);
    const toUpdate = shuffled.slice(0, 3);

    console.log(`  Updating ${toUpdate.length} related post(s):`);

    for (const { file, html } of toUpdate) {
      // Look for "Artículos relacionados" or blog-related section
      const relatedRegex = /(<div[^>]*class="blog-related"[^>]*>[\s\S]*?<h3[^>]*>[^<]*<\/h3>)([\s\S]*?)(<\/div>)/i;
      const match = html.match(relatedRegex);

      if (!match) {
        // No related section exists. Skip (don't inject, respect template).
        console.log(`    SKIP ${path.basename(file)} (no blog-related section)`);
        continue;
      }

      // Check if this post already links to the new post
      if (html.includes(newUrl)) {
        console.log(`    SKIP ${path.basename(file)} (already links to new post)`);
        continue;
      }

      // Count existing links in related section
      const relatedContent = match[2];
      const existingLinkCount = (relatedContent.match(/<a\s+href=/gi) || []).length;

      // Build new link entry (matching blog-related style)
      const newLink = `\n      <a href="${newUrl}">${newH1}<span>${newLead}</span></a>`;

      let updatedRelated;
      if (existingLinkCount >= 4) {
        // Remove the last link, add the new one at top
        updatedRelated = relatedContent.replace(/<a[^>]+>[\s\S]*?<\/a>\s*$/, '');
        updatedRelated = newLink + updatedRelated;
      } else {
        // Append new link at the top
        updatedRelated = newLink + relatedContent;
      }

      const newHtmlContent = html.replace(relatedRegex, `$1${updatedRelated}$3`);
      fs.writeFileSync(file, newHtmlContent);
      console.log(`    ✓ ${path.basename(file)}`);
    }
  }

  console.log('\nInternal linking update complete.');
}

main();
