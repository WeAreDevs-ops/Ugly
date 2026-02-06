# uglier.py - Uglier Phase 9 Full Python Replacement
import sys, math, os, builtins

# -------------------------
# Global environment
# -------------------------
variables = {}
functions = {}
classes = {}

# Helper to evaluate expressions
def eval_expr(expr):
    expr = expr.strip()
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    if expr.startswith("'") and expr.endswith("'"):
        return expr[1:-1]
    if expr in variables:
        return variables[expr]
    try:
        return eval(expr, {"__builtins__": None}, variables)
    except Exception:
        raise Exception(f"Cannot evaluate: {expr}")

# -------------------------
# Core execution
# -------------------------
def execute_line(line):
    line = line.strip()
    if not line:
        return

    # -------------------------
    # Variable assignment
    # -------------------------
    if line.startswith("let "):
        parts = line[4:].split("=", 1)
        if len(parts) != 2:
            raise Exception("Invalid let syntax")
        var, val = parts[0].strip(), parts[1].strip()
        variables[var] = eval_expr(val)
        return

    # -------------------------
    # Print
    # -------------------------
    if line.startswith("print "):
        val = line[6:].strip()
        print(eval_expr(val))
        return

    # -------------------------
    # Imports
    # -------------------------
    if line.startswith("import "):
        module_name = line[7:].strip()
        if module_name not in sys.modules:
            globals()[module_name] = __import__(module_name)
        return

    # -------------------------
    # Function definition
    # -------------------------
    if line.startswith("def "):
        name_args = line[4:].split("(", 1)
        if len(name_args) != 2:
            raise Exception("Invalid def syntax")
        name, args = name_args[0].strip(), name_args[1].rstrip("):").strip()
        functions[name] = {"args": [a.strip() for a in args.split(",") if a], "body": []}
        global current_function
        current_function = name
        global in_block
        in_block = True
        return

    # -------------------------
    # Class definition
    # -------------------------
    if line.startswith("class "):
        class_name = line[6:].split(":")[0].strip()
        classes[class_name] = {"body": []}
        global current_class
        current_class = class_name
        global in_block
        in_block = True
        return

    # -------------------------
    # Control flow (if/else/while/for)
    # -------------------------
    # Note: basic example, can expand
    if line.startswith("if ") or line.startswith("elif ") or line.startswith("else:") or line.startswith("while "):
        try:
            exec(line, {"__builtins__": None}, variables)
        except Exception as e:
            raise Exception(f"Error in control flow: {e}")
        return

    # -------------------------
    # Function call
    # -------------------------
    if "(" in line and line.endswith(")"):
        # naive call
        func_name = line.split("(")[0].strip()
        if func_name in functions:
            print(f"Calling user function: {func_name}")
        else:
            # try built-in
            try:
                eval(line, {"__builtins__": None}, variables)
            except Exception as e:
                raise Exception(f"Cannot call function: {func_name} -> {e}")
        return

    # -------------------------
    # Fallback eval
    # -------------------------
    eval_expr(line)

# -------------------------
# Multi-line block execution
# -------------------------
def execute_block(lines):
    global in_block, current_function, current_class
    in_block = False
    current_function = None
    current_class = None
    for line in lines:
        execute_line(line)
