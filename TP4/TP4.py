import ply.lex as lex

def build_lexer():
    reserved = {
        'select': 'SELECT',
        'where': 'WHERE',
        'LIMIT': 'LIMIT',
        'FILTER': 'FILTER',
        'OPTIONAL': 'OPTIONAL',
        'ORDER BY': 'ORDER_BY',
        'GROUP BY': 'GROUP_BY'
    }

    tokens = (
        'COMMENT', 'VAR', 'IRI', 'STRING', 'NUMBER', 'TYPE', 
        'LBRACE', 'RBRACE', 'DOT'  
    ) + tuple(reserved.values())

    # para tokens simples
    t_LBRACE = r'\{'  
    t_RBRACE = r'\}'  
    t_DOT = r'\.'  

    # ejemplo: "# DBPedia: obras de Chuck Berry"
    def t_COMMENT(t):
        r'\#.*'
        pass  

    # ejemplo: "select", "where", "LIMIT"
    def t_KEYWORDS(t):
        r'select|where|LIMIT|FILTER|OPTIONAL|ORDER\s+BY|GROUP\s+BY'
        t.type = reserved.get(t.value.lower(), 'VAR')
        return t

    # ejemplo: "?nome", "?desc", "?s"
    def t_VAR(t):
        r'\?[a-zA-Z_]\w*'
        return t

    # ejemplo: "dbo:MusicalArtist", "foaf:name"
    def t_IRI(t):
        r'dbo:[a-zA-Z_]\w*|foaf:[a-zA-Z_]\w*'
        return t

    # ejemplo: '"Chuck Berry"@en
    def t_STRING(t):
        r'"[^\"]*"(@[a-zA-Z]+)?'
        return t

    # ejemplo: "1000" en "LIMIT 1000"
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    # ejemplo: "a" en "?s a dbo:MusicalArtist."
    def t_TYPE(t):
        r'\ba\b'
        return t

    t_ignore = ' \t\n'  # ignorar espacios y saltos de línea

    def t_error(t):
        print(f"Carácter ilegal '{t.value[0]}'")
        t.lexer.skip(1)

    return lex.lex()

def main():
    lexer = build_lexer()
    
    with open("entrada.txt", "r", encoding="utf-8") as file:
        query = file.read()
    
    lexer.input(query)
    
    with open("resultado.txt", "w", encoding="utf-8") as output_file:
        for tok in lexer:
            output_file.write(f"{tok.type}, {tok.value}, {tok.lexpos}\n")

if __name__ == "__main__":
    main()
