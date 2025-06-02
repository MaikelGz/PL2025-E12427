import ply.lex as lex
import ply.yacc as yacc

# ------------------------ Análisis Léxico ------------------------

# Definir los tokens
tokens = [
    'ID', 'NUMBER', 'STRING', 'KEYWORD', 'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'COMMA', 'COLON', 'SEMICOLON', 'DOT', 'IF', 'THEN',
    'ELSE', 'WHILE', 'DO', 'BEGIN', 'END', 'VAR', 'PROGRAM', 'FUNCTION', 'PROCEDURE', 'WRITE'
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
t_STRING = r"'([^']*)'"

# Manejo de números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Manejo de identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')  # Verifica si es una palabra clave
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejar errores léxicos
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para analizar una cadena
def analyze_lexical(code):
    lexer.input(code)
    while True:
        token = lexer.token()
        if not token:
            break
        print(token)

# ------------------------ Análisis Sintáctico ------------------------

# Gramática para el analizador sintáctico
def p_program(p):
    '''program : PROGRAM ID SEMICOLON block DOT'''
    p[0] = f"Program {p[2]}"

def p_block(p):
    '''block : declarations compound_statement'''
    p[0] = f"Declarations: {p[1]} and Statement: {p[2]}"

def p_declarations(p):
    '''declarations : VAR declarations_list'''
    p[0] = f"Variables: {p[2]}"

def p_declarations_list(p):
    '''declarations_list : ID COLON type SEMICOLON declarations_list
                         | ID COLON type SEMICOLON'''
    p[0] = f"{p[1]}: {p[3]}"

def p_type(p):
    '''type : INTEGER
            | REAL'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : BEGIN statement_list END'''
    p[0] = f"Begin {p[2]} End"

def p_statement_list(p):
    '''statement_list : statement SEMICOLON statement_list
                      | statement SEMICOLON'''
    p[0] = f"{p[1]}, {p[3]}"

def p_statement(p):
    '''statement : ID ASSIGN expression
                 | IF expression THEN statement ELSE statement
                 | WRITE LPAREN expression RPAREN'''
    if p[1] == 'write':
        p[0] = f"Output: {p[3]}"
    else:
        p[0] = f"{p[1]} assigned to {p[3]}"

def p_expression(p):
    '''expression : NUMBER
                  | ID
                  | STRING'''
    p[0] = p[1]

def p_error(p):
    print(f"Syntax error at {p.value}")

# Construir el parser
parser = yacc.yacc()

# Función para analizar el código sintácticamente
def analyze_syntactic(code):
    return parser.parse(code)

# ------------------------ Análisis Semántico ------------------------

# Verificación de semántica
def check_semantics(ast):
    variables = {}
    for stmt in ast['statements']:
        if stmt['type'] == 'assign':
            var = stmt['variable']
            if var not in variables:
                print(f"Error: Variable {var} not declared.")
            # Verificar que la asignación es correcta en términos de tipos
            if type(stmt['value']) != variables[var]:
                print(f"Type mismatch for variable {var}.")

# ------------------------ Generación de Código ------------------------

# Generar código intermedio
def generate_code(ast):
    code = []
    for stmt in ast['statements']:
        if stmt['type'] == 'assign':
            code.append(f"STORE {stmt['variable']} = {stmt['value']}")
        elif stmt['type'] == 'print':
            code.append(f"PRINT {stmt['value']}")
    return code

# ------------------------ Función Principal ------------------------

def main(code):
    # Análisis Léxico
    print("Análisis Léxico:")
    analyze_lexical(code)

    # Análisis Sintáctico
    print("\nAnálisis Sintáctico:")
    ast = analyze_syntactic(code)
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
