from .scanning import Token
from copy import deepcopy


class ASTNode:
    def __init__(self, token_source: Token, left_node=None, right_node=None):
        '''
            Creates an abstract syntax tree node
            Node has three properties:
                token, left, right
        '''
        self.token = deepcopy(token_source)
        self.left = left_node
        if self.left:
            self.left.parent = self
        self.right = right_node
        if self.right:
            self.right.parent = self

        self.parent = None


def create_ast_leaf(token: Token):
    return ASTNode(token_source=token)


def create_unary_ast_node(token: Token, child: ASTNode):
    return ASTNode(token_source=token, left_node=child)
