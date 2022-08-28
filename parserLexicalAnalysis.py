from scannerLexicalAnalysis import *


class NodeNum:  # create nodes for numbers
    def __init__(self, tok):
        self.tok = tok
        self.start_pos = self.tok.start_pos
        self.end_pos = self.tok.end_pos

    def __repr__(self):
        return f'{self.tok}'


class OpNode:  # create nodes for binary operators
    def __init__(self, node_left, op_tok, node_right):
        self.node_left = node_left
        self.op_tok = op_tok
        self.node_right = node_right

        self.start_pos = self.node_left.start_pos
        self.end_pos = self.node_right.end_pos

    def __repr__(self):
        return f'({self.node_left}, {self.op_tok}, {self.node_right})'


class UnOpNode:  # create nodes for uniary operators
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.start_pos = self.op_tok.start_pos
        self.end_pos = node.end_pos

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current_token = None
        self.movecharacter()

    def movecharacter(self):  # moves past current tokens but stops once end of current tokens is reached
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        return self.current_token

    #def error(self):
        #raise Exception("Syntax Invalid")

    def parse_tokens(self):  # parse through tokens
        result_tok = self.expression_rule()
        return result_tok

    def factor_rule(self):  # grammar factor rule/ looks for number token
        tok = self.current_token
        if tok.type in (PLUS, MINUS):
            self.movecharacter()
            fact = self.factor_rule()
            return UnOpNode(tok, fact)  #allows for uniary operations involving positive neg values
        elif tok.type in (INT, FLOAT):
            self.movecharacter()
            return NodeNum(tok)
        elif tok.type == LPAREN: #uniary operations involving parenthesis precendence
            self.movecharacter()
            expr = self.expression_rule()
            if self.current_token.type == RPAREN:
                self.movecharacter()
                return expr
            else:
                return "Invalid Syntax"

    def term_rule(self): #grammar rule for terms / use binary function
        return self.binary(self.factor_rule, (MULTIPLY, DIVIDE))

    def expression_rule(self): #grammar rule for expressions / use binary function
        return self.binary(self.term_rule, (PLUS, MINUS))

    def binary(self, function, ops):  # for binary functions
        left = function()
        while self.current_token.type in ops:
            op_tok = self.current_token
            self.movecharacter()
            right = function()
            left = OpNode(left, op_tok, right)
        return left



