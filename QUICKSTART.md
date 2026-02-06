# Uglier - Quick Start Guide

## What is Uglier?

Uglier is a simplified Python-like programming language that you can code with in your browser! It features:

- Easy-to-learn syntax similar to Python
- Variables, functions, loops, and conditionals
- Lists, dictionaries, and other data structures
- Built-in functions and math operations
- A beautiful web interface for live coding

## Installation & Setup

### Option 1: Run Locally (Recommended)

1. Make sure you have Python 3.7+ installed
2. Install dependencies:
   ```bash
   pip install Flask==2.3.3
   ```
3. Start the server:
   ```bash
   python server.py
   ```
4. Open your browser to: `http://localhost:5000`

### Option 2: Command Line REPL

Run the interpreter directly:
```bash
python uglier.py
```

## Quick Examples

### Hello World
```python
let message = "Hello, World!"
print message
```

### Variables and Math
```python
let x = 10
let y = 20
print "Sum:", x + y
print "Product:", x * y
```

### Lists and Loops
```python
let numbers = [1, 2, 3, 4, 5]

for num in numbers:
    print num

let total = 0
for num in numbers:
    total += num
print "Total:", total
```

### Functions
```python
def greet(name):
    return "Hello, " + name + "!"

print greet("Alice")
print greet("Bob")

def add(a, b):
    return a + b

print add(10, 20)
```

### Conditionals
```python
let age = 18

if age >= 18:
    print "You are an adult"
elif age >= 13:
    print "You are a teenager"
else:
    print "You are a child"
```

### While Loops
```python
let count = 0
while count < 5:
    print count
    count += 1
```

### Recursive Functions
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print factorial(5)  # Output: 120
```

## Web Interface Features

When you open the web interface, you'll see:

1. **Code Editor** (left side)
   - Write your Uglier code here
   - Includes preloaded examples
   - Keyboard shortcuts:
     - `Ctrl/Cmd + Enter` to run code
     - `Tab` for indentation

2. **Output Panel** (right side)
   - See your program's output
   - View current variables and functions
   - Real-time results

3. **Control Buttons**
   - **Run Code** - Execute your program
   - **Reset State** - Clear all variables and functions
   - **Clear** - Empty the code editor
   - **Example Buttons** - Load sample code

## Key Differences from Python

1. **Variable Declaration**: Use `let` for new variables
   ```python
   let x = 10  # Uglier
   x = 10      # Python
   ```

2. **Print Syntax**: No parentheses needed
   ```python
   print x     # Uglier
   print(x)    # Python
   ```

3. **String Concatenation**: Direct with +
   ```python
   print "Hello " + name  # Uglier
   print(f"Hello {name}") # Python
   ```

## Testing Your Installation

Run the test suite to verify everything works:
```bash
python test_uglier.py
```

You should see: "Success rate: 100.0%"

## Common Tasks

### Working with Lists
```python
let fruits = ["apple", "banana", "cherry"]
print len(fruits)
print fruits[0]

for fruit in fruits:
    print fruit
```

### Working with Dictionaries
```python
let person = {"name": "Alice", "age": 30}
print person["name"]
print person["age"]
```

### Using Math Functions
```python
import math

print math.sqrt(16)
print math.pi
print math.pow(2, 3)
```

### Multiple Assignments
```python
let x, y = 10, 20
print x
print y
```

### Compound Assignment
```python
let x = 10
x += 5   # x = x + 5
x *= 2   # x = x * 2
print x  # Output: 30
```

## Tips for Success

1. **Indentation Matters**: Like Python, use consistent indentation (4 spaces recommended)
2. **Error Messages**: Read error messages carefully - they tell you what went wrong
3. **Test Incrementally**: Run your code frequently to catch errors early
4. **Use Examples**: Click the example buttons to see working code
5. **State Management**: Use "Reset State" if you want to start fresh

## Next Steps

1. Try the examples in the web interface
2. Experiment with modifying the example code
3. Write your own programs
4. Check out README.md for full documentation
5. Run test_uglier.py to see all features in action

## Need Help?

- Check the README.md for detailed documentation
- Look at test_uglier.py for code examples
- Examine the example buttons in the web interface
- The error messages will guide you to fix issues

## Have Fun!

Uglier is designed to make programming fun and accessible. Start simple, experiment, and gradually build more complex programs. Happy coding! 🔥
