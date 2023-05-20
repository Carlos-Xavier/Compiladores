import sys
import re

class OperadoresRelacionais:
    maior = "maior"
    menor = "menor"
    maior_ou_igual = "maior_ou_igual"
    menor_ou_igual = "menor_ou_igual"

class OperadoresAritmeticos:
    soma = "+"
    subtracao = "-"
    multiplicacao = "*"
    divisao = "/"
    divisao_por_inteiro = "//" 

class Semantico:
    def __init__(self, simbolos):
        self.operadores_Relacionais = OperadoresRelacionais()
        self.operadores_Aritmeticos = OperadoresAritmeticos()
        self.table = simbolos
        self.operators_arit_symbols = ['+', '-', '*', '/', '//']

    def maior(self, x,y):
        return x > y

    def menor(self, x,y):
        return x < y

    def igual(self, x,y):
        return x == y

    def multiplicacao(self, x,y):
        return x * y
    
    def soma(self, x, y):
        return x + y
    
    def subtracao(self, x,y):
        return x - y

    def divisao(self, x, y):
        return x/y
    
    def divisao_por_inteiro(self, x, y):
        return x//y

    def relacional(self, operacao, x, y):
        match operacao:
            case self.operadores_Relacionais.maior:
                return self.maior(x,y)
            case self.operadores_Relacionais.menor:
                return self.menor(x,y)
            case self.operadores_Relacionais.maior_ou_igual:
                if self.maior(x,y) or self.igual(x,y):
                   return True
                return False
            case  self.operadores_Relacionais.menor_ou_igual:
                if self.menor(x,y) or self.igual(x,y):
                   return True
                return False


    def aritmetico(self, operacao, x, y):
        match operacao:
            case self.operadores_Aritmeticos.soma:
                return self.soma(x,y)
            case self.operadores_Aritmeticos.subtracao:
                return self.subtracao(x,y)
            case self.operadores_Aritmeticos.multiplicacao:
                return self.multiplicacao(x,y)
            case  self.operadores_Aritmeticos.divisao:
                return self.divisao(x,y)
            case  self.operadores_Aritmeticos.divisao_por_inteiro:
                return self.divisao_por_inteiro(x,y)
    

    def check_value_in_table(self, item, scope):
        value_returned = None
        for row in self.table:
            if item in row and scope == row[item].scope:
                value_returned = row[item].value[0]
        
        return value_returned


    def check_value(self, propriedade, row):
        value_returned = True
        for value in row.value:
            flag = self.check_value_in_table(value, row.scope)
            if flag: value = flag
            
            if value[0] in self.operators_arit_symbols:
                operator = self.operators_arit_symbols.index(value[0])
                
                x, y = re.search(r"\((.*?)\)", value).group(1).split(',')
                x = self.check_value_in_table(x, row.scope) if self.check_value_in_table(x, row.scope) else x
                y = self.check_value_in_table(y, row.scope) if self.check_value_in_table(y, row.scope) else y

                value = self.aritmetico(self.operators_arit_symbols[operator], int(x), int(y))

            if row.type_ == "integer ":
                if not value.isdigit():
                    raise Exception(f"Valor inicial inválido para a variável {propriedade}. Esperado: integer.")

            elif row.type_ == "real ":
                if not str(value).replace('.', '', 1).isdigit():
                    raise Exception(f"Valor inicial inválido para a variável {propriedade}. Esperado: real.")

            elif row.type_ == "pilha of real ":   
                if not value.startswith('#') or not value.endswith('#'):
                    raise Exception(f"Valor inicial inválido para a variável {propriedade}. Esperado: pilha.")

        return value_returned


    def check_type_value(self, propriedade, row):
        items = ['concatena', 'inverte']

        flag = False
        for item in row.value:
            if item.split('(')[0] in items: flag = True

        if flag:
            pass
        else:
            self.check_value(propriedade, row)

      
    def startTheAnalysis(self):
        for simbolo in self.table:
            for item, value in simbolo.items():
                print(f'Variável: {item} / Classe: {value.class_} / Tipo: {value.type_} / Escopo: {value.scope} / Valor: {value.value}')
                # if value.class_ == 'var' and len(value.value) != 0:
                #     self.check_type_value(item, value)
                # elif value.class_ == None:
                #     print(f'{item} não foi declarado.')

