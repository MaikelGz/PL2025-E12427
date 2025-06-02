import ply.lex as lex
import ply.yacc as yacc

# ------------------------ Análisis Léxico ------------------------

# Definir los tokens
tokens = [
    'ID', 'NUMBER', 'STRING', 'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'COMMA', 'COLON', 'SEMICOLON', 'DOT', 'IF', 'THEN',
    'ELSE', 'WHILE', 'DO', 'BEGIN', 'END', 'VAR', 'PROGRAM', 'FUNCTION', 'PROCEDURE', 'WRITE',
    'INTEGER', 'REAL'
]

# Palabras clave
keywords = {
    'if': 'IF', 'then': 'THEN', 'else': 'ELSE', 'while': 'WHILE', 'do': 'DO',
    'begin': 'BEGIN', 'end': 'END', 'var': 'VAR', 'program': 'PROGRAM',
    'function': 'FUNCTION', 'procedure': 'PROCEDURE', 'writeln': 'WRITE'
}

# Expresiones regulares para los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_STRING = r'"([^"]*)"'

# Tokens de tipo
t_INTEGER = r'integer'
t_REAL = r'real'

# Manejo de números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Manejo de identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')  # Verifica si es una palabra clave
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejar errores léxicos
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# ------------------------ Análisis Sintáctico ------------------------

# Gramática para el analizador sintáctico
def p_program(p):
    '''program : PROGRAM ID SEMICOLON block DOT'''
    p[0] = {'type': 'program', 'name': p[2], 'block': p[4]}

def p_block(p):
    '''block : declarations compound_statement'''
    p[0] = {'type': 'block', 'declarations': p[1], 'statements': p[2]}

def p_declarations(p):
    '''declarations : VAR declarations_list'''
    p[0] = p[2]

def p_declarations_list(p):
    '''declarations_list : ID COLON type SEMICOLON declarations_list
                         | ID COLON type SEMICOLON'''
    p[0] = {'name': p[1], 'type': p[3]}

def p_type(p):
    '''type : INTEGER
            | REAL'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : BEGIN statement_list END'''
    p[0] = {'type': 'compound', 'statements': p[2]}

def p_statement_list(p):
    '''statement_list : statement SEMICOLON statement_list
                      | statement SEMICOLON'''
    p[0] = [p[1]] + (p[3] if len(p) > 3 else [])

def p_statement(p):
    '''statement : ID ASSIGN expression
                 | IF expression THEN statement ELSE statement
                 | WRITE LPAREN expression RPAREN'''
    if p[1] == 'write':
        p[0] = {'type': 'print', 'value': p[3]}
    else:
        p[0] = {'type': 'assign', 'variable': p[1], 'value': p[3]}

def p_expression(p):
    '''expression : NUMBER
                  | ID
                  | STRING'''
    p[0] = p[1]

def p_error(p):
    print(f"Syntax error at {p.value}")

# Construir el parser
parser = yacc.yacc()

# ------------------------ Análisis Semántico ------------------------

# Verificación de semántica
def check_semantics(ast):
    if ast is None:
        return
    
    variables = {}
    
    if 'declarations' in ast:
        for var in ast['declarations']:
            variables[var['name']] = var['type']
    
    if 'statements' in ast:
        for stmt in ast['statements']:
            if stmt['type'] == 'assign':
                var = stmt['variable']
                if var not in variables:
                    print(f"Error: Variable {var} not declared.")
                # Verificar que la asignación es correcta en términos de tipos
                if stmt['value'] != variables[var]:
                    print(f"Type mismatch for variable {var}.")
            elif stmt['type'] == 'print':
                # Verificación simple de tipo de impresión
                if not isinstance(stmt['value'], str) and not isinstance(stmt['value'], int):
                    print(f"Error: Cannot print value of type {type(stmt['value'])}.")

# ------------------------ Generación de Código ------------------------

# Generar código intermedio
def generate_code(ast):
    code = []
    if 'statements' in ast:
        for stmt in ast['statements']:
            if stmt['type'] == 'assign':
                code.append(f"STORE {stmt['variable']} = {stmt['value']}")
            elif stmt['type'] == 'print':
                code.append(f"PRINT {stmt['value']}")
    return code

# ------------------------ Función Principal ------------------------

def analyze_lexical(code):
    lexer.input(code)
    while True:
        token = lexer.token()
        if not token:
            break
        print(token)

def analyze_syntactic(code):
    return parser.parse(code)

def main(code):
    # Análisis Léxico
    print("Análisis Léxico:")
    analyze_lexical(code)

    # Análisis Sintáctico
    print("\nAnálisis Sintáctico:")
    ast = analyze_syntactic(code)
    if ast is None:
        print("Syntax error, unable to generate AST.")
    else:
        print(ast)

        # Análisis Semántico
        print("\nAnálisis Semántico:")
        check_semantics(ast)

        # Generación de código
        print("\nGeneración de Código:")
        generated_code = generate_code(ast)
        for line in generated_code:
            print(line)

# Código de ejemplo
code = """
program HolaMundo;
begin
    writeln('Hola Mundo!');
end.
"""

main(code)

