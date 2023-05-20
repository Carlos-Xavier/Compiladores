from Léxico.symbols import Symbols
from Léxico.tokens import Token
import sys
import os


SYMBOLS_TABLE = {}

class Lexical:
    symbols_lex = Symbols()

    def __init__(self, filename) -> None:
        self.__content = ''
        self.__fileLines = self.readFile(filename)
        self.__state = 0
        self.__currentTokenPosition = 0
        self.__column = 0
        self.__line = 0
        self.__tokens = []

    def readFile(self, filename) -> None:
        lines = []
        try:
            with open(os.path.join(os.path.dirname(sys.argv[0]), filename)) as f:
                lines = [line for line in f.readlines()]
            f.close()
        except Exception as e:
            print('Error', e)

        return lines

    def getTokens(self) -> list:
        return self.__tokens

    def startTheAnalysis(self):
        for line, content in enumerate(self.__fileLines):
            self.__line = line
            self.__content = content

            self.__column = 0
            self.__currentTokenPosition = 0
            while self.__column < len(self.__content):
                self.__match(self.__content[self.__column])

                if self.symbols_lex.ignore(self.__content[self.__column]):
                    self.__currentTokenPosition += 1

                self.__column += 1

        if self.__state != 0:
            self.createToken(self.__state)

    def __match(self, current: str) -> None:

        match self.__state:
            case 0:
                if self.symbols_lex.isChar(current):
                    self.__state = 1
                elif self.symbols_lex.isNumber(current):
                    self.__state = 2
                elif self.symbols_lex.isOperator(current):
                    self.__state = 3
                elif self.symbols_lex.other(current):
                    self.__state = 4
                elif current == ':':
                    self.__state = 7
                elif current == "#":
                    self.__state = 8
                elif self.symbols_lex.isRelacional(current):
                    self.__state = 9
                else:
                    if not self.symbols_lex.ignore(current):
                        print('Error', current, self.__line, self.__column)

            case 1:
                if self.symbols_lex.isChar(current) or self.symbols_lex.isNumber(current):
                    self.__state = 1
                else:
                    self.createToken(1)
                    if not self.symbols_lex.ignore(current):
                        self.back()

            case 2:
                if self.symbols_lex.isNumber(current):
                    self.__state = 2
                elif current == '.':
                    self.__state = 6
                else:
                    self.createToken(2)
                    if not self.symbols_lex.ignore(current):
                        self.back()

            case 3:
                if self.symbols_lex.isOperator(current):
                    self.__state = 3
                else:
                    self.createToken(3)
                    if not self.symbols_lex.ignore(current):
                        self.back()

            case 4:
                self.createToken(4)
                if not self.symbols_lex.ignore(current):
                    self.back()

            case 6:
                if self.symbols_lex.isNumber(current):
                    self.__state = 6
                else:
                    self.createToken(6)
                    if not self.symbols_lex.ignore(current):
                        self.back()

            case 7:
                if current == '=':
                    self.__column += 1
                    self.createToken(8)
                    if not self.symbols_lex.ignore(current):
                        self.back()
                else:
                    self.createToken(7)
                    self.back()

            case 8:
                self.createToken(9)
                if not self.symbols_lex.ignore(current):
                    self.back()

            case 9:
                if self.symbols_lex.isRelacional(current):
                    self.__state = 9
                else:
                    self.createToken(10)
                    if not self.symbols_lex.ignore(current):
                        self.back()

    def createToken(self, type):
        token = self.__content[self.__currentTokenPosition: self.__column].strip(
        )

        if type == 1:
            if token in Token.reservedWord:
                self.__tokens.append(
                    {'value': token, 'token': Token.reservedWord[token]})
            else:
                self.__tokens.append(
                    {'value': token, 'token': Token.TK_IDENTIFIER})

        elif type == 2:
            self.__tokens.append(
                {'value': token, 'token': Token.TK_NUMBER})

        elif type == 3:
            self.__tokens.append(
                {'value': token, 'token': Token.operador[token]})

        elif type == 4:
            self.__tokens.append(
                {'value': token, 'token': Token.others[token]})

        elif type == 6:
            self.__tokens.append(
                {'value': token, 'token': Token.TK_FLOAT})

        elif type == 7:
            self.__tokens.append(
                {'value': token, 'token': Token.TK_TWO_POINTS})

        elif type == 8:
            self.__tokens.append(
                {'value': token, 'token': Token.TK_ASSIGN})

        elif type == 9:
            self.__tokens.append(
                {'value': token, 'token': Token.TK_COMMENT})

        elif type == 10:
            if token in Token.relacional:
                self.__tokens.append(
                    {'value': token, 'token': Token.relacional[token]})

        self.__currentTokenPosition = self.__column
        self.__state = 0

    def back(self):
        self.__column -= 1

