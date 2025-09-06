from bs4 import BeautifulSoup

html = '<html><body><a href="https://example.com">link</a></body></html>'
soup = BeautifulSoup(html, 'html.parser')
for a in soup.find_all('a', href=True):
    print(type(a))
    print(a['href']) # type: ignore
