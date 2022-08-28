class Error:  # for program errors
    def __init__(self, start_pos, end_pos, error, details):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.error = error
        self.details = details

    def string(self):
        result = f'{self.error}: {self.details}'
        result += f'Line {self.start_pos.line_num + 1}'
        return result


class IllegalChar(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'Illegal Character', details)


############################################

class Position:
    def __init__(self, index, line_num, col_num, file_text):
        self.index = index
        self.line_num = line_num
        self.col_num = col_num
        self.file_text = file_text

    def movecharacter(self, current=None):
        self.index += 1
        self.col_num += 1

        if current == '\n':
            self.line_num += 1
            self.col_num = 0

        return self

    def copy_pos(self):
        return Position(self.index, self.line_num, self.col_num, self.file_text)


################################################################

DIGITS = '0123456789'  # defines what a DIGITS is
WHITESPACE = ' \n\t'  # defines what a WHITESPACE is
FLOAT = 'FLOAT'
INT = 'INT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EQUALS = 'EQUALS'
LT = 'LT'
GT = 'GT'
LTE = 'LTE'
GTE = 'GTE'


class Token:
    def __init__(self, type_, value=None, start_pos=None, end_pos=None):
        self.type = type_
        self.value = value

        if start_pos:
            self.start_pos = start_pos.copy_pos()
            self.end_pos = self.start_pos.copy_pos()
            self.end_pos.movecharacter()

        if end_pos:
            self.end_pos = end_pos.copy_pos()

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


###############################################################################

class Scanner:
    def __init__(self, userinput):
        self.userinput = userinput
        self.pos = Position(-1, 0, -1, userinput)
        self.current = None
        self.movecharacter()

    def movecharacter(self):  # move on to next character
        self.pos.movecharacter(self.current)
        self.current = self.userinput[self.pos.index] if self.pos.index < len(self.userinput) else None

    def tokenizer(self):  # generates tokens using user input
        toke = []
        while self.current != None:
            if self.current in WHITESPACE:
                self.movecharacter()  # moves to next character if current character is a WHITESPACE
            elif self.current in DIGITS:
                toke.append(
                    self.number_generator())  # generates a new token if currect token is a . or in DIGITS; yield == generator which generates multiple tokens
            elif self.current == "+":  # generates a new token if currect token is a +;
                toke.append(Token(PLUS, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "-":  # generates a new token if currect token is a - ;
                toke.append(Token(MINUS, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "*":  # generates a new token if currect token is a * ;
                toke.append(Token(MULTIPLY, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "/":  # generates a new token if currect token is a / ;
                toke.append(Token(DIVIDE, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "(":  # generates a new token if currect token is a left parenthesis;
                toke.append(Token(LPAREN, start_pos=self.pos))
                self.movecharacter()
            elif self.current == ")":  # generates a new token if currect token is a right parenthesis;
                toke.append(Token(RPAREN, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "=":  # generates a new token if currect token is a =;
                toke.append(Token(EQUALS, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "<":  # generates a new token if currect token is a <;
                toke.append(Token(LT, start_pos=self.pos))
                self.movecharacter()
            elif self.current == ">":  # generates a new token if currect token is a >;
                toke.append(Token(GT, start_pos=self.pos))
                self.movecharacter()
            elif self.current == "<=":  # generates a new token if currect token is a <=;
                toke.append(Token(LTE, start_pos=self.pos))
                self.movecharacter()
            elif self.current == ">=":  # generates a new token if currect token is a >=;
                toke.append(Token(GTE, start_pos=self.pos))
                self.movecharacter()
            else:
                start_pos = self.pos.copy_pos()
                char = self.current
                self.movecharacter()
                return [], IllegalChar(start_pos, self.pos, " ' " + char + " ' ")
        return toke, None

    def number_generator(self):  # moves character until you advance past . or DIGITS //for NUMBER tokens
        number_s = ''
        dec_count = 0
        start_pos = self.pos.copy_pos()
        while self.current != None and self.current in DIGITS + '.':
            if self.current == ".":
                if dec_count == 1: break
                dec_count += 1  # num can only have 1 decimal in it, so end of token = when you reach 2nd character
                number_s += '.'
            else:
                number_s += self.current
            self.movecharacter()

        if dec_count == 0:
            return Token(INT, int(number_s), start_pos, self.pos)
        else:
            return Token(FLOAT, float(number_s), start_pos, self.pos)
