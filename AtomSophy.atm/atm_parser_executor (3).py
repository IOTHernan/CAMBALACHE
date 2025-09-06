import re
from collections import namedtuple
import os
from urllib.parse import urlparse

Token = namedtuple('Token', ['type', 'value'])

# --- Léxico (Lexer) ---
KEYWORDS = {
    'load', 'open', 'read', 'write', 'play', 'stop',
    'analyze', 'map', 'route', 'link', 'exec',
    'crush', 'extract', 'parse', 'mount', 'scan'
}

DATATYPES = {
    'video', 'audio', 'text', 'img', 'binary', 'map', 'memory', 'struct', 'header'
}

OPERATORS = {
    ':', '->', '=', '+', '-', '*', '/', '(', ')', '[', ']', '{', '}'
}

FILE_EXTENSIONS = r'\.(atm|ogg|amr|avi|3gp|img|vlc|mp3|wav|lisp|json|bin|msg|xml)'

TOKEN_REGEX = [
    ('HEADER',   r'#\w+\s*:\s*[^\n]+'),
    ('NUMBER',   r'\b\d+(\.\d+)?\b'),
    ('COMMAND',  r'\b(?:' + '|'.join(KEYWORDS) + r')\b'),
    ('TYPE',     r'\b(?:' + '|'.join(DATATYPES) + r')\b'),
    ('REF',      r'@[\w/\.\-:]+'),
    ('ID',       r'[a-zA-Z_][\w\-]*'),
    ('OP',       r'[:=\->\+\*/\(\)\[\]\{\}]'),
    ('STRING',   r'"[^"]*"'),
    ('FILE',     FILE_EXTENSIONS),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
    ('MISMATCH', r'.'),
]

master_pattern = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_REGEX))

def lex_atm_code(code):
    tokens = []
    metadata = {}
    for mo in master_pattern.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP' or kind == 'NEWLINE':
            continue
        elif kind == 'HEADER':
            key, val = value[1:].split(':', 1)
            metadata[key.strip()] = val.strip()
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Token inesperado: {value}')
        else:
            tokens.append(Token(kind, value))
    return tokens, metadata

# --- Parser simplificado (AST builder) ---
class ASTNode:
    def __init__(self, command, args):
        self.command = command
        self.args = args

    def __repr__(self):
        return f"{self.command}({', '.join(map(str, self.args))})"


def parse_tokens(tokens):
    ast = []
    i = 0
    while i < len(tokens):
        if tokens[i].type == 'COMMAND':
            command = tokens[i].value
            args = []
            i += 1
            while i < len(tokens) and tokens[i].type not in ['COMMAND']:
                if tokens[i].type in {'STRING', 'ID', 'NUMBER', 'TYPE', 'FILE', 'REF'}:
                    args.append(tokens[i].value)
                elif tokens[i].type == 'OP' and tokens[i].value in {':', '=', '->'}:
                    args.append(tokens[i].value)
                i += 1
            ast.append(ASTNode(command, args))
        else:
            i += 1
    return ast

# --- Diccionario de firmas de cabeceras binarios ---
headers_dict = {
    b'\xFF\xD8\xFF': 'jpeg',
    b'\x89PNG\r\n\x1a\n': 'png',
    b'RIFF': 'wav/avi',
    b'OggS': 'ogg',
    b'\x1A\x45\xDF\xA3': 'mkv',
    b'fLaC': 'flac',
    b'PK\x03\x04': 'zip',
    b'Rar!\x1A\x07\x00': 'rar',
    b'\x00\x00\x01\xBA': 'mpeg',
    b'\x42\x5A\x68': 'bzip2',
    b'\x7FELF': 'elf',
    b'MZ': 'exe/dll',
    b'<msg': 'outlook_msg_xml',
    b'<?xml': 'xml'
}

def detect_format(filepath, headers=headers_dict):
    try:
        if filepath.startswith('http://') or filepath.startswith('https://'):
            return 'url'
        with open(filepath, 'rb') as f:
            file_head = f.read(16)
            for signature, fmt in headers.items():
                if file_head.startswith(signature):
                    return fmt
    except Exception as e:
        return f"error: {e}"
    return 'unknown'


def classify_reference(ref):
    if ref.startswith('http://') or ref.startswith('https://'):
        return 'url'
    elif any(ref.endswith(ext) for ext in ['.mp3', '.mp4', '.avi', '.ogg', '.wav', '.3gp']):
        return 'media'
    elif any(ref.endswith(ext) for ext in ['.jpg', '.png', '.jpeg', '.bmp']):
        return 'image'
    elif any(ref.endswith(ext) for ext in ['.msg', '.xml', '.json']):
        return 'structured_text'
    elif os.path.isfile(ref):
        return detect_format(ref)
    else:
        return 'unknown'

# --- Motor de ejecución simbólica (stub) ---
def execute_ast(ast, metadata):
    print("[.atm] Metadatos detectados:")
    for key, val in metadata.items():
        print(f"  - {key}: {val}")

    print("\n[.atm] Ejecutando comandos:")
    for node in ast:
        print(f"[.atm] Ejecutando: {node.command}")
        for arg in node.args:
            print(f"  \u2514 Argumento: {arg}")
            if arg.startswith('@'):
                ref = arg[1:]
                tipo = classify_reference(ref)
                print(f"    \u2192 Tipo detectado: {tipo}")

        # Implementación especial para análisis de cabecera
        if node.command == 'analyze' and ':header' in node.args:
            for a in node.args:
                if a.startswith('@'):
                    path = a[1:]
                    fmt = detect_format(path)
                    print(f"    \u2192 Formato detectado: {fmt}")

# --- Ejemplo de prueba ---
if __name__ == "__main__":
    code = '''
    #atm.version: 0.3
    #atm.author: Comandante
    #atm.arch: x64
    #atm.mode: offline

    analyze :header @test_files/facebook_data.msg
    analyze :header @https://media.fbcdn.com/video123.3gp
    analyze :header @totalrecall.dump.avi
    '''
    tokens, metadata = lex_atm_code(code)
    ast = parse_tokens(tokens)
    execute_ast(ast, metadata)
