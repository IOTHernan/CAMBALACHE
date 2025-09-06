import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

# --- Léxico (Lexer) ---
KEYWORDS = {
    'load', 'open', 'read', 'write', 'play', 'stop',
    'analyze', 'map', 'route', 'link', 'exec',
    'crush', 'extract', 'parse', 'mount', 'scan'
}

DATATYPES = {
    'video', 'audio', 'text', 'img', 'binary', 'map', 'memory', 'struct'
}

OPERATORS = {
    ':', '->', '=', '+', '-', '*', '/', '(', ')', '[', ']', '{', '}'
}

FILE_EXTENSIONS = r'\.(atm|ogg|amr|avi|3gp|img|vlc|mp3|wav|lisp|json|bin)'

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
        # Aquí se puede mapear a funciones reales o llamadas del sistema


# --- Ejemplo de prueba ---
if __name__ == "__main__":
    code = '''
    #atm.version: 0.1
    #atm.author: Comandante
    #atm.arch: x64
    #atm.mode: offline

    load :video @media/intro.avi
    parse :text @log.lisp
    exec -> memory [2048]
    '''
    tokens, metadata = lex_atm_code(code)
    ast = parse_tokens(tokens)
    execute_ast(ast, metadata)
