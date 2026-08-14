from pathlib import Path
import re

ROOT = Path(__file__).parent
html_files = sorted(ROOT.glob("*.html"))

for path in html_files:
    text = path.read_text(encoding="utf-8")
    if '<meta name="viewport"' not in text:
        marker = '<meta charset="utf-8"/>'
        if marker in text:
            text = text.replace(marker, marker + '\n<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n<meta name="theme-color" content="#FAF9F5"/>', 1)
        else:
            text = text.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n<meta name="theme-color" content="#FAF9F5"/>', 1)

    image_count = [0]
    def improve_image(match):
        image_count[0] += 1
        attributes = match.group(1)
        # Keep the first image eager for the initial visual; defer the rest.
        if image_count[0] > 1 and 'loading=' not in attributes:
            attributes += ' loading="lazy"'
        if 'decoding=' not in attributes:
            attributes += ' decoding="async"'
        return '<img' + attributes + '>'

    text = re.sub(r'<img\b([^>]*)>', improve_image, text, flags=re.IGNORECASE)

    # External links opened in a new tab should not retain the opener reference.
    text = re.sub(r'<a\b([^>]*target="_blank"[^>]*)(?<!rel="noopener")>', lambda m: ('<a' + m.group(1) + (' rel="noopener"' if 'rel=' not in m.group(1) else '') + '>'), text, flags=re.IGNORECASE)
    path.write_text(text, encoding="utf-8")

print(f"Updated {len(html_files)} HTML files for viewport, image loading and external-link safety")
