import ply.lex as lex
import ply.yacc as yacc

# ===========================================
#                ANALIZADOR LÉXICO
# ===========================================
# Diccionario de palabras reservadas.
# La clave es la palabra en Pascal, el valor es el tipo de token que le asignaremos.
reserved = {
    'program': 'PROGRAM', 'var': 'VAR', 'integer': 'INTEGER',
    'begin': 'BEGIN', 'end': 'END', 'writeln': 'WRITELN',
    'write': 'WRITE', 'readln': 'READLN', 'if': 'IF',
    'then': 'THEN', 'else': 'ELSE', 'for': 'FOR', 'to': 'TO',
    'do': 'DO', 'while': 'WHILE', 'div': 'DIV', 'mod': 'MOD',
    'array': 'ARRAY', 'of': 'OF', 'boolean': 'BOOLEAN',
    'and': 'AND', 'or': 'OR', 'true': 'TRUE', 'false': 'FALSE',
    'string': 'STRING_TYPE', # Tipo de dato para cadenas
    'length': 'LENGTH', # Función para obtener la longitud de un string
    'downto': 'DOWNTO'  # Para bucles for descendentes
}

tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT',
    'LPAREN', 'RPAREN', 'SEMI', 'COLON', 'COMMA',
    'DOTDOT', 'DOT', 'ASSIGN', 'STRING_LITERAL',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
    'LSQUARE', 'RSQUARE'
    # STRING_TYPE, LENGTH, DOWNTO se incluirán automáticamente desde reserved
] + list(reserved.values())

t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
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

# Regla para reconocer literales de string.
# Captura cualquier cosa entre comillas simples.
def t_STRING_LITERAL(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    return t

# Regla para reconocer números enteros.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para reconocer identificadores (variables, nombres de programa, etc.).
# También verifica si el identificador es una palabra reservada.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

# Regla para manejar saltos de línea y actualizar el número de línea.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# ===========================================
#               TABLA DE SÍMBOLOS
# ===========================================
symbol_table = {} # Diccionario para almacenar información de las variables
symbol_counter = 0 # Contador para asignar índices únicos a las variables (para P-Machine)

# Función para registrar una variable en la tabla de símbolos.
def register_variable(name, var_type_info):
    global symbol_counter
    if name not in symbol_table:
        entry = {'index': symbol_counter, 'type_info': var_type_info, 'is_array': False}
        symbol_counter += 1
        # Si es un array, añadimos información específica del array
        if isinstance(var_type_info, tuple) and var_type_info[0] == 'array':
            entry['is_array'] = True
            entry['array_info'] = {
                'lower_bound': var_type_info[1],
                'upper_bound': var_type_info[2],
                'size': var_type_info[3],
                'element_type': var_type_info[4]
            }
        symbol_table[name] = entry
    return symbol_table[name]['index']


# ===========================================
#              ANALIZADOR SINTÁCTICO
# ===========================================
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
)

def p_program(p):
    'program : PROGRAM ID SEMI block DOT'
    p[0] = ('program', p[2], p[4])

def p_block(p):
    '''block : declarations BEGIN statements_body END
             | BEGIN statements_body END'''
    if len(p) == 5:
        p[0] = ('block', p[1], p[3])
    else:
        p[0] = ('block', ('empty_declarations',), p[2])

def p_declarations(p):
    '''declarations : VAR var_declaration_list_nonempty
                    | empty_decl_tag'''
    if p.slice[1].type == 'VAR':
         p[0] = ('declarations', p[2]) 
    else:
         p[0] = p[1]


def p_empty_decl_tag(p):
    'empty_decl_tag :'
    p[0] = ('empty_declarations',)

def p_var_declaration_list_nonempty(p):
    '''var_declaration_list_nonempty : var_declaration SEMI
                                     | var_declaration SEMI var_declaration_list_nonempty'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_var_declaration(p):
    'var_declaration : id_list COLON type'
    type_info = p[3]
    for var_name in p[1]:
        register_variable(var_name, type_info)
    p[0] = ('var_decl_group', p[1], type_info)

def p_type(p):
    '''type : basic_type
            | array_type'''
    p[0] = p[1]

def p_basic_type(p):
    '''basic_type : INTEGER
                  | BOOLEAN
                  | STRING_TYPE''' 
    p[0] = ('type', p[1].lower())


def p_array_type(p):
    'array_type : ARRAY LSQUARE NUMBER DOTDOT NUMBER RSQUARE OF type'
    element_type_info = p[8]

    if not (isinstance(element_type_info, tuple) and \
            (element_type_info[0] == 'type' or element_type_info[0] == 'array') and \
            len(element_type_info) >= 2):
        print(f"Error semántico: Tipo de elemento de array inválido: {element_type_info} en línea {p.lineno(7)}")
        if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
        element_type_info = ('type', 'integer')

    lower = p[3]
    upper = p[5]
    array_size = upper - lower + 1
    if array_size <= 0:
        print(f"Error semántico: El tamaño del array debe ser positivo. [{lower}..{upper}] Línea: {p.lineno(3)}")
        if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
        array_size = 1
    p[0] = ('array', lower, upper, array_size, element_type_info)


def p_id_list(p):
    '''id_list : ID
               | ID COMMA id_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_statements_body(p):
    '''statements_body : statement_sequence
                       | empty_stmt_node'''
    if p[1][0] == 'empty_node':
        p[0] = []
    else:
        p[0] = p[1]

def p_statement_sequence(p):
    '''statement_sequence : statement
                          | statement SEMI statement_sequence'''
    if p[1][0] == 'empty_node':
        if len(p) == 2: 
            p[0] = []
        else: 
            p[0] = p[3] 
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_empty_stmt_node(p):
    'empty_stmt_node :'
    p[0] = ('empty_node',)

def p_statement(p):
    '''statement : writeln_stmt
                 | write_stmt
                 | readln_stmt
                 | assign_stmt
                 | for_loop
                 | if_stmt
                 | while_loop
                 | block
                 | empty_stmt_node'''
    p[0] = p[1]


def p_writeln_stmt(p):
    'writeln_stmt : WRITELN LPAREN expr_list RPAREN'
    p[0] = ('writeln', p[3])

def p_write_stmt(p):
    'write_stmt : WRITE LPAREN expr_list RPAREN'
    p[0] = ('write', p[3])

def p_readln_stmt(p):
    'readln_stmt : READLN LPAREN variable_list RPAREN'
    p[0] = ('readln', p[3])

def p_assign_stmt(p):
    'assign_stmt : variable ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_for_loop(p):
    '''for_loop : FOR ID ASSIGN expression TO expression DO statement
                 | FOR ID ASSIGN expression DOWNTO expression DO statement'''
    if p[5].lower() == 'to':
        p[0] = ('for_to', p[2], p[4], p[6], p[8])
    else: # DOWNTO
        p[0] = ('for_downto', p[2], p[4], p[6], p[8])


def p_if_stmt(p):
    'if_stmt : IF condition THEN statement else_clause'
    p[0] = ('if', p[2], p[4], p[5])

def p_else_clause(p):
    '''else_clause : ELSE statement
                   | empty_stmt_node'''
    if p.slice[1].type == 'ELSE':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_while_loop(p):
    'while_loop : WHILE condition DO statement'
    p[0] = ('while', p[2], p[4])

def p_variable(p):
    '''variable : ID
                | ID LSQUARE expression RSQUARE''' 
    if len(p) == 2:
        p[0] = ('id', p[1])
    else:
        p[0] = ('indexed_access', p[1], p[3]) 


def p_variable_list(p):
    '''variable_list : variable
                    | variable COMMA variable_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_expr_list(p):
    '''expr_list : expr
                 | expr COMMA expr_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_expr(p):
    '''expr : STRING_LITERAL
            | expression'''
    if p.slice[1].type == 'STRING_LITERAL':
        p[0] = ('string_literal', p[1])
    else:
        p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression MOD expression'''
    op_map = {'+': 'add', '-': 'sub', '*': 'mul', 'div': 'idiv', 'mod': 'mod'}
    p[0] = (op_map[p[2].lower()], p[1], p[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_factor(p):
    'expression : factor'
    p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | variable 
              | TRUE
              | FALSE
              | length_func_call
              | STRING_LITERAL''' # <--- AÑADIDO STRING_LITERAL como factor
    if isinstance(p[1], tuple) and p[1][0] == 'length_call':
        p[0] = p[1]
    elif p.slice[1].type == 'NUMBER':
        p[0] = ('number', p[1])
    elif p.slice[1].type == 'TRUE':
        p[0] = ('boolean', 1)
    elif p.slice[1].type == 'FALSE':
        p[0] = ('boolean', 0)
    elif p.slice[1].type == 'STRING_LITERAL': 
        p[0] = ('string_literal', p[1])
    else: # Es 'variable'
        p[0] = p[1]

def p_length_func_call(p):
    'length_func_call : LENGTH LPAREN ID RPAREN'
    p[0] = ('length_call', ('id',p[3]))


def p_condition_logop(p):
    '''condition : condition AND condition
                 | condition OR condition'''
    p[0] = (p[2].lower(), p[1], p[3])

def p_condition_relop(p):
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

def p_condition_expr(p):
    'condition : expression'
    p[0] = ('is_true', p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en token '{p.value}', tipo '{p.type}', línea {p.lineno}, posición {p.lexpos}")
    else:
        print("Error de sintaxis en EOF (inesperado fin de archivo).")
    if not hasattr(parser, 'error') or parser.error == 0 : 
        setattr(parser, 'error', 1)

parser = yacc.yacc(debug=False, write_tables=True) 

# ===========================================
#           GENERACIÓN DE CÓDIGO
# ===========================================
label_count = 0
asm_code_list = []

def new_label():
    global label_count
    lbl = f"L{label_count}"
    label_count += 1
    return lbl

# Función principal para generar código ensamblador a partir del AST.
# Es recursiva y maneja cada tipo de nodo del AST.
def gen_asm_node(node):
    global asm_code_list
    if node is None or node[0] == 'empty_node' or node[0] == 'empty_declarations':
        return

    node_type = node[0]

    if node_type == 'program':
        asm_code_list.extend(["PUSHI 0"] * symbol_counter)
        asm_code_list.append("START")
        gen_asm_node(node[2])
        asm_code_list.append("STOP")

    elif node_type == 'block':
        if node[1] is not None and node[1][0] != 'empty_declarations':
            gen_declarations_alloc(node[1])

        if node[2] is not None : 
            for stmt_node in node[2]: 
                if stmt_node and stmt_node[0] != 'empty_node':
                    gen_asm_node(stmt_node)


    elif node_type in ('writeln', 'write'):
        expr_list = node[1]
        for expr_node in expr_list:
            if expr_node[0] == 'string_literal':
                string_value_for_vm = expr_node[1]
                asm_code_list.append(f'PUSHS "{string_value_for_vm}"')
                asm_code_list.append("WRITES")
            else: 
                gen_asm_node(expr_node)
                asm_code_list.append("WRITEI") 
        if node_type == 'writeln':
            asm_code_list.append("WRITELN")

    elif node_type == 'readln':
        var_list = node[1] 
        for var_node in var_list: 
            if var_node[0] == 'id':
                var_name = var_node[1]
                if var_name not in symbol_table:
                    print(f"Error semántico: Variable '{var_name}' en readln no declarada.")
                    if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
                    return
                var_s_info = symbol_table[var_name]
                
                asm_code_list.append("READ") 
                
                if not (var_s_info['type_info'][0] == 'type' and var_s_info['type_info'][1] == 'string'):
                    asm_code_list.append("ATOI")
                
                asm_code_list.append(f"STOREG {var_s_info['index']}")
            
            elif var_node[0] == 'indexed_access': 
                array_name = var_node[1]
                index_expr = var_node[2]

                if array_name not in symbol_table or not symbol_table[array_name]['is_array']:
                    print(f"Error semántico en readln: '{array_name}' no es un array o no está declarado.")
                    if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
                    return
                array_info = symbol_table[array_name]['array_info']
                
                asm_code_list.append(f"PUSHG {symbol_table[array_name]['index']}")
                gen_asm_node(index_expr)
                asm_code_list.append(f"PUSHI {array_info['lower_bound']}")
                asm_code_list.append("SUB")
                asm_code_list.append("READ")
                asm_code_list.append("ATOI") 
                asm_code_list.append("STOREN")


    elif node_type == 'assign':
        var_node = node[1] 
        expr_node = node[2]

        if var_node[0] == 'id':
            var_name = var_node[1]
            gen_asm_node(expr_node)
            asm_code_list.append(f"STOREG {symbol_table[var_name]['index']}")
        elif var_node[0] == 'indexed_access': 
            target_name = var_node[1] 
            index_expr = var_node[2]

            if target_name not in symbol_table:
                print(f"Error semántico en asignación indexada: '{target_name}' no declarado.")
                if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
                return
            
            target_info = symbol_table[target_name]

            if target_info['is_array']:
                array_info = target_info['array_info']
                asm_code_list.append(f"PUSHG {target_info['index']}") 
                gen_asm_node(index_expr) 
                asm_code_list.append(f"PUSHI {array_info['lower_bound']}")
                asm_code_list.append("SUB") 
                gen_asm_node(expr_node) 
                asm_code_list.append("STOREN")
            elif target_info['type_info'][0] == 'type' and target_info['type_info'][1] == 'string':
                print(f"Error: Asignación a carácter de string (ej. miString[i] := 'a') no soportada aún.")
                if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            else:
                print(f"Error semántico: '{target_name}' no es un array ni un string para acceso indexado en asignación.")
                if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)


    elif node_type == 'for_to':
        var_name = node[1]
        start_expr = node[2]
        end_expr = node[3]
        stmt_node = node[4]
        if var_name not in symbol_table:
            print(f"Error semántico en for: Variable '{var_name}' no declarada.")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            return
        var_idx = symbol_table[var_name]['index']

        loop_start_label = new_label()
        loop_end_label = new_label()

        gen_asm_node(start_expr)
        asm_code_list.append(f"STOREG {var_idx}")
        asm_code_list.append(f"{loop_start_label}:")
        asm_code_list.append(f"PUSHG {var_idx}")
        gen_asm_node(end_expr)
        asm_code_list.append("INFEQ")
        asm_code_list.append(f"JZ {loop_end_label}")
        gen_asm_node(stmt_node)
        asm_code_list.append(f"PUSHG {var_idx}")
        asm_code_list.append("PUSHI 1")
        asm_code_list.append("ADD")
        asm_code_list.append(f"STOREG {var_idx}")
        asm_code_list.append(f"JUMP {loop_start_label}")
        asm_code_list.append(f"{loop_end_label}:")

    elif node_type == 'for_downto': 
        var_name = node[1]
        start_expr = node[2] 
        end_expr = node[3]   
        stmt_node = node[4]
        
        if var_name not in symbol_table:
            print(f"Error semántico en for downto: Variable '{var_name}' no declarada.")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            return
        var_idx = symbol_table[var_name]['index']

        loop_start_label = new_label()
        loop_end_label = new_label()

        gen_asm_node(start_expr) 
        asm_code_list.append(f"STOREG {var_idx}")

        asm_code_list.append(f"{loop_start_label}:")
        asm_code_list.append(f"PUSHG {var_idx}") 
        gen_asm_node(end_expr)   
        asm_code_list.append("SUPEQ") 
        asm_code_list.append(f"JZ {loop_end_label}") 

        gen_asm_node(stmt_node)

        asm_code_list.append(f"PUSHG {var_idx}")
        asm_code_list.append("PUSHI 1")
        asm_code_list.append("SUB") 
        asm_code_list.append(f"STOREG {var_idx}")

        asm_code_list.append(f"JUMP {loop_start_label}")
        asm_code_list.append(f"{loop_end_label}:")
    

    elif node_type == 'if':
        cond_node = node[1]
        then_stmt = node[2]
        else_stmt = node[3]

        else_label = new_label()
        end_if_label = new_label()

        gen_asm_condition(cond_node, else_label)
        gen_asm_node(then_stmt)

        if else_stmt is not None and else_stmt[0] != 'empty_node':
            asm_code_list.append(f"JUMP {end_if_label}")

        asm_code_list.append(f"{else_label}:")
        if else_stmt is not None and else_stmt[0] != 'empty_node':
            gen_asm_node(else_stmt)

        if else_stmt is not None and else_stmt[0] != 'empty_node':
             asm_code_list.append(f"{end_if_label}:")


    elif node_type == 'while':
        cond_node = node[1]
        stmt_node = node[2]

        loop_start_label = new_label()
        loop_end_label = new_label()

        asm_code_list.append(f"{loop_start_label}:")
        gen_asm_condition(cond_node, loop_end_label)
        gen_asm_node(stmt_node)
        asm_code_list.append(f"JUMP {loop_start_label}")
        asm_code_list.append(f"{loop_end_label}:")

    elif node_type == 'number':
        asm_code_list.append(f"PUSHI {node[1]}")
    elif node_type == 'boolean':
        asm_code_list.append(f"PUSHI {node[1]}")
    elif node_type == 'id':
        if node[1] not in symbol_table:
            print(f"Error semántico: Variable '{node[1]}' no declarada usada en expresión.")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            return
        asm_code_list.append(f"PUSHG {symbol_table[node[1]]['index']}")
    elif node_type == 'string_literal':
        string_value_for_vm = node[1]
        asm_code_list.append(f'PUSHS "{string_value_for_vm}"')

    elif node_type == 'length_call': 
        id_node = node[1] 
        var_name = id_node[1]
        
        if var_name not in symbol_table:
            print(f"Error semántico: Variable '{var_name}' para LENGTH no declarada.")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            return
        
        var_s_info = symbol_table[var_name]
        if not (var_s_info['type_info'][0] == 'type' and var_s_info['type_info'][1] == 'string'):
            print(f"Error semántico: LENGTH solo se puede aplicar a variables string. '{var_name}' no es string.")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            return

        asm_code_list.append(f"PUSHG {var_s_info['index']}") 
        asm_code_list.append("STRLEN") 

    elif node_type == 'indexed_access': 
        base_var_name = node[1]
        index_expr = node[2]

        if base_var_name not in symbol_table :
            print(f"Error semántico en acceso indexado: '{base_var_name}' no declarada.")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)
            return
        
        var_info = symbol_table[base_var_name]

        if var_info['is_array']:
            array_info = var_info['array_info']
            asm_code_list.append(f"PUSHG {var_info['index']}")
            gen_asm_node(index_expr)
            asm_code_list.append(f"PUSHI {array_info['lower_bound']}")
            asm_code_list.append("SUB")
            asm_code_list.append("LOADN")
        elif var_info['type_info'][0] == 'type' and var_info['type_info'][1] == 'string':
            asm_code_list.append(f"PUSHG {var_info['index']}") 
            gen_asm_node(index_expr) 
            asm_code_list.append("PUSHI 1") 
            asm_code_list.append("SUB") 
            asm_code_list.append("CHARAT") 
        else:
            print(f"Error semántico: '{base_var_name}' no es un array ni un string para acceso con [].")
            if not hasattr(parser, 'error') or parser.error == 0 : setattr(parser, 'error', 1)


    elif node_type in ('add', 'sub', 'mul', 'idiv', 'mod'):
        gen_asm_node(node[1])
        gen_asm_node(node[2])
        op_map_vm = {'add': 'ADD', 'sub': 'SUB', 'mul': 'MUL', 'idiv': 'DIV', 'mod': 'MOD'}
        asm_code_list.append(op_map_vm[node_type])

def gen_declarations_alloc(declarations_node): 
    global asm_code_list
    if declarations_node is None or declarations_node[0] == 'empty_declarations' or declarations_node[1] is None:
        return

    list_of_var_decl_groups = declarations_node[1] 

    for var_decl_group in list_of_var_decl_groups:
        if not isinstance(var_decl_group, tuple) or len(var_decl_group) < 3:
            continue 

        id_list = var_decl_group[1]     
        type_info = var_decl_group[2]

        if isinstance(type_info, tuple) and type_info[0] == 'array':
            array_size = type_info[3]
            for var_name in id_list:
                asm_code_list.append(f"ALLOC {array_size}")
                asm_code_list.append(f"STOREG {symbol_table[var_name]['index']}")

def gen_asm_condition(cond_node, false_label):
    global asm_code_list
    if cond_node is None or cond_node[0] == 'empty_node': return

    cond_type = cond_node[0]

    if cond_type in ('>', '<', '>=', '<=', '=', '<>'):
        left_expr = cond_node[1]  
        right_expr = cond_node[2] 
        
        gen_asm_node(left_expr) 

        if right_expr[0] == 'string_literal' and len(right_expr[1]) == 1 and \
           left_expr[0] == 'indexed_access' and \
           symbol_table.get(left_expr[1]) and \
           symbol_table[left_expr[1]]['type_info'][0] == 'type' and \
           symbol_table[left_expr[1]]['type_info'][1] == 'string':
            # Comparación de char (resultado de CHARAT) con string literal de un char
            char_val = right_expr[1][0]
            asm_code_list.append(f"PUSHI {ord(char_val)}") 
        else:
            gen_asm_node(right_expr) 
        
        op_map_vm = {'>': 'SUP', '<': 'INF', '>=': 'SUPEQ', '<=': 'INFEQ', '=': 'EQUAL'}
        if cond_type == '<>':
            asm_code_list.append("EQUAL")
            asm_code_list.append("NOT")
        else:
            asm_code_list.append(op_map_vm[cond_type])
        asm_code_list.append(f"JZ {false_label}")

    elif cond_type == 'and':
        left_cond = cond_node[1]
        right_cond = cond_node[2]
        gen_asm_condition(left_cond, false_label)
        gen_asm_condition(right_cond, false_label)

    elif cond_type == 'or':
        left_cond = cond_node[1]
        right_cond = cond_node[2]
        
        path_OR_is_true = new_label()
        gen_asm_condition_inverted(left_cond, path_OR_is_true)
        gen_asm_condition(right_cond, false_label)
        asm_code_list.append(f"{path_OR_is_true}:")


    elif cond_type == 'is_true':
        gen_asm_node(cond_node[1])
        asm_code_list.append(f"JZ {false_label}")

def gen_asm_condition_inverted(cond_node, true_label):
    global asm_code_list
    if cond_node is None or cond_node[0] == 'empty_node': return

    cond_type = cond_node[0]

    if cond_type in ('>', '<', '>=', '<=', '=', '<>'):
        left_expr = cond_node[1]
        right_expr = cond_node[2]
        
        gen_asm_node(left_expr)

        if right_expr[0] == 'string_literal' and len(right_expr[1]) == 1 and \
           left_expr[0] == 'indexed_access' and \
           symbol_table.get(left_expr[1]) and \
           symbol_table[left_expr[1]]['type_info'][0] == 'type' and \
           symbol_table[left_expr[1]]['type_info'][1] == 'string':
            char_val = right_expr[1][0]
            asm_code_list.append(f"PUSHI {ord(char_val)}")
        else:
            gen_asm_node(right_expr)
            
        op_map_vm = {'>': 'SUP', '<': 'INF', '>=': 'SUPEQ', '<=': 'INFEQ', '=': 'EQUAL'}
        if cond_type == '<>':
            asm_code_list.append("EQUAL")
            asm_code_list.append("NOT")
        else:
            asm_code_list.append(op_map_vm[cond_type])
        asm_code_list.append(f"JNZ {true_label}")

    elif cond_type == 'and':
        end_of_and_check_inverted = new_label()
        gen_asm_condition(cond_node[1], end_of_and_check_inverted) # Si es FALSO, salta al final
        # Si no saltó, el primero es VERDADERO, ahora el segundo debe ser VERDADERO
        gen_asm_condition_inverted(cond_node[2], true_label)
        asm_code_list.append(f"{end_of_and_check_inverted}:")


    elif cond_type == 'or':
        # Si el primero es VERDADERO, salta a true_label
        gen_asm_condition_inverted(cond_node[1], true_label)
        # Si no saltó, el primero es FALSO. Si el segundo es VERDADERO, salta a true_label
        gen_asm_condition_inverted(cond_node[2], true_label)
        
    elif cond_type == 'is_true':
        gen_asm_node(cond_node[1])
        asm_code_list.append(f"JNZ {true_label}")

# --- DEBUG LEXER ---
def debug_lexer_for_file(filename_to_debug, file_content):
    # print(f"\n--- INICIANDO DEBUG DEL LEXER PARA EL ARCHIVO: '{filename_to_debug}' ---") 
    if file_content:
        global lexer
        lexer.lineno = 1 # Reiniciar contador de línea del lexer
        lexer.input(file_content)
        # print(f"\n--- LEXER DEBUG OUTPUT PARA '{filename_to_debug}' ---") 
        while True:
            tok = lexer.token()
            if not tok:
                break
            # print(f"Token: {tok}") 
        # print("--- END LEXER DEBUG ---\n") 
    lexer.lineno = 1 
# --- FIN DEBUG LEXER ---


# ===========================================
#               EJECUCIÓN
# ===========================================
if __name__ == "__main__":
    symbol_table.clear()
    symbol_counter = 0
    label_count = 0
    asm_code_list = []
    parser.error = 0 # Flag para errores de parsing/semánticos


    numero_programa = input("Introduce el número del programa Pascal a compilar (ejemplo: 1 para HelloWorld, 4 para SomaArray): ")
    archivo_entrada = f"programa_pascal{numero_programa}.pas"
    data = "" 

    try:
        with open(archivo_entrada, "r") as archivo:
            data = archivo.read()
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{archivo_entrada}'. Verifica el nombre (debe estar en el mismo directorio).")
        exit(1)
    
    # Descomentar para debug específico del lexer si es necesario
    # debug_lexer_for_file(archivo_entrada, data)

    print(f"\n--- Compilando {archivo_entrada} ---")
    
    lexer.lineno = 1 
    parser.error = 0 
    
    ast = parser.parse(data,lexer=lexer) 
    
    if ast and parser.error == 0: 
        print("\n--- Tabla de Símbolos ---")
        for name, info in symbol_table.items():
            print(f"{name}: {info}")

        print("\n--- Generando Código Ensamblador ---")
        gen_asm_node(ast)
        
        output_filename = "codigo_ensamblador.asm"
        with open(output_filename, "w") as file:
            file.write('\n'.join(asm_code_list))
        print(f"\nArchivo '{archivo_entrada}' compilado con éxito.")
        print(f"Código ensamblador generado en '{output_filename}'.")
    else: # Si hubo errores durante el parseo o el AST no se generó
        final_error_flag = getattr(parser, 'error', 0)
        print(f"Error durante el parsing (parser.error = {final_error_flag}) o AST no generado. No se generó código ensamblador.")