from pkg.calculator import Calculator

calc = Calculator()

# Test with spaces (which works)
result = calc.evaluate("3 + 7 * 2")
print(f"Result of '3 + 7 * 2': {result}")
print(f"Expected: 17 (3 + (7 * 2)) or 20 ((3 + 7) * 2)?")

# Let's also check the precedence values
print(f"\nPrecedence values:")
print(f"+: {calc.precedence['+']}")
print(f"*: {calc.precedence['*']}")
print(f"-: {calc.precedence['-']}")
print(f"/: {calc.precedence['/']}")