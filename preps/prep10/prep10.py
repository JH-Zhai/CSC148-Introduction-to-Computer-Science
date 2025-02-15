"""Prep 10 Synthesize: Expression Trees

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a set of classes used to represent expressions
that you would see in a Python program.

It includes the three classes Expr, Num, and BinOp covered in the prep readings.
Note that in addition to the initializer and evaluate methods, we've also
included a __str__ implementation for each class that shows the corresponding
Python expression that the tree represents.

Your task is to complete the implementations of three new classes:

1.  Bool: a constant boolean (similar to Num).
2.  BoolOp: a sequence of `and` or `or` expressions (similar to BinOp).
3.  Compare: a sequence of `<` and `<=` expressions (for simplicity, we'll
    ignore other forms of expressions like `>` and `==`).

Note that BoolOp and Compare are a bit more challenging than BinOp, because
both of them can have an *arbitrary number* of subtrees, rather than being
limited to exactly two subtrees.
"""
from __future__ import annotations
from typing import Any, List, Tuple, Union


class Expr:
    """An abstract class representing a Python expression.
    """
    def evaluate(self) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.
        """
        raise NotImplementedError


class Num(Expr):
    """A numeric constant literal.

    === Attributes ===
    n: the value of the constant
    """
    n: Union[int, float]

    def __init__(self, number: Union[int, float]) -> None:
        """Initialize a new numeric constant."""
        self.n = number

    def evaluate(self) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = Num(10.5)
        >>> expr.evaluate()
        10.5
        """
        return self.n  # Simply return the value itself!

    def __str__(self) -> str:
        """Return a string representation of this expression.

        One feature we'll stick with for all Expr subclasses here is that we'll
        want to return a string that is valid Python code representing the same
        expression.

        >>> str(Num(5))
        '5'
        """
        return str(self.n)


class BinOp(Expr):
    """An arithmetic binary operation.

    === Attributes ===
    left: the left operand
    op: the name of the operator
    right: the right operand

    === Representation Invariants ===
    - self.op == '+' or self.op == '*'
    """
    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialize a new binary operation expression.

        Precondition: <op> is the string '+' or '*'.
        """
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = BinOp(Num(10.5), '+', Num(30))
        >>> expr.evaluate()
        40.5
        """
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if self.op == '+':
            return left_val + right_val
        elif self.op == '*':
            return left_val * right_val
        else:
            raise ValueError(f'Invalid operator {self.op}')

    def __str__(self) -> str:
        """Return a string representation of this expression.

        One feature we'll stick with for all Expr subclasses here is that we'll
        want to return a string that is valid Python code representing the same
        expression.

        >>> expr = BinOp(Num(10.5), '+', Num(30))
        >>> str(expr)
        '(10.5 + 30)'
        """
        return f'({str(self.left)} {self.op} {str(self.right)})'


class Bool(Expr):
    """A boolean constant literal.

    === Attributes ===
    b: the value of the constant
    """
    b: bool

    def __init__(self, b: bool) -> None:
        """Initialize a new boolean constant."""
        self.b = b

    def evaluate(self) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = Bool(True)
        >>> expr.evaluate()
        True
        """
        re_var = self.b
        return re_var


    def __str__(self) -> str:
        """Return a string representation of this expression.

        One feature we'll stick with for all Expr subclasses here is that we'll
        want to return a string that is valid Python code representing the same
        expression.

        >>> str(Bool(True))
        'True'
        """
        return str(self.b)


class BoolOp(Expr):
    """A boolean operation.

    Represents either a sequences of `and`s or a sequence of `or`s.
    Unlike BinOp, this expression can contains more than two operands,
    each separated by SAME operator:

        True and False and True and False
        True or False or True or False

    === Attributes ===
    op: the name of the boolean operation
    values: a list of operands that the operation is applied to

    === Representation invariants ===
    - self.op == 'and' or self.op == 'or'
    - len(self.values) >= 2
    - the expressions in self.values all evaluate to boolean values.
    """
    op: str
    values: List[Expr]

    def __init__(self, op: str, values: List[Expr]) -> None:
        """Initialize a new boolean operation expression.

        Precondition: op == 'and' or op == 'or' and the expressions in
                      self.values all evaluate to boolean values.
        """
        self.op = op
        self.values = values


    def evaluate(self) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = BoolOp('and', [Bool(True), Bool(True), Bool(False)])
        >>> expr.evaluate()
        False
        """
        re_var = False
        if self.op == 'or':
            for item in self.values:
                if item.evaluate() is True:
                    re_var = True
                    break

        else:
            re_var = True
            for item in self.values:
                if item.evaluate() is False:
                    re_var = False
                    break

        return re_var


    def __str__(self) -> str:
        """Return a string representation of this boolean expression.

        >>> expr = BoolOp('and', [Bool(True), Bool(True), Bool(False)])
        >>> str(expr)
        '(True and True and False)'
        """
        op_string = f' {self.op} '
        return f'({op_string.join([str(v) for v in self.values])})'


class Compare(Expr):
    """A sequence of comparison operations.

    In Python, it is possible to chain together comparison operations:
        x1 <= x2 < x3 <= x4

    This is logically equivalent to the more explicit binary form:
        (x1 <= x2) and (x2 <= x3) and (x3 <= x4),
    except each middle expression is only evaluated once.

    === Attributes ===
    left:
        the leftmost value being compared.
        (in the example above, this is `x1`)
    comparisons:
        a list of tuples, where each tuple stores an operation and expression
        (in the example above, this is [(<=, x2), (<, x3), (<= x4)])

    === Representation Invariants ===
    - len(self.comparisons) >= 1
    - the first element of every tuple in self.comparisons is '<=' or '<'.
    - the second element of every tuple in self.comparisons evaluates to a
      numerical value.
    """
    left: Expr
    comparisons: List[Tuple[str, Expr]]

    def __init__(self, left: Expr,
                 comparisons: List[Tuple[str, Expr]]) -> None:
        """Initialize a new comparison expression."""
        self.left = left
        self.comparisons = comparisons


    def evaluate(self) -> Any:
        """Return the *value* of this expression.

        The returned value should the result of how this expression would be
        evaluated by the Python interpreter.

        >>> expr = Compare(Num(1), [
        ...            ('<=', Num(2)),
        ...            ('<', Num(4.5)),
        ...            ('<=', Num(4.5))])
        >>> expr.evaluate()
        True
        """
        if self.comparisons.__len__() == 1:
            if self.comparisons[0][0] == '<=':
                return self.left.evaluate() <= self.comparisons[0][1].evaluate()
            else:
                return self.left.evaluate() < self.comparisons[0][1].evaluate()
        else:
            if self.comparisons[0][0] == '<=':
                if not self.left.evaluate() \
                       <= self.comparisons[0][1].evaluate():
                    return False
                else:
                    return Compare(self.comparisons[0][1],
                                   self.comparisons[1:]).evaluate()
            else:
                if not self.left.evaluate() < self.comparisons[0][1].evaluate():
                    return False
                else:
                    return Compare(self.comparisons[0][1],
                                   self.comparisons[1:]).evaluate()



    def __str__(self) -> str:
        """Return a string representation of this comparison expression.

        >>> expr = Compare(Num(1), [
        ...            ('<=', Num(2)),
        ...            ('<', Num(4.5)),
        ...            ('<=', Num(4.5))])
        >>> str(expr)
        '(1 <= 2 < 4.5 <= 4.5)'
        """
        s = str(self.left)
        for operator, subexpr in self.comparisons:
            s += f' {operator} {str(subexpr)}'
        return '(' + s + ')'


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
