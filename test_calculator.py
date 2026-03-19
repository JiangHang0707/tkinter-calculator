def evaluate(expression):
    try:
        return eval (expression)
    except ZeroDivisionError:
        return "÷ by zero!"
    
# run tests
assert evaluate("5+3") == 8
assert evaluate("9-4") == 5
assert evaluate("6*7") == 42
assert evaluate("10/4") == 2.5
assert evaluate("5/0") == "÷ by zero!"

print("All tests passed!")
