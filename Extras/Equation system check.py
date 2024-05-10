from sympy import symbols, Eq, solve

x = symbols('x')
y = symbols('y')
eq1 = Eq((2*x + 2*y), 6)
eq2 = Eq((4*x), 0)
sol = solve((eq1, eq2), (x, y))
print(sol)