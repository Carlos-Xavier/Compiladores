

class Token:
    TK_IDENTIFIER = 'TK_IDENTIFICADOR'
    TK_NUMBER = 'TK_NUMERO'
    TK_OPERATOR = 'TK_OPERADOR'
    TK_OTHER = 'TK_OTHER'
    TK_ASSIGN = 'TK_ATRIBUICAO'
    TK_FLOAT = 'TK_FLOAT'
    TK_ERROR = 'TK_ERRO'
    TK_STRING = 'TK_STRING'
    TK_CHAR = 'TK_CARACTERE'
    TK_RELATIONAL = 'TK_RELACIONAL'
    TK_TWO_POINTS = 'TK_DOIS_PONTOS'
    TK_COMMENT = 'TK_COMENTARIO'

    reservedWord = {
        'program': "RW_PROGRAMA",
        'begin': "RW_BEGIN",
        "end": "RW_END",
        "var": "RW_VAR",
        "integer": "RW_INTEGER",
        "real": "RW_REAL",
        "of": "RW_OF",
        "pilha": "RW_PILHA",
        "procedure": "RW_PROCEDURE",
        "function": "RW_FUNCAO",
        "read": "RW_READ",
        "write": "RW_WRITE",
        "for": "RW_FOR",
        "to": "RW_TO",
        "do": "RW_DO",
        "repeat": "RW_REPEAT",
        "until": "RW_UNTIL",
        "while": "RW_WHILE",
        "if": "RW_IF",
        "then": "RW_THEN",
        "else": "RW_ELSE",
        "concatena": "RW_CONCATENA",
        "inverte": "RW_INVERT",
        "input": "RW_INPUT",
        "output": "RW_OUTPUT",
        "length": "RW_LENGTH",
    }

    others = {
        "(": "TK_ABRIR_PARENTESES",
        ")": "TK_FECHAR_PARENTESES",
        ",": "TK_VIRGULA",
        ";": "TK_PONTO_VIRGULA",
        "[": "TK_ABRIR_COLCHETES",
        "]": "TK_FECHAR_COLCHETES",
        ".": "TK_PONTO",
        "\"": "TK_ASPAS_DUPLAS",
        "\'": "TK_ASPAS_SIMPLES"
    }

    operador = {
        "+": "TK_ADICAO",
        "-": "TK_SUBTRACAO",
        "*": "MULTIPLICACAO",
        "/": "TK_DIVISAO",
        "//": "TK_DIVISAO_INTEIRA"
    }

    relacional = {
        ">": "TK_MAIOR",
        "<": "TK_MENOR",
        ">=": "TK_MAIOR_IGUAL",
        "<=": "TK_MENOR_IGUAL",
        "==": "TK_IGUAL"
    }
