from typing import Dict

from ..scanning import Token, TokenType
from ..utils import BeanieSyntaxError
from ..beanie import GLOBAL_SCANNER
from .beanie_ast import ASTNode, create_ast_leaf

OPERATOR_PRECEDENCE: Dict[TokenType, int] = {
    TokenType.PLUS: 12,
    TokenType.MINUS: 12,
    TokenType.STAR: 13,
    TokenType.SLASH: 13,
}


def parse_terminal_node() -> ASTNode:
    out: ASTNode
    if GLOBAL_SCANNER.current_token.type == TokenType.INTEGER_LITERAL:
        out = create_ast_leaf(GLOBAL_SCANNER.current_token)
        print(GLOBAL_SCANNER.current_token)
        GLOBAL_SCANNER.scan()
        return out
    else:
        raise BeanieSyntaxError(
            f'Expected terminal Token but got "{str(GLOBAL_SCANNER.current_token.type)}"'
        )


def err_check_precedence(node_type: TokenType) -> int:
    """Checks the precedence of an operator with error checking

    Args:
        node_type (TokenType): Type of operator to get precedence of
    Raises:
        EccoSyntaxError: If node_type is a non-operator type
    Returns:
        int: The precedence of the passed operator Token

    """
    if node_type not in OPERATOR_PRECEDENCE:
        raise BeanieSyntaxError(f"Expected operator but found {node_type}")
    return OPERATOR_PRECEDENCE[node_type]


def parse_binary_expression(previous_token_precedence: int) -> ASTNode:
    left: ASTNode
    right: ASTNode
    node_type: TokenType

    # Get an integer literal, and scan the next token into GLOBAL_SCANNER.current_token
    left = parse_terminal_node()

    node_type = GLOBAL_SCANNER.current_token.type
    # EOF
    if GLOBAL_SCANNER.current_token.type == TokenType.EOF:
        # if we hit the ned of file
        return left

    # If we haven't reached EOF, we're looking at an operator (hopefully)
    # We want to store this value so we can make an AST operator node
    # with integer literals (or sub-expressions) as children

    

    while err_check_precedence(node_type) > previous_token_precedence:

        # get the next token
        GLOBAL_SCANNER.scan()

        # recursively parse the right side of the expression
        right = parse_binary_expression(OPERATOR_PRECEDENCE[node_type])

        left = ASTNode(Token(node_type), left, right)

        # Update node_type and check for EOF
        node_type = GLOBAL_SCANNER.current_token.type
        if node_type == TokenType.EOF:
            break

    return left
