import os
import time


def solve():
    input_file_contents = open(os.path.join("input", "day21")).read().rstrip()
    #input_file_contents = open(os.path.join("input", "test")).read().rstrip()

    monkey_expressions = dict(tuple(line.split(": ")) for line in input_file_contents.splitlines())

    sol_part1 = int(calc_monkey_yell("root", monkey_expressions))
    print("Part 1:", sol_part1)

    sol_part2 = calc_monkey_yell("root", monkey_expressions, True)
    print("Part 2:", sol_part2)


def calc_monkey_yell(monkey, monkey_expressions, part2=False):
    if monkey == "humn" and part2:
        return Expression()
    expression = monkey_expressions[monkey]
    try:
        return int(expression)
    except ValueError:
        pass
    m1, op, m2 = expression.split()
    v1 = calc_monkey_yell(m1, monkey_expressions, part2)
    v2 = calc_monkey_yell(m2, monkey_expressions, part2)
    if monkey == "root" and part2:
        return v1.solve(v2)
    if op == "+":
        return v1 + v2
    elif op == "-":
        return v1 - v2
    elif op == "*":
        return v1 * v2
    elif op == "/":
        return v1 // v2
    else:
        raise ValueError("Invalid opetation!")


class Expression:
    def __init__(self, expression=None) -> None:
        self._expression = expression

    def __add__(self, other):
        return Expression(
            (self, "+", other)
        )

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Expression(
            (self, "+", -other)
        )

    def __rsub__(self, other):
        return -1 * self + other

    def __mul__(self, other):
        return Expression(
            (self, "*", other)
        )

    def __rmul__(self, other):
        return self * other

    def __floordiv__(self, other):
        return Expression(
            (self, "/", other)
        )

    def __repr__(self) -> str:
        return str(f"Expression: {str(self._expression)}")

    def __iter__(self):
        return iter(self._expression)
    
    def is_base(self):
        return self._expression is None

    def solve(self, rhs):
        expression = self
        rhs = rhs
        while not expression.is_base():
            expression, op, term2 = expression
            if op == "*":
                rhs //= term2
            elif op == "/":
                rhs *= term2
            elif op == "+":
                rhs -= term2
            else:
                raise ValueError("invalid OP")
        return rhs

if __name__ == "__main__":
    start = time.time()
    solve()
    print(f"Run time: {time.time() - start:.3f}s")
