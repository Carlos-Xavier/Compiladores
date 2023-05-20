import sys

class OperadoresRelacionais:
    maior = "maior"
    menor = "menor"
    maior_ou_igual = "maior_ou_igual"
    menor_ou_igual = "menor_ou_igual"

class OperadoresAritmeticos:
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"
    divisao_por_inteiro = "divisao_por_inteiro" 

class Semantico:
    def __init__(self, simbolos):
        self.operadores_Relacionais = OperadoresRelacionais()
        self.operadores_Aritmeticos = OperadoresAritmeticos()
        self.tabela = simbolos;

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
    

    def checar_tipos(self,propriedade, valor):
        if valor.type_ == ": integer ":
            if valor.value[0].isdigit() == False:
                print(f"Valor inicial inválido para a variável {propriedade}. Esperado: integer.")
        elif valor.type_ == ": real ":
            if not valor.value[0].replace('.', '', 1).isdigit():
                    print(f"Valor inicial inválido para a variável {propriedade}. Esperado: real.")
        elif valor.type_ == ": pilha of real ":   
            if not valor.value[0].startswith('#') or not valor.value[0].endswith('#'):
                    print(f"Valor inicial inválido para a variável {propriedade}. Esperado: pilha.")
      
    def startTheAnalysis(self):
        for simbolo in self.tabela:
            for item, value in simbolo.items():
                print(f'Variável: {item} / Classe: {value.class_} / Tipo: {value.type_} / Escopo: {value.scope} / Valor: {value.value}')
                if value.class_ == 'var' and len(value.value) != 0:
                    self.checar_tipos(item, value)
