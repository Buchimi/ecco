from argparse import Namespace

from .scanning import Scanner
from .utils import get_args, setup_tracebacks


DEBUG = True
GLOBAL_SCANNER: Scanner
ARGS: Namespace


def main():
    """Entrypoint for the compiler"""
    global GLOBAL_SCANNER, ARGS, LLVM_OUT_FILE
    ARGS = get_args()

    GLOBAL_SCANNER = Scanner(ARGS.PROGRAM)
    GLOBAL_SCANNER.open()
    setup_tracebacks()

    # GLOBAL_SCANNER.scan()

    GLOBAL_SCANNER.scan()
    from .parsing import (parse_binary_expression)
    from .generation import generate_llvm

    generate_llvm()
    # print(interpret_ast(parsed_ast))
    GLOBAL_SCANNER.close()


if __name__ == "__main__":
    main()
