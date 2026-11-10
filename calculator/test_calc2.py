from pkg.calculator import Calculator

calc = Calculator()
result = calc.evaluate("3 + 7 * 2")
print(f"Result of '3 + 7 * 2': {result}")

result2 = calc.evaluate("3+7*2")
print(f"Result of '3+7*2': {result2}")