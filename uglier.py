import sys
import math
import json
import builtins

# -----------------------
# Core storage
# -----------------------
variables = {}
functions = {}
classes = {}
imports = {}

# -----------------------
# Helper: Evaluate expressions
# -----------------------
def eval_expr(expr):
    expr = expr.strip()
    # Integer / float
    try:
        return int(expr)
    except:
        try:
            return float(expr)
        except:
            pass
    # String
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    # List
    if expr.startswith('[') and expr.endswith(']'):
        return [eval_expr(i.strip()) for i in expr[1:-1].split(',') if i.strip()]
    # Dict
    if expr.startswith('{') and expr.endswith('}'):
        d = {}
        for item in expr[1:-1].split(','):
            if ':' in item:
                k,v = item.split(':',1)
                d[eval_expr(k.strip())] = eval_expr(v.strip())
        return d
    # Variable
    if expr in variables:
        return variables[expr]
    # Imported module
    if '.' in expr:
        mod, attr = expr.split('.',1)
        if mod in imports:
            return getattr(imports[mod], attr)
    # Math operations
    for op in ['+', '-', '*', '/', '%', '**']:
        if op in expr:
            left,right = expr.split(op,1)
            return eval_expr(left) + eval_expr(right) if op=='+' else \
                   eval_expr(left) - eval_expr(right) if op=='-' else \
                   eval_expr(left) * eval_expr(right) if op=='*' else \
                   eval_expr(left) / eval_expr(right) if op=='/' else \
                   eval_expr(left) % eval_expr(right) if op=='%' else \
                   eval_expr(left) ** eval_expr(right)
    return expr

# -----------------------
# Execute code block
# -----------------------
def execute_block(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        # Print
        if line.startswith("print "):
            print(eval_expr(line[6:]))

        # Variables
        elif line.startswith("let "):
            var,val = line[4:].split('=',1)
            variables[var.strip()] = eval_expr(val.strip())

        # Functions
        elif line.startswith("def "):
            fn_name = line[4:].split()[0]
            fn_lines = []
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                fn_lines.append(lines[i][4:])
                i += 1
            functions[fn_name] = fn_lines
            i -= 1

        # Call function
        elif line.startswith("call "):
            parts = line[5:].split()
            fn_name = parts[0]
            args = parts[1:]
            if fn_name in functions:
                for idx,arg in enumerate(args):
                    variables[f"arg{idx}"] = eval_expr(arg)
                execute_block(functions[fn_name])

        # If / Elif / Else
        elif line.startswith("if "):
            condition = line[3:].rstrip(':')
            true_block, false_block = [], []
            i += 1
            in_false = False
            while i < len(lines) and lines[i].startswith("    "):
                subline = lines[i][4:]
                if subline.startswith("else:") or subline.startswith("elif "):
                    in_false = True
                    false_block.append(subline)
                    i += 1
                    continue
                if not in_false:
                    true_block.append(subline)
                else:
                    false_block.append(subline)
                i += 1
            if eval_expr(condition):
                execute_block(true_block)
            else:
                execute_block(false_block)
            i -= 1

        # While loop
        elif line.startswith("while "):
            condition = line[6:].rstrip(':')
            loop_block = []
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                loop_block.append(lines[i][4:])
                i += 1
            while eval_expr(condition):
                execute_block(loop_block)
            i -= 1

        # Import module
        elif line.startswith("import "):
            mod = line[7:].strip()
            imports[mod] = __import__(mod)

        # Try / Catch / Finally
        elif line.startswith("try:"):
            try_block, catch_block, finally_block = [], [], []
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                subline = lines[i][4:]
                if subline.startswith("catch "):
                    exception_var = subline[6:].strip()
                    i += 1
                    while i < len(lines) and lines[i].startswith("        "):
                        catch_block.append(lines[i][8:])
                        i += 1
                    continue
                if subline.startswith("finally:"):
                    i += 1
                    while i < len(lines) and lines[i].startswith("        "):
                        finally_block.append(lines[i][8:])
                        i += 1
                    continue
                try_block.append(subline)
                i += 1
            try:
                execute_block(try_block)
            except Exception as e:
                variables[exception_var] = str(e)
                execute_block(catch_block)
            finally:
                execute_block(finally_block)
            i -= 1

        # File I/O
        elif line.startswith("open "):
            parts = line[5:].split()
            fname = eval_expr(parts[0])
            mode = eval_expr(parts[1])
            variables[parts[2]] = open(fname, mode)

        i += 1

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename,'r') as f:
            lines = f.readlines()
        execute_block(lines)
    else:
        print("Welcome to Uglier Phase 9 (Full Python Replacement)")
        while True:
            inp = input("uglier> ").strip()
            if inp.lower() == "exit":
                break
            try:
                execute_block([inp])
            except Exception as e:
                print("Error:", e)
