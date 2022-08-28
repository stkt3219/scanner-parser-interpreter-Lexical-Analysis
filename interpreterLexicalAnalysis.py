from scannerLexicalAnalysis import *
from parserLexicalAnalysis import *


class Number:  # store numbers and completing operations on numbers
    def __init__(self, value):
        self.value = value
        self.set_position()

    def set_position(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def added(self, other):  # adds numbers
        if isinstance(other, Number):  # checks to see if value is a number
            return Number(self.value + other.value)

    def subtracted(self, other):  # subtracts numbers
        if isinstance(other, Number):  # checks to see if value is a number
            return Number(self.value - other.value)

    def multiplied(self, other):  # multiplies numbers
        if isinstance(other, Number):  # checks to see if value is a number
            return Number(self.value * other.value)

    def divided(self, other):  # divides numbers
        if isinstance(other, Number):  # checks to see if value is a number
            return Number(self.value / other.value)


#######################################################################


class Interpreter:
    def visitNode(self, node):  # method visits each type of node
        func_name = f'visit_{type(node).__name__}'
        function = getattr(self, func_name, self.no_visit)
        return function(node)

    def no_visit(self, node):  # if there is not a visit method defined
        raise Exception(f'No visit_{type(node).__name__} function defined')

    def visit_NodeNum(self, node):  # if number node is found
        return Number(node.tok.value).set_position(node.start_pos, node.end_pos)

    def visit_OpNode(self, node):  # if binary op node is found
        global res, result
        left = self.visitNode(node.node_left)
        right = self.visitNode(node.node_right)

        # checks operator token of node to determine what function needs to be called
        if node.op_tok.type == PLUS:
            result = left.added(right)
        elif node.op_tok.type == MINUS:
            result = left.subtracted(right)
        elif node.op_tok.type == MULTIPLY:
            result = left.multiplied(right)
        elif node.op_tok.type == DIVIDE:
            result = left.divided(right)

        return result.set_position(node.start_pos, node.end_pos)

    def visit_UnOpNode(self, node):  # if uniary op node is found

        num = self.visitNode(node.node)
        if node.op_tok.type == MINUS:
            num = num.multiplied(Number(-1))  # multiplies number by -1 to make it negative
            return num.set_position(node.start_pos, node.end_pos)



def run(userinput):
    scan = Scanner(userinput)
    tok, error = scan.tokenizer()
    if error:
        return None, error
    parser = Parser(tok)
    parse = parser.parse_tokens()
    interpreter = Interpreter()
    result = interpreter.visitNode(parse)

    return result.value, None
