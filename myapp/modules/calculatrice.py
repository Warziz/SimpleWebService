"""Module de calculatrice simple pour évaluer des expressions arithmétiques."""

import ast
import operator


OPERATEURS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def eval_expr(node):
    """Évalue récursivement un nœud AST."""
    if isinstance(node, ast.BinOp):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        return OPERATEURS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp):
        return OPERATEURS[type(node.op)](eval_expr(node.operand))
    if isinstance(node, ast.Constant):
        return node.n
    raise ValueError("Expression non supportée.")


def calculatrice(expr: str) -> int:
    """Évalue une expression arithmétique en toute sécurité à partir d'une chaîne.

    Args:
        expr (str): L'expression à évaluer.

    Returns:
        int: Le résultat de l'expression.
    """
    try:
        tree = ast.parse(expr, mode='eval')
        return eval_expr(tree.body)
    except Exception as e:
        raise ValueError("Erreur de calcul : " + str(e)) from e