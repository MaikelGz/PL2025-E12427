import ply.lex as lex
import ply.yacc as yacc

# ---- Análisis Léxico ----

reserved = {
    'program': 'PROGRAM', 'var': 'VAR', 'integer': 'INTEGER',
    'begin': 'BEGIN', 'end': 'END', 'writeln': 'WRITELN',
    'write': 'WRITE', 'readln': 'READLN', 'if': 'IF',
    'then': 'THEN', 'else': 'ELSE', 'for': 'FOR', 'to': 'TO',
    'do': 'DO', 'while': 'WHILE', 'div': 'DIV', 'mod': 'MOD',
    'array': 'ARRAY', 'of': 'OF', 'boolean': 'BOOLEAN',
    'and': 'AND', 'or': 'OR', 'true': 'TRUE', 'false': 'FALSE'  # Added TRUE and FALSE
}

tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIVIDE',
    'LPAREN', 'RPAREN', 'SEMI', 'COLON', 'COMMA',
    'DOTDOT',   # DOTDOT debe ir antes que DOT
    'DOT',
    'ASSIGN', 'STRING', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
    'LSQUARE', 'RSQUARE', 'TRUE', 'FALSE'  # Added tokens for TRUE and FALSE
] + list(reserved.values())

t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_DOTDOT = r'\.\.'
t_DOT = r'\.'
t_ASSIGN = r':='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'='
t_NE = r'<>'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'

def t_STRING(t):
    r'\'[^\']*\''
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

symbol_table = {}
symbol_counter = 0

def register_variable(name):
    global symbol_counter
    if name not in symbol_table:
        symbol_table[name] = symbol_counter
        symbol_counter += 1
    return symbol_table[name]

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'DIV', 'MOD'),
)

start = 'program'

def p_program(p):
    'program : PROGRAM ID SEMI block DOT'
    p[0] = ('program', p[2], p[4])

def p_block_with_decls(p):
    'block : declarations BEGIN statements END'
    p[0] = ('block', p[1], p[3])

def p_block_no_decls(p):
    'block : BEGIN statements END'
    p[0] = ('block', None, p[2])

def p_statement_block(p):
    'statement : block'
    p[0] = p[1]

def p_declarations(p):
    '''declarations : VAR var_declaration_list
                    | empty'''
    p[0] = ('declarations', p[2] if len(p) == 3 else None)

def p_var_declaration_list(p):
    '''var_declaration_list : var_declaration SEMI var_declaration_list
                            | var_declaration SEMI'''
    p[0] = [p[1]] + (p[3] if len(p) == 4 else [])

def p_var_declaration(p):
    'var_declaration : id_list COLON type'
    for var in p[1]:
        register_variable(var)
    p[0] = ('var_decl', p[1], p[3])

def p_id_list(p):
    '''id_list : ID
               | ID COMMA id_list'''
    p[0] = [p[1]] + (p[3] if len(p) == 4 else [])

def p_type(p):
    '''type : INTEGER
            | BOOLEAN
            | ARRAY LSQUARE NUMBER DOTDOT NUMBER RSQUARE OF type'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('array', p[3], p[5], p[8])

def p_statements(p):
    '''statements : statement SEMI statements
                  | statement'''
    p[0] = [p[1]] + (p[3] if len(p) == 4 else [])

def p_statement_write(p):
    '''statement : WRITE LPAREN expr_list RPAREN
                 | WRITELN LPAREN expr_list RPAREN'''
    p[0] = (p[1].lower(), p[3])

def p_statement_readln(p):
    'statement : READLN LPAREN ID RPAREN'
    p[0] = ('readln', p[3])

def p_statement_if(p):
    'statement : IF condition THEN statement ELSE statement'
    p[0] = ('if', p[2], p[4], p[6])

def p_statement_for(p):
    'statement : FOR ID ASSIGN expression TO expression DO statement'
    p[0] = ('for', p[2], p[4], p[6], p[8])

def p_statement_while(p):
    'statement : WHILE condition DO statement'
    p[0] = ('while', p[2], p[4])

def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_statement_empty(p):
    'statement : empty'
    p[0] = 'empty'

def p_expr_list(p):
    '''expr_list : expr
                 | expr COMMA expr_list'''
    p[0] = [p[1]] + (p[3] if len(p) == 4 else [])

def p_expr(p):
    '''expr : STRING
            | expression'''
    p[0] = p[1]

def p_condition_binop(p):
    '''condition : condition AND condition
                 | condition OR condition'''
    p[0] = (p[2].lower(), p[1], p[3])

def p_condition_relational(p):
    '''condition : expression GT expression
                 | expression LT expression
                 | expression GE expression
                 | expression LE expression
                 | expression EQ expression
                 | expression NE expression'''
    p[0] = (p[2], p[1], p[3])

def p_condition_group(p):
    'condition : LPAREN condition RPAREN'
    p[0] = p[2]

# Added rule for condition as a single expression (e.g., boolean variable)
def p_condition_expr(p):
    'condition : expression'
    p[0] = p[1]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_plus_minus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = ('add', p[1], p[3])
    else:
        p[0] = ('sub', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_mult_div_mod(p):
    '''term : term MULT factor
            | term DIVIDE factor
            | term DIV factor
            | term MOD factor'''
    if p[2] == '*':
        p[0] = ('mul', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('div', p[1], p[3])
    elif p[2].lower() == 'div':
        p[0] = ('idiv', p[1], p[3])
    else:
        p[0] = ('mod', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = p[1]

def p_factor_boolean(p):
    '''factor : TRUE
              | FALSE'''
    p[0] = 1 if p[1].lower() == 'true' else 0

def p_factor_array_access(p):
    'factor : ID LSQUARE expression RSQUARE'
    p[0] = ('array_access', p[1], p[3])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en token '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis en EOF")

parser = yacc.yacc()

label_count = 0
def new_label():
    global label_count
    lbl = f"L{label_count}"
    label_count += 1
    return lbl

def generate_asm(node):
    asm = []
    if node is None:
        return asm

    if isinstance(node, list):
        for n in node:
            asm += generate_asm(n)
        return asm

    if isinstance(node, int):
        asm.append(f"PUSHI {node}")
        return asm
    if isinstance(node, str):
        if node not in symbol_table:
            return asm
        asm.append(f"PUSHG {symbol_table.get(node, 0)}")
        return asm

    tag = node[0]

    if tag == 'program':
        for _ in range(len(symbol_table)):
            asm.append("PUSHI 0")
        asm.append("START")
        asm += generate_asm(node[2])
        asm.append("STOP")

    elif tag == 'block':
        asm += generate_asm(node[2])

    elif tag in ('write', 'writeln'):
        for expr in node[1]:
            if isinstance(expr, str) and expr.startswith("'"):
                cleaned = expr.strip("'")
                asm.append(f'PUSHS "{cleaned}"')
                asm.append("WRITES")
            elif isinstance(expr, int):
                asm.append(f'PUSHI {expr}')
                asm.append("WRITEI")
            elif isinstance(expr, str):
                asm.append(f'PUSHG {symbol_table.get(expr, 0)}')
                asm.append("WRITEI")
            else:
                asm += generate_asm(expr)
                asm.append("WRITEI")
        if tag == 'writeln':
            asm.append("WRITELN")

    elif tag == 'readln':
        asm.append("READ")
        asm.append("ATOI")
        asm.append(f'STOREG {symbol_table.get(node[1], 0)}')

    elif tag == 'assign':
        varname, value = node[1], node[2]
        if isinstance(varname, tuple) and varname[0] == 'array_access':
            array_var = varname[1]
            index_expr = varname[2]
            base_pos = symbol_table.get(array_var, 0)
            asm += generate_asm(index_expr)
            asm += generate_asm(value)
            asm.append(f"PUSHG {base_pos}")
            asm.append("ADD")
            asm.append("STORE 0")
        else:
            asm += generate_asm(value)
            asm.append(f'STOREG {symbol_table.get(varname, 0)}')

    elif tag == 'if':
        cond = node[1]
        then_stmt = node[2]
        else_stmt = node[3]
        else_lbl = new_label()
        end_lbl = new_label()
        asm += generate_asm_condition(cond)
        asm.append(f"JZ {else_lbl}")
        asm += generate_asm(then_stmt)
        if else_stmt != 'empty':
            asm.append(f"JUMP {end_lbl}")
        asm.append(f"{else_lbl}:")
        asm += generate_asm(else_stmt)
        if else_stmt != 'empty':
            asm.append(f"{end_lbl}:")

    elif tag == 'for':
        var, start_expr, end_expr, stmt = node[1], node[2], node[3], node[4]
        var_pos = symbol_table.get(var, 0)
        start_lbl = new_label()
        end_lbl = new_label()
        asm += generate_asm(('assign', var, start_expr))
        asm.append(f"{start_lbl}:")
        asm += generate_asm_condition(('<=', var, end_expr))
        asm.append(f"JZ {end_lbl}")
        asm += generate_asm(stmt)
        asm.append(f"PUSHG {var_pos}")
        asm.append("PUSHI 1")
        asm.append("ADD")
        asm.append(f"STOREG {var_pos}")
        asm.append(f"JUMP {start_lbl}")
        asm.append(f"{end_lbl}:")

    elif tag == 'while':
        cond = node[1]
        stmt = node[2]
        start_lbl = new_label()
        end_lbl = new_label()
        asm.append(f"{start_lbl}:")
        asm += generate_asm_condition(cond)
        asm.append(f"JZ {end_lbl}")
        asm += generate_asm(stmt)
        asm.append(f"JUMP {start_lbl}")
        asm.append(f"{end_lbl}:")

    elif tag == 'idiv':
        asm += generate_asm(node[1])
        asm += generate_asm(node[2])
        asm.append('DIV')

    elif tag in ('add', 'sub', 'mul', 'div', 'mod'):
        asm += generate_asm(node[1])
        asm += generate_asm(node[2])
        op_map = {'add': 'ADD', 'sub': 'SUB', 'mul': 'MUL', 'div': 'DIV', 'mod': 'MOD'}
        asm.append(op_map[tag])

    elif tag == 'array_access':
        array_var = node[1]
        index_expr = node[2]
        base_pos = symbol_table.get(array_var, 0)
        asm += generate_asm(index_expr)
        asm.append(f"PUSHG {base_pos}")
        asm.append("ADD")
        asm.append("LOAD 0")

    else:
        print(f"Warning: nodo inesperado en generate_asm: {node}")

    return asm

def generate_asm_condition(cond):
    asm = []
    if isinstance(cond, tuple):
        op = cond[0]
        if op in ('and', 'or'):
            left = cond[1]
            right = cond[2]
            if op == 'and':
                end_lbl = new_label()
                asm += generate_asm_condition(left)
                asm.append(f"JZ {end_lbl}")
                asm += generate_asm_condition(right)
                asm.append(f"{end_lbl}:")
            elif op == 'or':
                true_lbl = new_label()
                end_lbl = new_label()
                asm += generate_asm_condition(left)
                asm.append(f"JNZ {true_lbl}")
                asm += generate_asm_condition(right)
                asm.append(f"JNZ {true_lbl}")
                asm.append("PUSHI 0")
                asm.append(f"JUMP {end_lbl}")
                asm.append(f"{true_lbl}:")
                asm.append("PUSHI 1")
                asm.append(f"{end_lbl}:")
        else:
            left = cond[1]
            right = cond[2]
            for val in (left, right):
                if isinstance(val, int):
                    asm.append(f'PUSHI {val}')
                elif isinstance(val, str):
                    asm.append(f'PUSHG {symbol_table.get(val, 0)}')
                elif isinstance(val, tuple):
                    asm += generate_asm(val)
            ops = {
                '>': 'SUP', '>=': 'SUPEQ',
                '<': 'INF', '<=': 'INFEQ',
                '=': 'EQUAL', '<>': 'EQUAL\nNOT'
            }
            asm.append(ops[op])
    else:
        # Handle simple expression (e.g., boolean variable)
        asm += generate_asm(cond)
        asm.append("PUSHI 0")
        asm.append("NE")  # Check if != 0 (True)
    return asm

# --- Entrada para archivo programa_pascalX.pas ---

numero_programa = input("Introduce el número del programa Pascal a compilar (ejemplo: 1, 2, 3, 4): ")
archivo_entrada = f"programa_pascal{numero_programa}.pas"

try:
    with open(archivo_entrada, "r") as archivo:
        data = archivo.read()
except FileNotFoundError:
    print(f"Error: no se encontró el archivo '{archivo_entrada}'. Verifica el número y vuelve a intentar.")
    exit(1)

ast = parser.parse(data)

asm_code = generate_asm(ast)

with open("codigo_ensamblador.asm", "w") as file:
    file.write('\n'.join(asm_code))

print(f"Archivo '{archivo_entrada}' compilado con éxito. Código ensamblador generado en 'codigo_ensamblador.asm'.")