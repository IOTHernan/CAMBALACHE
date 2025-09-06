import pkgutil
import importlib
import inspect

def extract_docstrings_from_module(module, prefix=""):
    docs = {}
    doc = inspect.getdoc(module)
    if doc:
        docs[prefix or module.__name__] = doc

    for name, member in inspect.getmembers(module):
        if inspect.isclass(member) or inspect.isfunction(member) or inspect.ismodule(member):
            full_name = f"{prefix}.{name}" if prefix else name
            try:
                print(f"DOC: {full_name}\n")
                docs.update(extract_docstrings_from_module(member, full_name))
            except Exception:
                # Ignorar errores de importación o introspección
                pass
    return docs

def extract_all_installed_docs():
    all_docs = {}
    for finder, name, ispkg in pkgutil.iter_modules():
        try:
            module = importlib.import_module(name)
            print(f"Modulo: {module}")
            docs = extract_docstrings_from_module(module, name)
            print(f"Docs: {docs}")
            all_docs.update(docs)
        except Exception:
            # Ignorar módulos que no carguen
            print("Ignorando modulo que no carga")
            continue
    return all_docs

def save_docs_to_md(docs, filename="all_docstrings.md"):
    with open(filename, "w", encoding="utf-8") as f:
        for name, doc in docs.items():
            print(f"Write {name} with {doc}")
            f.write(f"# {name}\n\n")
            f.write(f"{doc}\n\n---\n\n")

if __name__ == "__main__":
    print("Extrayendo docstrings de todos los paquetes instalados...")
    docs = extract_all_installed_docs()
    print(f"Documentación extraída: {len(docs)} elementos.")
    print("Guardando en all_docstrings.md ...")
    save_docs_to_md(docs)
    print("Listo.")