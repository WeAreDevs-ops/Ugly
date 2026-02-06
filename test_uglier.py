#!/usr/bin/env python3
"""
Test suite for Uglier interpreter
Run this to verify all features work correctly
"""

from uglier import execute_block, variables, functions, classes
import sys
import io

def capture_output(code):
    """Execute code and capture output"""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        execute_block(code.split('\n'))
        output = sys.stdout.getvalue()
        return output, None
    except Exception as e:
        return None, str(e)
    finally:
        sys.stdout = old_stdout
        # Clear state
        variables.clear()
        functions.clear()
        classes.clear()

def test(name, code, expected_output=None, should_error=False):
    """Run a test"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    print(f"Code:\n{code}")
    
    output, error = capture_output(code)
    
    if should_error:
        if error:
            print(f"✓ Expected error: {error}")
            return True
        else:
            print(f"✗ Should have errored but didn't")
            return False
    
    if error:
        print(f"✗ Unexpected error: {error}")
        return False
    
    print(f"Output:\n{output}")
    
    if expected_output is not None:
        if output.strip() == expected_output.strip():
            print("✓ Output matches expected")
            return True
        else:
            print(f"✗ Expected:\n{expected_output}")
            return False
    
    print("✓ Executed successfully")
    return True

def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("UGLIER INTERPRETER TEST SUITE")
    print("="*60)
    
    passed = 0
    failed = 0
    
    # Test 1: Basic variables
    if test("Basic Variables", """let x = 10
let y = 20
print x + y""", "30"):
        passed += 1
    else:
        failed += 1
    
    # Test 2: Strings
    if test("Strings", """let name = "Alice"
print "Hello, " + name""", "Hello, Alice"):
        passed += 1
    else:
        failed += 1
    
    # Test 3: Lists
    if test("Lists", """let numbers = [1, 2, 3, 4, 5]
print numbers[0]
print len(numbers)""", "1\n5"):
        passed += 1
    else:
        failed += 1
    
    # Test 4: For loop
    if test("For Loop", """let total = 0
for i in range(1, 6):
    total += i
print total""", "15"):
        passed += 1
    else:
        failed += 1
    
    # Test 5: While loop
    if test("While Loop", """let count = 0
while count < 5:
    count += 1
print count""", "5"):
        passed += 1
    else:
        failed += 1
    
    # Test 6: If statement
    if test("If Statement", """let x = 10
if x > 5:
    print "Greater"
else:
    print "Smaller"
""", "Greater"):
        passed += 1
    else:
        failed += 1
    
    # Test 7: Function definition
    if test("Function Definition", """def add(a, b):
    return a + b

let result = add(5, 3)
print result""", "8"):
        passed += 1
    else:
        failed += 1
    
    # Test 8: Recursive function
    if test("Recursive Function", """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print factorial(5)""", "120"):
        passed += 1
    else:
        failed += 1
    
    # Test 9: Nested loops
    if test("Nested Loops", """for i in range(1, 4):
    for j in range(1, 4):
        print i * j""", "1\n2\n3\n2\n4\n6\n3\n6\n9"):
        passed += 1
    else:
        failed += 1
    
    # Test 10: List iteration
    if test("List Iteration", """let fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print fruit""", "apple\nbanana\ncherry"):
        passed += 1
    else:
        failed += 1
    
    # Test 11: Compound assignment
    if test("Compound Assignment", """let x = 10
x += 5
x *= 2
print x""", "30"):
        passed += 1
    else:
        failed += 1
    
    # Test 12: Multiple variables
    if test("Multiple Variables", """let x, y = 10, 20
print x
print y""", "10\n20"):
        passed += 1
    else:
        failed += 1
    
    # Test 13: Dictionary
    if test("Dictionary", """let person = {"name": "Alice", "age": 30}
print person["name"]""", "Alice"):
        passed += 1
    else:
        failed += 1
    
    # Test 14: Math operations
    if test("Math Operations", """import math
print math.sqrt(16)
print math.pow(2, 3)""", "4.0\n8.0"):
        passed += 1
    else:
        failed += 1
    
    # Test 15: Built-in functions
    if test("Built-in Functions", """let numbers = [1, 2, 3, 4, 5]
print sum(numbers)
print max(numbers)
print min(numbers)""", "15\n5\n1"):
        passed += 1
    else:
        failed += 1
    
    # Test 16: Elif
    if test("Elif Statement", """let x = 15
if x > 20:
    print "Greater than 20"
elif x > 10:
    print "Greater than 10"
else:
    print "10 or less"
""", "Greater than 10"):
        passed += 1
    else:
        failed += 1
    
    # Test 17: String methods
    if test("String in List", """let text = "hello"
print len(text)""", "5"):
        passed += 1
    else:
        failed += 1
    
    # Test 18: Boolean operations
    if test("Boolean Operations", """let x = True
let y = False
if x and not y:
    print "Correct"
else:
    print "Wrong"
""", "Correct"):
        passed += 1
    else:
        failed += 1
    
    # Test 19: List comprehension simulation
    if test("Sum with Loop", """let numbers = [1, 2, 3, 4, 5]
let total = 0
for num in numbers:
    total += num
print total""", "15"):
        passed += 1
    else:
        failed += 1
    
    # Test 20: Function with multiple calls
    if test("Multiple Function Calls", """def greet(name):
    return "Hello, " + name

print greet("Alice")
print greet("Bob")""", "Hello, Alice\nHello, Bob"):
        passed += 1
    else:
        failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed/(passed+failed)*100:.1f}%")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
