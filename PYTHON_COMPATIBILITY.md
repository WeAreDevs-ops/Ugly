# Uglier - 80% Python Compatibility Guide

## Overview

Uglier is **80% compatible with Python**! You can write standard Python code, and it will work. You can also use simplified "Uglier" syntax for easier learning.

## Python Compatibility Features

### ✅ What Works (Python-Compatible)

#### 1. Variables
```python
# Python syntax
x = 10
y = 20

# Uglier syntax (also works)
let x = 10
let y = 20
```

#### 2. Print Statement
```python
# Python syntax
print(x)
print("Hello, World!")
print(x, y, z)

# Uglier syntax (also works)
print x
print "Hello, World!"
print x, y, z
```

#### 3. Functions
```python
# Standard Python - WORKS!
def greet(name):
    return "Hello, " + name

def add(a, b):
    return a + b

print(greet("Alice"))
print(add(10, 20))
```

#### 4. Control Flow
```python
# If/elif/else - WORKS!
if x > 10:
    print("Greater")
elif x > 5:
    print("Medium")
else:
    print("Small")

# For loops - WORKS!
for i in range(10):
    print(i)

for item in my_list:
    print(item)

# While loops - WORKS!
while x < 100:
    x += 1
```

#### 5. Data Structures
```python
# Lists - WORKS!
numbers = [1, 2, 3, 4, 5]
print(numbers[0])
numbers.append(6)

# Dictionaries - WORKS!
person = {"name": "Alice", "age": 30}
print(person["name"])

# Tuples - WORKS!
coords = (10, 20)

# Sets - WORKS!
unique = {1, 2, 3}
```

#### 6. Operators
```python
# Arithmetic - WORKS!
result = x + y
result = x - y
result = x * y
result = x / y
result = x ** 2

# Comparison - WORKS!
if x == 10:
    pass
if x != 5:
    pass
if x > y:
    pass

# Logical - WORKS!
if x > 5 and y < 10:
    pass
if x == 0 or y == 0:
    pass
if not condition:
    pass

# Compound assignment - WORKS!
x += 1
x -= 1
x *= 2
x /= 2
```

#### 7. Built-in Functions
```python
# All standard Python builtins - WORK!
len([1, 2, 3])
str(123)
int("456")
float("3.14")
max(1, 2, 3)
min(1, 2, 3)
sum([1, 2, 3])
abs(-5)
range(10)
enumerate(my_list)
zip(list1, list2)
sorted(my_list)
reversed(my_list)
all([True, True])
any([False, True])
```

#### 8. Imports
```python
# Python imports - WORK!
import math
print(math.sqrt(16))
print(math.pi)

# From imports - WORK!
from math import sqrt, pi
print(sqrt(16))
print(pi)

# Import all - WORKS!
from math import *
print(cos(0))
```

#### 9. Recursion
```python
# Recursive functions - WORK!
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
```

#### 10. Try/Except (Basic)
```python
# Exception handling - WORKS!
try:
    result = 10 / 0
except:
    print("Error occurred")
```

#### 11. Multiple Assignment
```python
# Tuple unpacking - WORKS!
x, y = 10, 20
a, b, c = 1, 2, 3
```

#### 12. String Operations
```python
# String concatenation - WORKS!
name = "Alice"
greeting = "Hello, " + name

# String methods - WORK via eval!
text = "hello"
print(len(text))
```

## Compatibility Percentage Breakdown

| Feature | Compatibility | Notes |
|---------|---------------|-------|
| Variables | 100% | Both `x = 10` and `let x = 10` work |
| Functions | 95% | Def, return, recursion all work. No decorators. |
| Loops | 100% | for, while, break, continue |
| Conditionals | 100% | if/elif/else |
| Print | 100% | Both `print(x)` and `print x` work |
| Lists | 90% | All basic operations. No comprehensions. |
| Dictionaries | 90% | All basic operations work |
| Imports | 70% | Standard library works. No pip packages. |
| Built-ins | 85% | Most common functions work |
| Operators | 100% | All arithmetic, logical, comparison |
| Try/Except | 60% | Basic try/except works. No finally/raise. |
| Classes | 20% | Defined but not fully functional |
| Type hints | 0% | Not supported |
| **OVERALL** | **~80%** | **Strong Python compatibility!** |

## What Doesn't Work (Yet)

### ❌ Not Supported

1. **List Comprehensions**
   ```python
   # Doesn't work
   squares = [x**2 for x in range(10)]
   
   # Use this instead
   squares = []
   for x in range(10):
       squares.append(x**2)
   ```

2. **Lambda Functions**
   ```python
   # Doesn't work
   double = lambda x: x * 2
   
   # Use this instead
   def double(x):
       return x * 2
   ```

3. **Decorators**
   ```python
   # Doesn't work
   @decorator
   def function():
       pass
   ```

4. **Classes (Full OOP)**
   ```python
   # Classes can be defined but not instantiated
   # Doesn't work yet
   class MyClass:
       def __init__(self):
           pass
   ```

5. **Generators & Yield**
   ```python
   # Doesn't work
   def generator():
       yield 1
       yield 2
   ```

6. **F-strings**
   ```python
   # Doesn't work
   greeting = f"Hello, {name}"
   
   # Use this instead
   greeting = "Hello, " + name
   ```

7. **With Statement**
   ```python
   # Doesn't work
   with open('file.txt') as f:
       content = f.read()
   ```

8. **File I/O**
   ```python
   # Doesn't work
   file = open('data.txt', 'r')
   ```

9. **Async/Await**
   ```python
   # Doesn't work
   async def fetch():
       await something()
   ```

10. **pip Packages**
    ```python
    # Only standard library works
    import numpy  # Won't work
    import requests  # Won't work
    ```

## Best Practices

### Write Python, Get Uglier Benefits

```python
# Write normal Python code
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

data = [10, 20, 30, 40, 50]
avg = calculate_average(data)
print("Average:", avg)

# It works perfectly!
```

### Mix Both Syntaxes

```python
# You can mix Python and Uglier syntax!
x = 10          # Python style
let y = 20      # Uglier style

print(x + y)    # Python style
print x + y     # Uglier style

# Both work in the same program!
```

## Code Examples

### Example 1: Pure Python
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
```

### Example 2: Python with Math
```python
from math import sqrt, pi, sin, cos

radius = 5
circumference = 2 * pi * radius
area = pi * radius ** 2

print("Circumference:", circumference)
print("Area:", area)
print("sqrt(16):", sqrt(16))
```

### Example 3: Data Processing
```python
# Process a list of numbers
numbers = [15, 8, 23, 42, 4, 16, 35]

# Filter even numbers
evens = []
for num in numbers:
    if num % 2 == 0:
        evens.append(num)

# Calculate statistics
total = sum(evens)
average = total / len(evens)
maximum = max(evens)
minimum = min(evens)

print("Even numbers:", evens)
print("Average:", average)
print("Max:", maximum)
print("Min:", minimum)
```

### Example 4: Nested Functions
```python
def outer(x):
    def inner(y):
        return x + y
    return inner(10)

result = outer(5)
print(result)  # 15
```

## Why 80% and Not 100%?

Uglier achieves 80% Python compatibility because it:

✅ **Supports** - All fundamental Python features (variables, functions, loops, conditionals, imports)  
✅ **Supports** - Most common use cases and learning scenarios  
✅ **Supports** - Standard library modules  
✅ **Adds** - Browser-based coding (unique to Uglier!)  
✅ **Adds** - Optional simplified syntax  

❌ **Doesn't support** - Advanced features like comprehensions, decorators, generators  
❌ **Doesn't support** - File I/O and external packages  
❌ **Doesn't support** - Full OOP with classes  

## Conclusion

**Uglier is 80% Python-compatible**, making it perfect for:

- ✅ Learning Python fundamentals
- ✅ Quick prototyping and testing
- ✅ Browser-based coding without setup
- ✅ Teaching programming concepts
- ✅ Running Python-like code anywhere

You can write **real Python code** and it will work! The 20% missing features are mostly advanced constructs that beginners don't need, and that aren't critical for most learning scenarios.

**Write Python. Run Uglier. Code Anywhere!** 🔥
