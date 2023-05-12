
class Symbol:
    def __init__(self, class_=None, type_=None, value=None, scope=None):
        self.class_ = class_
        self.type_   = type_
        self.value  = []
        self.scope = scope
    

class SymbolTable:
    def __init__(self, prev=None):
        self.table = []
        self.prev  = prev


    def insert(self, s, symb):
        self.table.append(
            {
                s: symb
            }
        )


    def updateValue(self, s, value, scope):
        for symbol in self.table:
            if s in symbol and symbol[s].scope == scope:
                symbol[s].value.append(value)
                break  
        else:
            new = Symbol()
            new.value.append(value)
            self.table.append(
                {s: new}
            )
