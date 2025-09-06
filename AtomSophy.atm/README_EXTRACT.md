## Comandos especiales para scraping

- `html2json archivo.html salida.json`  
  Convierte un HTML a estructura JSON navegable.

- `json2blocks archivo.json pre code`  
  Extrae y muestra el texto de todos los bloques `<pre>` y `<code>` del JSON.

Ejemplo de uso:
```bash
python cli.py html2json pagina.html dom.json
python cli.py json2blocks dom.json pre code
```