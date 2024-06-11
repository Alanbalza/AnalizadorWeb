import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMI', 'COLON', 'COMMA', 'LBRACKET', 'RBRACKET',
    'STRING_LITERAL'
]

# Palabras reservadas
reserved = {
    'object': 'OBJECT',
    'def': 'DEF',
    'Array': 'ARRAY',
    'String': 'STRING',
    'Unit': 'UNIT',
    'println': 'PRINTLN'
}

tokens += list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Expresiones regulares para tokens más complejos
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\".*?\"'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal {t.value[0]}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definir la precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# Definición de la gramática
def p_program(p):
    'program : OBJECT ID LBRACE main_def RBRACE'
    pass

def p_main_def(p):
    'main_def : DEF ID LPAREN args RPAREN COLON UNIT EQUALS LBRACE stmt_list RBRACE'
    pass

def p_args(p):
    'args : ID COLON ARRAY LBRACKET STRING RBRACKET'
    pass

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    pass

def p_stmt(p):
    'stmt : PRINTLN LPAREN STRING_LITERAL RPAREN SEMI'
    pass

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis en '{p.value}'")
    else:
        raise SyntaxError("Error de sintaxis al final de la entrada")

# Construir el parser
parser = yacc.yacc()

# Función para realizar el análisis
def analizar_codigo(codigo):
    lexer.input(codigo)
    tokens = []
    for tok in lexer:
        token_info = {
            'token': tok.type,
            'valor': tok.value,
            'linea': tok.lineno,
            'posicion': tok.lexpos
        }
        tokens.append(token_info)
    resultado_lexico = tokens

    resultado_sintactico = "Programa válido"
    try:
        parser.parse(codigo)
    except SyntaxError as e:
        resultado_sintactico = f"Programa inválido: {e}"

    # Clasificación de tokens para la tabla
    resultado_clasificado = []
    totales = {
        'reservada': 0,
        'identificador': 0,
        'numero': 0,
        'simbolo': 0,
        'parentesis_izquierdo': 0,
        'parentesis_derecho': 0,
        'llave_izquierda': 0,
        'llave_derecha': 0
    }
    for token in tokens:
        clasificado = {
            'Token': token['valor'],
            'reservada': 'x' if token['token'] in reserved.values() else '',
            'identificador': 'x' if token['token'] == 'ID' else '',
            'numero': 'x' if token['token'] == 'NUMBER' else '',
            'simbolo': 'x' if token['token'] in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'SEMI', 'COLON', 'COMMA'] else '',
            'parentesis_izquierdo': 'x' if token['token'] == 'LPAREN' else '',
            'parentesis_derecho': 'x' if token['token'] == 'RPAREN' else '',
            'llave_izquierda': 'x' if token['token'] == 'LBRACE' else '',
            'llave_derecha': 'x' if token['token'] == 'RBRACE' else ''
        }
        for key in totales:
            if clasificado[key] == 'x':
                totales[key] += 1
        resultado_clasificado.append(clasificado)

    return resultado_clasificado, resultado_sintactico, totales
