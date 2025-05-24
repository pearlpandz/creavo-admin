import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

// Recreate __dirname for ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const distDir = path.join(__dirname, 'dist');
const djangoTemplatesDir = path.join(__dirname, '..', 'templates');
const djangoStaticDir = path.join(__dirname, '..', 'static');

// Helper: Clean a directory except specified subfolder(s)
function cleanDirExcept(dirPath, exceptions = []) {
  const entries = fs.readdirSync(dirPath);
  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry);
    const isException = exceptions.some((ex) => fullPath.startsWith(path.join(dirPath, ex)));

    if (!isException) {
      fs.removeSync(fullPath); // delete file or directory
    }
  }
}

// Clean templates except 'admin'
console.log('🧹 Cleaning templates (except templates/admin)...');
cleanDirExcept(djangoTemplatesDir, ['admin']);

// Clean static normally
console.log('🧹 Cleaning static folder...');
fs.emptyDirSync(djangoStaticDir);

// Read index.html content
let indexHtml = fs.readFileSync(path.join(distDir, 'index.html'), 'utf-8');

// Inject {% load static %} at the top
indexHtml = `{% load static %}\n` + indexHtml;

// Replace src="/assets/..." ➔ src="{% static 'assets/...' %}"
indexHtml = indexHtml.replace(/src="\/assets\//g, `src="{% static 'assets/`);
indexHtml = indexHtml.replace(/href="\/assets\//g, `href="{% static 'assets/`);

// Close the Django static template tag
indexHtml = indexHtml.replace(/\.js"/g, `.js' %}"`);
indexHtml = indexHtml.replace(/\.css"/g, `.css' %}"`);

// Write the modified index.html into templates
console.log('📄 Writing modified index.html to Django templates...');
fs.writeFileSync(path.join(djangoTemplatesDir, 'index.html'), indexHtml, 'utf-8');

// Copy assets ➝ static
console.log('📁 Copying assets to Django static...');
fs.copySync(path.join(distDir, 'assets'), path.join(djangoStaticDir, 'assets'));

console.log('✅ Postbuild complete!');
