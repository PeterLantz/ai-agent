from pkg.calculator import Calculator

calc = Calculator()

# Test cases
test_cases = [
    "3 + 7 * 2",      # Should be 3 + (7 * 2) = 17
    "3 + 7 * 2",      # Same as above, no spaces
    "3 + 7 * 2 + 1",  # 3 + 14 + 1 = 18
    "10 * 2 + 5",     # 20 + 5 = 25
    "10 + 2 * 5",     # 10 + 10 = 20
    "10 + 2 + 5",     # 17
    "10 * 2 * 5",     # 100
    "10 / 2 + 5",     # 5 + 5 = 10
    "(3 + 7) * 2",    # 10 * 2 = 20 (parentheses should work)
]

for expr in test_cases:
    try:
        result = calc.evaluate(expr)
        print(f"{expr} = {result}")
    except Exception as e:
        print(f"{expr} = ERROR: {e}")