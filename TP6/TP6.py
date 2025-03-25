import ply.lex as lex

# Definir os tokens
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espaços e tabs
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}'")

lexer = lex.lex()

# Parser LL(1) recursivo descendente
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = None

    def advance(self):
        self.token = self.lexer.token()

    def eat(self, token_type):
        if self.token and self.token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected token '{token_type}' but found '{self.token.type if self.token else None}'")

    def parse(self, data):
        self.lexer.input(data)
        self.advance()
        return self.expr()

    def expr(self):
        result = self.term()
        while self.token and self.token.type in ('PLUS', 'MINUS'):
            if self.token.type == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            elif self.token.type == 'MINUS':
                self.eat('MINUS')
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.token and self.token.type in ('TIMES', 'DIVIDE'):
            if self.token.type == 'TIMES':
                self.eat('TIMES')
                result *= self.factor()
            elif self.token.type == 'DIVIDE':
                self.eat('DIVIDE')
                denominator = self.factor()
                if denominator == 0:
                    raise ZeroDivisionError("division by zero")
                result /= denominator
        return result

    def factor(self):
        token = self.token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result
        else:
            raise SyntaxError(f"Unexpected token '{token.type}'")

# Testar o parser
parser = Parser(lexer)

examples = ["2+3", "67-(2+3*4)", "(9-2)*(13-4)"]

for expr in examples:
    result = parser.parse(expr)
    print(f"{expr} = {result}")
