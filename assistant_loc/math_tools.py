import ast
import math
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv
}


UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}


FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs
}


CONSTANTS = {
    "pi": math.pi,
    "e": math.e
}


def calculate(expression):
    tree = ast.parse(expression, mode="eval")

    return evaluate_node(tree.body)


def evaluate_node(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Valeur non autorisée.")

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Opérateur non autorisé.")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operation = OPERATORS[operator_type]

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)

        if operator_type not in UNARY_OPERATORS:
            raise ValueError("Opérateur non autorisé.")

        value = evaluate_node(node.operand)

        operation = UNARY_OPERATORS[operator_type]

        return operation(value)

    if isinstance(node, ast.Name):

        if node.id in CONSTANTS:
            return CONSTANTS[node.id]

        raise ValueError(
            f"Constante inconnue : {node.id}"
        )

    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Fonction non autorisée.")

        function_name = node.func.id

        if function_name not in FUNCTIONS:
            raise ValueError(
                f"Fonction inconnue : {function_name}"
            )

        function = FUNCTIONS[function_name]

        arguments = [
            evaluate_node(argument)
            for argument in node.args
        ]

        return function(*arguments)

    raise ValueError("Expression non autorisée.")