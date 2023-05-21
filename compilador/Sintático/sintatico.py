import sys, os
import copy
sys.path.insert(0, os.path.abspath('..'))

from SymbolTable.symbolTable import SymbolTable, Symbol

scope = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']

table = SymbolTable()
temp_scope = []
others_ends = []

"""
 Método: RECURSIVE DESCENTE PARSER
 Para cada não-terminal, teremos que criar uma função que valide sua produção
"""


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens_hist = tokens.copy()
        self.count = 0
        self.look_ahead = self.nextToken()

    def nextToken(self):
        """
        Return: retorna sempre o elemeno na cabeça da lista
        """
        if len(self.tokens) > 0:
            self.count += 1
            a = self.tokens.pop(0)
            return a
        return ''

    def checkToken(self, char):
        if self.look_ahead != '':
            if self.look_ahead['token'] == char:
                #print(self.look_ahead['token'], char)
                self.look_ahead = self.nextToken()
                return True
            else:
                return False

    def cont_sentencas(self):
        """
        <cont_sentencas> ::= <sentencas> | <empty>
        """
        if self.look_ahead['value'] != 'end':
            return self.sentencas()
        return True

    def mais_sentencas(self):
        """
        <mais_sentencas> ::= ; <cont_sentencas>
        """
        if self.checkToken('TK_PONTO_VIRGULA') and self.cont_sentencas():
            return True
        return False

    def cont_lista_id(self):
        """
        <cont_lista_id> ::= , <lista_id> | <empty>
        """
        if self.look_ahead['value'] == ',':
            return self.checkToken('TK_VIRGULA') and self.lista_id()
        return True

    def lista_id(self):
        """
        <lista_id> ::= <id> <cont_lista_id>
        """
        if self.id() and self.cont_lista_id():
            return True
        return False

    def cont_lista_par(self):
        """
        <cont_lista_par> ::= ; <lista_parametros> | <empty>
        """
        if self.look_ahead['value'] == ';':
            return self.checkToken('TK_PONTO_VIRGULA') and self.lista_parametros()
        return True

    def lista_parametros(self):
        """
        <lista_parametros> ::= <lista_id> : <tipo_var> <cont_lista_par>
        """
        if self.lista_id() and self.checkToken('TK_DOIS_PONTOS') and self.tipo_var() and self.cont_lista_par():
            return True
        return False

    def parametros(self):
        """
        <parametros> ::= ( <lista_parametros> ) | <empty>
        """
        if self.checkToken('TK_ABRIR_PARENTESES'):
            if not self.look_ahead['value'] == ')':
                return self.lista_parametros() and self.checkToken('TK_FECHAR_PARENTESES')
        return self.checkToken('TK_FECHAR_PARENTESES')

    def integer_num_cont(self):
        """
        <integer_num_cont> ::= ,<integer_num><integer_num_cont>|<empty>
        """
        if self.look_ahead['value'] == ',':
          return self.checkToken('TK_VIRGULA') and self.num() and self.integer_num_cont()
        return True

    def num(self):
        """
        <num> ::= <num>
        """
        if self.look_ahead['token'] == 'TK_NUMERO':
            #print(self.look_ahead)
            self.look_ahead = self.nextToken()
            return True
        return False

    def real_num_cont(self):
        """
        <real_num_cont> ::= ,<real_num><real_num_cont>|<empty>
        """
        if self.look_ahead['value'] == ',':
          return self.checkToken('TK_VIRGULA') and self.real() and self.real_num_cont()
        return True

    def real(self):
        """
        <real> ::= <real>
        """
        if self.look_ahead['token'] == 'TK_FLOAT':
            #print(self.look_ahead)
            self.look_ahead = self.nextToken()
            return True
        return False

    def real_num(self):
        """
        <real_num> ::=  +<real> | -<real> | <real>
        """
        if self.checkToken('TK_ADICAO') and self.real():
            return True
        elif self.checkToken('TK_SUBTRACAO') and self.real():
            return True
        elif self.real():
            return True
        return False

    def integer_num(self):
        """
        <integer_num> ::= +<num> | -<num> | <num> | 0 
        """
        if self.checkToken('TK_ADICAO') and self.num():
            return True
        elif self.checkToken('TK_SUBTRACAO') and self.num():
            return True
        elif self.num():
            return True
        elif self.checkToken('TK_NUMERO'):
            return True
        return False

    def opPilha(self):
        """
        <opPilha> ::= input | output | length
        """
        if self.checkToken('RW_INPUT'):
            return True
        elif self.checkToken('RW_OUTPUT'):
            return True
        elif self.checkToken('RW_LENGTH'):
            return True
        return False

    def expressao_pilha(self):
        """
        <expressao_pilha> ::= <opPilha>(<conteudo>) | concatena(<conteudo> , <conteudo>) | inverte(<conteudo>)
        """
        if self.opPilha() and self.checkToken('TK_ABRIR_PARENTESES') and self.id() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.checkToken('RW_CONCATENA') and self.checkToken('TK_ABRIR_PARENTESES') and self.id() and self.checkToken('TK_VIRGULA') and self.id() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.checkToken('RW_INVERT') and self.checkToken('TK_ABRIR_PARENTESES') and self.id() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        return False

    def operando(self):
        """
        <operando> ::= <id> | <integer_num> | <real_num> | <operador> ( <operando> , <operando> )
        """
        if self.id():
            return True
        elif self.integer_num():
            return True
        elif self.real_num():
            return True
        elif self.operador() and self.checkToken('TK_ABRIR_PARENTESES') and self.operando() and self.checkToken('TK_VIRGULA') and self.operando() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        return False

    def operador(self):
        """
        <operador> ::= + | - | * | / | //
        """
        if self.look_ahead['value'] == '+':
            return self.checkToken('TK_ADICAO')
        elif self.look_ahead['value'] == '-':
            return self.checkToken('TK_SUBTRACAO')
        elif self.look_ahead['value'] == '*':
            return self.checkToken('TK_MULTIPLICACAO')
        elif self.look_ahead['value'] == '/':
            return self.checkToken('TK_DIVISAO')
        elif self.look_ahead['value'] == '//':
            return self.checkToken('TK_DIVISAO_INTEIRA')
        return False

    def termo(self):
        """
        <termo> ::= <operador> ( <operando> , <operando> ) | <id> | <integer_num> | <real_num> 
        """
        if self.operador() and self.checkToken('TK_ABRIR_PARENTESES') and self.operando() and self.checkToken('TK_VIRGULA') and self.operando() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.integer_num():
            return True
        elif self.real_num():
            return True
        return False

    def cont_lista_arg(self):
        """
        <cont_lista_arg> ::= , <lista_arg> | <empty>
        """
        if self.look_ahead['value'] == ',':
            return self.checkToken('TK_VIRGULA') and self.lista_arg()
        return True

    def lista_arg(self):
        """
        <lista_arg> ::= <expressao> <cont_lista_arg>
        """
        if self.expressao() and self.cont_lista_arg():
            return True
        return False

    def argumentos(self):
        """
        <argumentos> ::= ( <lista_arg> ) | <empty>
        """
        if self.look_ahead['value'] == '(':
            return self.checkToken('TK_ABRIR_PARENTESES') and self.lista_arg() and self.checkToken('TK_FECHAR_PARENTESES')
        return True

    def expressao_num(self):
        """
        <expressao_num> ::=<termo> | <id><argumentos>
        """
        if self.termo():
            return True
        elif self.id() and self.argumentos():
            return True
        elif self.id():
            return True
        return False

    def expressao(self):
        """
        <expressao> ::= <expressao_num> | <expressao_pilha>
        """
        if self.expressao_num():
            return True
        elif self.expressao_pilha():
            return True
        return False

    def mais_var_write(self):
        """
        <mais_var_write> ::= , <var_write> | <empty>
        """
        if self.checkToken('TK_VIRGULA') and self.var_write():
            return True
        return False

    def var_write(self):
        """
        <var_write> ::= <id> <mais_var_write>
        """
        if self.id():
            if self.mais_var_write():
                return True
            else:
                return True
        return False

    def mais_var_read(self):
        """
        <mais_var_read> ::= , <var_read> | <empty>
        """
        if self.look_ahead['value'] == ',':
            return self.checkToken('TK_VIRGULA') and self.var_read()
        return True

    def var_read(self):
        """
        <var_read> ::= <id> <mais_var_read>
        """
        if self.id() and self.mais_var_read():
            return True
        return False

    def chamada_procedimento(self):
        """
        <chamada_procedimento> ::= <id> <argumentos>
        """
        if self.id() and self.argumentos():
            return True
        return False

    def pfalsa(self):
        """
        <pfalsa> ::= else begin <sentencas> end | <empty>
        """
        if self.look_ahead['value'] == 'else':
            return self.checkToken('RW_ELSE') and self.checkToken('RW_BEGIN') and self.sentencas() and self.checkToken('RW_END')
        return True

    def relacao(self):
        """
        <relacao> :: == | > | < | >= | <= 
        """
        if self.look_ahead['value'] == '==':
            return self.checkToken('TK_IGUAL')
        elif self.look_ahead['value'] == '>':
            return self.checkToken('TK_MAIOR')
        elif self.look_ahead['value'] == '<':
            return self.checkToken('TK_MENOR')
        elif self.look_ahead['value'] == '>=':
            return self.checkToken('TK_MAIOR_IGUAL')
        elif self.look_ahead['value'] == '<=':
            return self.checkToken('TK_MENOR_IGUAL')

        return False

    def condicao(self):
        """
        <condicao> ::= <relacao>(<expressao_num> ,<expressao_num>) |
        <relacao>(<expressao_pilha> ,<expressao_pilha>)
        """
        if self.relacao() and self.checkToken('TK_ABRIR_PARENTESES') and self.expressao_num() and self.checkToken('TK_VIRGULA') and self.expressao_num() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.relacao() and self.checkToken('TK_ABRIR_PARENTESES') and self.expressao_pilha() and self.checkToken('TK_VIRGULA') and self.expressao_pilha() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        return False

    def comando(self):
        """
        <comando> ::= read ( <var_read> ) | write ( <var_write> ) | for <id> := <expressao> to <expressao> do begin
        <sentencas> end | repeat <sentencas> until ( <condicao> ) | while ( <condicao> ) do begin <sentencas> end | if
        ( <condicao> ) then begin <sentencas> end <pfalsa> | <id> := <expressao> | <chamada_procedimento>
        """
        if self.look_ahead['token'] == 'RW_FOR' or self.look_ahead['token'] == 'RW_WHILE' or self.look_ahead['token'] == 'RW_IF' or self.look_ahead['token'] == 'RW_ELSE':
            others_ends.append('end')

        if self.checkToken('RW_READ') and self.checkToken('TK_ABRIR_PARENTESES') and self.var_read() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.checkToken('RW_WRITE') and self.checkToken('TK_ABRIR_PARENTESES') and self.var_write() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.checkToken('RW_FOR') and self.id() and self.checkToken('TK_ATRIBUICAO') and self.expressao() and self.checkToken('RW_TO') and self.expressao() and self.checkToken('RW_DO') and self.checkToken('RW_BEGIN') and self.sentencas() and self.checkToken('RW_END'):
            return True
        elif self.checkToken('RW_REPEAT') and self.sentencas() and self.checkToken('RW_UNTIL') and self.checkToken('TK_ABRIR_PARENTESES') and self.condicao() and self.checkToken('TK_FECHAR_PARENTESES'):
            return True
        elif self.checkToken('RW_WHILE') and self.checkToken('TK_ABRIR_PARENTESES') and self.condicao() and self.checkToken('TK_FECHAR_PARENTESES') and self.checkToken('RW_DO') and self.checkToken('RW_BEGIN') and self.sentencas() and self.checkToken('RW_END'):
            return True
        elif self.checkToken('RW_IF') and self.checkToken('TK_ABRIR_PARENTESES') and self.condicao() and self.checkToken('TK_FECHAR_PARENTESES') and self.checkToken('RW_THEN') and self.checkToken('RW_BEGIN') and self.sentencas() and self.checkToken('RW_END') and self.checkToken('TK_PONTO_VIRGULA') and self.pfalsa():
            return True
        elif self.id() and self.checkToken('TK_ATRIBUICAO') and self.expressao():
            return True
        elif self.chamada_procedimento():
            return True

        return False

    def sentencas(self):
        """
        <sentencas> ::= <comando> <mais_sentencas>
        """
        if self.comando() and self.mais_sentencas():
            return True
        
        return False

    def tipo_funcao(self):
        """
        <tipo_funcao> ::= integer |real | pilha of integer | pilha of real
        """
        if self.checkToken('RW_INTEGER') or self.checkToken('RW_REAL'):
            return True
        elif self.checkToken('RW_PILHA') and self.checkToken('RW_OF') and (self.checkToken('RW_INTEGER') or self.checkToken('RW_REAL')):
            return True
        return False

    def funcao(self):
        """
        <funcao> ::= function <id> <parametros> : <tipo_funcao> ; <corpo> ; <rotina>
        """
        if self.checkToken('RW_FUNCAO') and self.id() and self.parametros() and self.checkToken('TK_DOIS_PONTOS') and self.tipo_funcao() and self.checkToken('TK_PONTO_VIRGULA') and self.corpo() and self.checkToken('TK_PONTO_VIRGULA') and self.rotina():
            temp_scope.pop(-1)
            return True
        return False

    def procedimento(self):
        """
        <procedimento> ::= procedure <id> <parametros> ; <corpo> ; <rotina>
        """
        if self.checkToken('procedure') and self.id() and self.parametros() and self.checkToken('TK_PONTO_VIRGULA') and self.corpo() and self.checkToken('TK_PONTO_VIRGULA') and self.rotina():
            temp_scope.pop(-1)
            return True
        return False

    def get_function_procedure_type(self):
        index = 0
        for idx in range(self.count+1, len(self.tokens_hist)):
            if self.tokens_hist[idx]['value'] == ')': 
                index = idx+2
            if self.tokens_hist[idx]['value'] == ';':
                break
        type_ = [value['value'] for value in self.tokens_hist[index:idx]]
        return ' '.join(type_)

    def rotina(self):
        """
        <rotina> ::= <procedimento> | <funcao> | <empty>
        """
        if self.look_ahead != '' and self.look_ahead['value'] == 'procedure':
            temp_scope.append(scope.pop(0))
            table.insert(self.tokens_hist[self.count]['value'], Symbol('procedure', None, None, temp_scope[-1]))
            return self.procedimento()
        elif self.look_ahead != '' and self.look_ahead['value'] == 'function':
            temp_scope.append(scope.pop(0))
            type_ = self.get_function_procedure_type()
            table.insert(self.tokens_hist[self.count]['value'], Symbol('function', type_, None, temp_scope[-1]))
            return self.funcao()
        return True

    def cont_dc(self):
        """
        <cont_dc> ::= <dvar> <mais_dc> | <empty>
        """
        if self.look_ahead['token'] == 'TK_IDENTIFICADOR':
            return self.dvar() and self.mais_dc()
        return True

    def mais_dc(self):
        """
        <mais_dc> ::= ; <cont_dc>
        """
        if self.checkToken('TK_PONTO_VIRGULA'):
            if self.look_ahead != '' and self.look_ahead['token'] == 'TK_IDENTIFICADOR':
                return self.cont_dc()
            else:
                return True
        return False

    def tipo_var(self):
        """
        <tipo_var> ::= integer | real | pilha of integer | pilha of real
        """
        if self.checkToken('RW_INTEGER') or self.checkToken('RW_REAL'):
            return True
        elif self.checkToken('RW_PILHA') and self.checkToken('RW_OF') and (self.checkToken('RW_INTEGER') or self.checkToken('RW_REAL')):
            return True
        return False

    def variaveis(self):
        """
        <variaveis> ::= <id> , <variaveis> | empty
        """
        if self.id() and self.checkToken('TK_VIRGULA'):
            return self.variaveis()
        return True

    def dvar(self):
        """
        <dvar> ::= <variaveis> : <tipo_var>
        """
        if self.variaveis() and self.checkToken('TK_DOIS_PONTOS') and self.tipo_var():
            return True

        return False

    def conteudoPilha(self):
        """
        <conteudoPilha> := ## | #<integer_num><integer_num_cont># | #<real_num><real_num_cont>#
        """
        if self.checkToken('TK_COMENTARIO'):
           if self.checkToken('TK_COMENTARIO'):
              return True
           if self.num() and self.integer_num_cont() and self.checkToken('TK_COMENTARIO'):
              return True
           if self.real() and self.real_num_cont() and self.checkToken('TK_COMENTARIO'):
              return True
        return False

    def id(self):
        """
        <id> ::= a | b | ... | z | <conteudoPilha>
        """
        scope = None
        if len(temp_scope) != 0:
            scope = temp_scope[-1]

        if self.tokens[0]['value'] == ':=':
            value = ''
            for idx in range(self.count+1, len(self.tokens_hist)):
                if self.tokens_hist[idx]['value'] == ';' or self.tokens_hist[idx]['value'] == 'to': 
                    break

                value += self.tokens_hist[idx]['value']
            
            idx = table.updateValue(self.look_ahead['value'], value, scope)
            self.tokens_hist[self.count-1]['position'] = idx

        if (self.tokens[0]['value'] == ',' or self.tokens[0]['value'] == ':') or self.tokens[0]['value'] == ')':
            type_ = ''
            can_add = False
            for idx in range(self.count, len(self.tokens_hist)):
                if self.tokens_hist[idx]['value'] == ';' or self.tokens_hist[idx]['value'] == ')': 
                    break
                elif self.tokens_hist[idx]['value'] == ':': 
                    can_add = True
                elif can_add:
                    type_ += self.tokens_hist[idx]['value'] + ' '

            current_count = self.count
            while self.tokens_hist[current_count]['value'] != ';':
                current_count -= 1

            if self.tokens_hist[current_count+1]['value'] == 'function' or self.tokens_hist[current_count+1]['value'] == 'procedure':
                class_ = 'Paramater'
            else:
                class_ = 'var'

            if type_ == '' and self.tokens_hist[self.count-1]['token'] == 'TK_IDENTIFICADOR':
                self.tokens_hist[self.count-1]['position'] = table.getPosition(self.tokens_hist[self.count-1]['value'], scope)

            if type_ != '':
                self.tokens_hist[self.count-1]['position'] = len(table.table)
                table.insert(self.look_ahead['value'], Symbol(class_, type_, None, scope))

        return self.checkToken('TK_IDENTIFICADOR') or self.conteudoPilha()

    def declara(self):
        """
        <declara> ::= var <dvar> <mais_dc> | <empty>
        """
        if self.look_ahead['value'] == 'var':
            return self.checkToken('RW_VAR') and self.dvar() and self.mais_dc()
        return True

    def corpo(self):
        """
        <corpo> ::= <declara> <rotina> begin <sentencas> end
        """
        return self.declara() and self.rotina() and self.checkToken('RW_BEGIN') and self.sentencas() and self.checkToken('RW_END')

    def programa(self):
        """
        <programa> ::= program <id>; <corpo> • 
        """
        temp_scope.append(scope.pop(0))
        return self.checkToken('RW_PROGRAMA') and self.id() and self.checkToken('TK_PONTO_VIRGULA') and self.corpo() and self.checkToken('TK_PONTO')

    def getSymbolsTable(self):
        return table.table, self.tokens_hist
    
    def startTheAnalysis(self):
        """
        Entrada: cada token vai estar associado a uma regra de produção
        Esta função vai chamar um método para executar uma determinada regra da gramática
        """
        answer = self.programa()
        if answer:
            return 'A cadeia de tokens foi aceita'
        else:
            return 'O programa encerrou antes do esperado'

