from Léxico.lexico import *
from Sintático.sintatico import *


if __name__ == "__main__":
    lexical = Lexical("Léxico/file.txt")
    lexical.startTheAnalysis()
    print('\nResultado do Análise Léxica\n')
    tokens = lexical.getTokens()
    print(tokens)
    print('\nResultado da Análise Sintática\n')
    parser = Parser(tokens)
    result = parser.startTheAnalysis()
    print(result)
     




