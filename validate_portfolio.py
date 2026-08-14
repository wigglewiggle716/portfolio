from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent
html_files = sorted(root.glob('*.html'))
errors = []
summary = []
for path in html_files:
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    if not soup.find('html', attrs={'lang': True}):
        errors.append(f'{path.name}: missing html lang')
    if not soup.find('meta', attrs={'name': 'viewport'}):
        errors.append(f'{path.name}: missing viewport')
    if not soup.title or not soup.title.get_text(strip=True):
        errors.append(f'{path.name}: missing title')
    for img in soup.find_all('img'):
        if img.get('alt') is None:
            errors.append(f'{path.name}: image missing alt')
    for anchor in soup.find_all('a', href=True):
        href = anchor['href'].split('#', 1)[0].split('?', 1)[0]
        if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:')):
            target = (path.parent / href).resolve()
            if not target.exists():
                errors.append(f'{path.name}: broken local link -> {href}')
    summary.append((path.name, len(soup.find_all('img')), len(soup.find_all('a', href=True))))

print(f'checked={len(html_files)}')
for name, images, links in summary:
    print(f'{name}: images={images}, links={links}')
if errors:
    print('ERRORS:')
    print('\n'.join(errors))
    raise SystemExit(1)
print('validation=PASS')
