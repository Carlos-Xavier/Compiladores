import sys
import re


class RelationalOperators:
    bigger = ">"
    minor = "<"
    greater_or_equal = ">="
    less_or_equal = "<="


class ArithmeticOperators:
    sum = "+"
    subtraction = "-"
    multiplication = "*"
    division = "/"
    divide_by_integer = "//"


class Semantic:
    def __init__(self, symbols, tokens):
        self.relational_operators = RelationalOperators()
        self.arithmetic_operators = ArithmeticOperators()
        self.table = symbols
        self.tokens = tokens
        self.arithmeticOperatorSymbols = ['+', '-', '*', '/', '//']
        self.count = 0

    def biggest(self, x, y):
        return x > y

    def minor(self, x, y):
        return x < y

    def equal(self, x, y):
        return x == y

    def multiplication(self, x, y):
        return x * y

    def sum(self, x, y):
        return x + y

    def subtraction(self, x, y):
        return x - y

    def division(self, x, y):
        return x/y

    def divide_by_integer(self, x, y):
        return x//y

    def relational(self, operation, x, y):
        match operation:
            case self.relational_operators.bigger:
                return self.biggest(x, y)
            case self.relational_operators.minor:
                return self.minor(x, y)
            case self.relational_operators.greater_or_equal:
                if self.biggest(x, y) or self.equal(x, y):
                    return True
                return False
            case self.relational_operators.less_or_equal:
                if self.minor(x, y) or self.equal(x, y):
                    return True
                return False

    def arithmetic(self, operation, x, y):
        match operation:
            case self.arithmetic_operators.sum:
                return self.sum(x, y)
            case self.arithmetic_operators.subtraction:
                return self.subtraction(x, y)
            case self.arithmetic_operators.multiplication:
                return self.multiplication(x, y)
            case self.arithmetic_operators.division:
                return self.division(x, y)
            case self.arithmetic_operators.divide_by_integer:
                return self.divide_by_integer(x, y)

    def concatenate(self, x, y):
        if x == "##":
            return y
        if y == "##":
            return x

        conc = x.replace("#", "") + "," + y.replace("#", "")
        if x.startswith("#") or y.startswith("#"):
            return "#" + conc + "#"
        return conc

    def invert(self, x):
        return x[::-1]

    def length(self, x):
        x = x.strip('#')
        x = x.replace(',', '')
        x = list(x)
        return len(x)

    def read(self):
        pass

    def forCommand(self):
        # while self.tokens[self.count].value != 'end':
        print(self.tokens[self.count + 3]['value'])
        initial = int(self.tokens[self.count + 3]['value'])
        if (self.tokens[self.count + 5]['token'] == "TK_NUMERO" or self.tokens[self.count + 5]['token'] == "TK_FLOAT"):
            pass
        else:
            pos = self.tokens[self.count + 7]['position']
            print(self.table[pos][self.tokens[self.count + 7]['value']].value)
            stack = self.table[pos]['value']
            if stack.startswith('#'):
                stack = stack.replace("#", "")
                stack = stack.split(',')
                tempCount = self.count
                for i in range(initial, len(stack)):
                    while self.tokens[tempCount]['value'] != 'end':
                        if self.tokens[tempCount]['value'] != 'begin':
                            if self.tokens[tempCount]['token'] == "TK_IDENTIFICADOR":
                                pos = self.tokens[tempCount]['position']
                                print(self.table[pos]['value'])
                        tempCount += 1
                    tempCount = self.count
            else:
                raise Exception(
                    f"Valor inicial inválido para a variável {stack}. Esperado: pilha.")
    
    def getParameterDetails(self,scope):
        types = []
        count = 0
        for row in self.table:
            key = list(row.keys())[0]
            if scope == row[key].scope and row[key].class_ == 'parameter':
                types.append(row[key].type_)
                count+=1
        return count, types
    
    def checkIfTheFunctionCalIsCorrect(self,item, value):
        count = 0
        flag = False
        listFlag = False
        amount, types = self.getParameterDetails(value.scope)
        for idx, token in enumerate(self.tokens):
            if flag:
                if self.tokens[idx + 1]['value'] == ')':
                    break
                if not listFlag and self.tokens[idx + 1]['value'] != ',':
                    self.checkType('parameter',self.tokens[idx + 1]['value'],types.pop(0))
                    count+=1    
                if listFlag and self.tokens[idx + 1]['value'] == '#':
                    listFlag = False
                elif self.tokens[idx + 1]['value'] == '#':
                    listFlag = True
            if token['value'] == item and self.tokens[idx - 1]['value'] == ':=':
                flag = True
        return amount == count
        
    def function_procedure(self, item, currentItemType):
        flag = False
        for row in self.table:
                if (item in row and row[item].class_ == 'function') or (item in row and row[item].class_ == 'procedure'):
                    if row[item].type_.strip() == currentItemType.strip():
                        flag = True
        return flag

    def update_table(self, current_value, new_value, scope, item):
        for row in self.table:
            if item in row:
                index = row[item].value.index(current_value)
                row[item].value[0] = new_value
        
    def checkMethod(self, item, currentItemType, scope, property):
        flag = False
        type_ = item.split('(')[0]
        if type_ == 'concatena':
            flag = True
        elif type_ == 'inverte':
            flag = True
        elif type_ == 'length':
            flag = True
        else:
            flag = self.function_procedure(type_, currentItemType)
            
        return flag

    def checkMethod_tokens(self, item, currentItemType, scope, property):
        flag = False
        type_ = str(item).split('(')[0]
        if type_ == 'concatena':
            x, y = re.search(r"\((.*?)\)", item).group(1).split(',')
            x = self.check_value_in_table(x,scope) if self.check_value_in_table(x,scope) else x
            y = self.check_value_in_table(y,scope) if self.check_value_in_table(y,scope) else y

            result = self.concatenate(x, y)
            self.checkType(property, result, 'pilha of real ')
            self.update_table(item, result, scope, property)
            flag = True
        elif type_ == 'inverte':
            x = re.search(r"\((.*?)\)", item).group(1)
            x = self.check_value_in_table(x,scope) if self.check_value_in_table(x,scope) else x

            result = self.invert(x)
            self.checkType(property, result, 'pilha of real ')
            self.update_table(item, result, scope, property)
            flag = True
        elif type_ == 'length':
            x = re.search(r"\((.*?)\)", item).group(1)
            y = self.check_value_in_table(x,scope) if self.check_value_in_table(x,scope) else x
            self.checkType(x, y, 'pilha of real ')
            result = self.length(y)
            self.checkType(property, result, 'integer')
            self.update_table(item, result, scope, property)
            flag = True
        else:
            flag = self.function_procedure(type_, currentItemType)
            
        return flag
    
    def check_value_in_table(self, item, scope):
        value_returned = None
        for row in self.table:
            if (item in row and scope == row[item].scope):
                value_returned = row[item].value[0]

        return value_returned

    def check_scope_in_table(self, item, scope):
        scope_returned = None
        for row in self.table:
            if (item in row and scope == row[item].scope):
                scope_returned = row[item].scope[0]

        return scope_returned

    def operational(self, value, scope, property):
        if str(value)[0] in self.arithmeticOperatorSymbols:
            x, y = re.search(r"\((.*?)\)", value).group(1).split(',')
            x = self.check_value_in_table(x,scope) if self.check_value_in_table(x,scope) else x
            y = self.check_value_in_table(y,scope) if self.check_value_in_table(y,scope) else y
            result = self.arithmetic(value[0], int(x), int(y))
            self.update_table(value, result, scope, property)
            return result

    def checkType(self, property, value, type_):
        if type_ == "integer ":
            if not str(value).isdigit():
                raise Exception(f"Valor inicial inválido para a variável {property}. Esperado: integer.")
        elif type_ == "real ":
            if not str(value).replace('.', '', 1).isdigit():
                raise Exception(f"Valor inicial inválido para a variável {property}. Esperado: real.")
        elif type_ == "pilha of real ":
            if not str(value).startswith('#') or not value.endswith('#'):
                raise Exception(f"Valor inicial inválido para a variável {property}. Esperado: pilha.")
            
    def checkVariabels(self, property, row):
        result = False
        for value in row.value:
            result = self.check_value_in_table(value, row.scope)
            if not result and self.checkMethod(value, row.type_, row.scope, property):
                continue
            if result:
                value = result
            else:
                result = self.operational(value, row.scope, property)
                if result:
                    value = result
            self.checkType(property, value, row.type_)

    def checkVariabels_tokens(self, property, row, value):
        result = self.check_value_in_table(value, row.scope)
        if not result and self.checkMethod_tokens(value, row.type_, row.scope, property):
            return
        if result:
            value = result
        else:
            result = self.operational(value, row.scope, property)
            if result:
                value = result
        self.checkType(property, value, row.type_)
    
    def get_sentence(self, index):
        flag = False
        final = ''
        for idx, token in enumerate(self.tokens):
            if index+2 == idx: flag = True
            if token['value'] == ';' and flag: break
            if flag:
                final += token['value']

        return final

    def startTheAnalysis(self):
        print("\nAntes:\n")
        for simbolo in self.table:
            for item, value in simbolo.items():
                print(f'Variável: {item} / Classe: {value.class_} / Tipo: {value.type_} / Escopo: {value.scope} / Valor: {value.value}')

        for simbolo in self.table:
            for item, value in simbolo.items():
                if value.class_ == 'var' and len(value.value) != 0:
                    self.checkVariabels(item, value)
                if value.class_ == 'function' or value.class_ == 'procedure':
                    if not self.checkIfTheFunctionCalIsCorrect(item,value):
                        raise Exception(f"Número de paramêtros do método {item} não está correto")
                if value.class_ == None:
                    raise Exception(f"{item} não foi declarado")
        
        scope = 'A'
        flag = False
        for idx, token in enumerate(self.tokens):
            if token['value'] == 'begin': flag = True
            if token['value'] == 'end': flag = False
            if token['token'] == 'TK_IDENTIFICADOR' and 'position' in token and flag:
                if self.check_scope_in_table(token['value'], scope) and self.tokens[idx+1]['value'] == ':=':
                    simbolo = self.table[token['position']]
                    key = list(simbolo.keys())[0]
                    value = self.get_sentence(idx)
                    self.checkVariabels_tokens(key, simbolo[key], value)

        print("\nDepois:\n")
        for simbolo in self.table:
            for item, value in simbolo.items():
                print(f'Variável: {item} / Classe: {value.class_} / Tipo: {value.type_} / Escopo: {value.scope} / Valor: {value.value}')