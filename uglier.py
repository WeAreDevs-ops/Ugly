# uglier.py - 80% Python-Compatible Interpreter
# Accepts both standard Python syntax AND simplified Uglier syntax
import sys
import math
import os
import re

# -------------------------
# Global environment
# -------------------------
variables = {}
functions = {}
classes = {}
return_value = None
in_return = False

# -------------------------
# Helper functions
# -------------------------
def parse_value(val):
    """Parse a value (string, number, bool, list, dict, etc.)"""
    val = val.strip()
    
    # String literals
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    
    # Boolean
    if val == "True":
        return True
    if val == "False":
        return False
    
    # None
    if val == "None":
        return None
    
    # List literal
    if val.startswith("[") and val.endswith("]"):
        if val == "[]":
            return []
        items = split_by_comma(val[1:-1])
        return [eval_expr(item) for item in items]
    
    # Dict literal
    if val.startswith("{") and val.endswith("}"):
        if val == "{}":
            return {}
        items = split_by_comma(val[1:-1])
        result = {}
        for item in items:
            if ":" in item:
                k, v = item.split(":", 1)
                result[eval_expr(k.strip())] = eval_expr(v.strip())
        return result
    
    # Tuple literal
    if val.startswith("(") and val.endswith(")"):
        items = split_by_comma(val[1:-1])
        return tuple(eval_expr(item) for item in items)
    
    # Variable reference
    if val in variables:
        return variables[val]
    
    # Number
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        pass
    
    # Try to evaluate as expression
    return eval_expr(val)

def split_by_comma(expr):
    """Split expression by commas, respecting parentheses and brackets"""
    parts = []
    current = ""
    depth = 0
    
    for char in expr:
        if char in "([{":
            depth += 1
            current += char
        elif char in ")]}":
            depth -= 1
            current += char
        elif char == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    
    if current.strip():
        parts.append(current.strip())
    
    return parts

def eval_expr(expr):
    """Evaluate an expression - handles both Python and Uglier syntax"""
    expr = expr.strip()
    
    if not expr:
        return None
    
    # Handle string literals
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]
    
    # Handle boolean and None
    if expr == "True":
        return True
    if expr == "False":
        return False
    if expr == "None":
        return None
    
    # Handle list/dict/tuple literals
    if expr.startswith("[") or expr.startswith("{") or (expr.startswith("(") and expr.endswith(")")):
        return parse_value(expr)
    
    # Handle variable references
    if expr in variables:
        return variables[expr]
    
    # Handle attribute access (e.g., obj.method())
    if "." in expr and "(" in expr:
        obj_part = expr.split(".")[0].strip()
        if obj_part in variables:
            try:
                return eval(expr, {"__builtins__": {}}, variables)
            except:
                pass
    
    # Handle indexing (e.g., list[0])
    if "[" in expr and "]" in expr and not expr.startswith("["):
        var_name = expr.split("[")[0].strip()
        if var_name in variables:
            try:
                return eval(expr, {"__builtins__": {}}, variables)
            except Exception as e:
                raise Exception(f"Indexing error: {e}")
    
    # Handle function calls - check user functions first
    if "(" in expr and ")" in expr:
        # Simple function call
        match = re.match(r'^(\w+)\((.*)\)$', expr)
        if match:
            func_name = match.group(1)
            args_str = match.group(2)
            
            if func_name in functions:
                args = []
                if args_str.strip():
                    args = [eval_expr(arg) for arg in split_by_comma(args_str)]
                return call_function(func_name, args)
        
        # Complex expressions with function calls
        temp_expr = expr
        while True:
            found = False
            for func_name in functions:
                pattern = rf'{func_name}\([^()]*\)'
                matches = re.finditer(pattern, temp_expr)
                for match in matches:
                    func_call = match.group(0)
                    args_str = func_call[len(func_name)+1:-1]
                    args = []
                    if args_str.strip():
                        args = [eval_expr(arg) for arg in split_by_comma(args_str)]
                    result = call_function(func_name, args)
                    temp_expr = temp_expr.replace(func_call, str(result), 1)
                    found = True
                    break
                if found:
                    break
            if not found:
                break
        
        if temp_expr != expr:
            expr = temp_expr
    
    # Built-in functions
    if "(" in expr and expr.endswith(")"):
        func_name = expr.split("(")[0].strip()
        
        builtins_map = {
            "print": print,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "sorted": sorted,
            "reversed": reversed,
            "round": round,
            "type": type,
            "isinstance": isinstance,
            "input": input,
            "pow": pow,
            "all": all,
            "any": any,
            "chr": chr,
            "ord": ord,
        }
        
        args_str = expr[expr.index("(")+1:-1]
        args = []
        if args_str.strip():
            args = [eval_expr(arg) for arg in split_by_comma(args_str)]
        
        if func_name in builtins_map:
            return builtins_map[func_name](*args)
        
        if hasattr(math, func_name):
            return getattr(math, func_name)(*args)
    
    # Handle arithmetic and comparison
    try:
        safe_dict = {
            "__builtins__": {},
            "math": math,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            "range": range,
            "pow": pow,
        }
        safe_dict.update(variables)
        
        return eval(expr, safe_dict)
    except Exception as e:
        raise Exception(f"Cannot evaluate expression '{expr}': {e}")

def call_function(func_name, args):
    """Call a user-defined function"""
    global return_value, in_return
    
    if func_name not in functions:
        raise Exception(f"Function '{func_name}' not defined")
    
    func = functions[func_name]
    func_args = func["args"]
    func_body = func["body"]
    
    if len(args) != len(func_args):
        raise Exception(f"Function '{func_name}' expects {len(func_args)} arguments, got {len(args)}")
    
    saved_vars = {}
    for arg_name in func_args:
        if arg_name in variables:
            saved_vars[arg_name] = variables[arg_name]
    
    for i, arg_name in enumerate(func_args):
        variables[arg_name] = args[i]
    
    return_value = None
    in_return = False
    
    try:
        execute_block(func_body)
    finally:
        for arg_name in func_args:
            if arg_name in saved_vars:
                variables[arg_name] = saved_vars[arg_name]
            elif arg_name in variables:
                del variables[arg_name]
    
    result = return_value
    return_value = None
    in_return = False
    return result

# -------------------------
# Core execution
# -------------------------
def execute_line(line):
    """Execute a single line - accepts Python OR Uglier syntax"""
    global return_value, in_return
    
    line = line.strip()
    
    if not line or line.startswith("#"):
        return
    
    # Return statement
    if line.startswith("return "):
        return_value = eval_expr(line[7:].strip())
        in_return = True
        return
    
    # Variable assignment - accept both "let x = 10" AND "x = 10"
    if line.startswith("let "):
        line = line[4:].strip()
    
    if "=" in line and not any(op in line for op in ["==", "!=", "<=", ">=", "+=", "-=", "*=", "/="]):
        parts = line.split("=", 1)
        if len(parts) == 2:
            var_name = parts[0].strip()
            val_expr = parts[1].strip()
            
            if "[" in var_name and "]" in var_name:
                base_var = var_name.split("[")[0].strip()
                if base_var in variables:
                    exec(f"{line}", {"__builtins__": {}}, variables)
                    return
            elif "." in var_name:
                exec(f"{line}", {"__builtins__": {}}, variables)
                return
            else:
                if "," in var_name:
                    var_names = [v.strip() for v in var_name.split(",")]
                    values = split_by_comma(val_expr)
                    if len(var_names) != len(values):
                        raise Exception("Number of variables doesn't match number of values")
                    for vn, ve in zip(var_names, values):
                        variables[vn] = eval_expr(ve)
                else:
                    variables[var_name] = eval_expr(val_expr)
                return
    
    # Compound assignment
    for op in ["+=", "-=", "*=", "/=", "//=", "%=", "**="]:
        if op in line:
            parts = line.split(op, 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                val_expr = parts[1].strip()
                if var_name in variables:
                    current = variables[var_name]
                    new_val = eval_expr(val_expr)
                    if op == "+=":
                        variables[var_name] = current + new_val
                    elif op == "-=":
                        variables[var_name] = current - new_val
                    elif op == "*=":
                        variables[var_name] = current * new_val
                    elif op == "/=":
                        variables[var_name] = current / new_val
                    elif op == "//=":
                        variables[var_name] = current // new_val
                    elif op == "%=":
                        variables[var_name] = current % new_val
                    elif op == "**=":
                        variables[var_name] = current ** new_val
                    return
    
    # Print - accept both "print x" AND "print(x)"
    if line.startswith("print ") or line.startswith("print("):
        if line.startswith("print(") and line.endswith(")"):
            val_expr = line[6:-1].strip()
        else:
            val_expr = line[6:].strip()
        
        if not val_expr:
            print()
        else:
            if "," in val_expr and not ('"' in val_expr or "'" in val_expr):
                values = split_by_comma(val_expr)
                results = [str(eval_expr(v)) for v in values]
                print(" ".join(results))
            else:
                result = eval_expr(val_expr)
                print(result)
        return
    
    # Import - full Python syntax support
    if line.startswith("import ") or line.startswith("from "):
        try:
            if line.startswith("from "):
                match = re.match(r'from\s+(\w+)\s+import\s+(.+)', line)
                if match:
                    module_name = match.group(1)
                    imports = match.group(2).strip()
                    mod = __import__(module_name)
                    
                    if imports == "*":
                        for name in dir(mod):
                            if not name.startswith("_"):
                                variables[name] = getattr(mod, name)
                    else:
                        for item in imports.split(","):
                            item = item.strip()
                            variables[item] = getattr(mod, item)
            else:
                module_name = line[7:].strip()
                if module_name not in sys.modules:
                    mod = __import__(module_name)
                    variables[module_name] = mod
                    globals()[module_name] = mod
        except ImportError as e:
            raise Exception(f"Cannot import module: {e}")
        return
    
    # Pass statement
    if line == "pass":
        return
    
    # Break and continue
    if line in ["break", "continue"]:
        return
    
    # Expression evaluation
    result = eval_expr(line)
    return result

# -------------------------
# Multi-line block execution
# -------------------------
def execute_block(lines):
    """Execute a block with proper indentation handling"""
    global in_return
    
    i = 0
    while i < len(lines):
        if in_return:
            break
            
        line = lines[i].rstrip()
        
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        
        indent = len(line) - len(line.lstrip())
        line = line.strip()
        
        # Function definition
        if line.startswith("def "):
            match = re.match(r'def\s+(\w+)\s*\((.*?)\)\s*:', line)
            if not match:
                raise Exception(f"Invalid function definition: {line}")
            
            func_name = match.group(1)
            args_str = match.group(2).strip()
            args = [a.strip() for a in args_str.split(",")] if args_str else []
            
            body = []
            i += 1
            base_indent = None
            while i < len(lines):
                body_line = lines[i].rstrip()
                if not body_line.strip():
                    i += 1
                    continue
                body_indent = len(body_line) - len(body_line.lstrip())
                if body_indent <= indent:
                    break
                if base_indent is None:
                    base_indent = body_indent
                relative_indent = body_indent - base_indent
                body.append(' ' * relative_indent + body_line.strip())
                i += 1
            
            functions[func_name] = {"args": args, "body": body}
            continue
        
        # Class definition
        if line.startswith("class "):
            match = re.match(r'class\s+(\w+)(\(.*?\))?\s*:', line)
            if not match:
                raise Exception(f"Invalid class definition: {line}")
            
            class_name = match.group(1)
            
            body = []
            i += 1
            while i < len(lines):
                body_line = lines[i].rstrip()
                if not body_line.strip():
                    i += 1
                    continue
                body_indent = len(body_line) - len(body_line.lstrip())
                if body_indent <= indent:
                    break
                body.append(body_line.strip())
                i += 1
            
            classes[class_name] = {"body": body}
            variables[class_name] = type(class_name, (), {})
            continue
        
        # If/elif/else
        if line.startswith("if ") or line.startswith("elif ") or line.startswith("else:") or line == "else":
            condition_result = False
            
            if line.startswith("if "):
                condition = line[3:].rstrip(":")
                condition_result = bool(eval_expr(condition))
            elif line.startswith("elif "):
                condition = line[5:].rstrip(":")
                condition_result = bool(eval_expr(condition))
            elif line.startswith("else:") or line == "else":
                condition_result = True
            
            body = []
            i += 1
            while i < len(lines):
                body_line = lines[i].rstrip()
                if not body_line.strip():
                    i += 1
                    continue
                body_indent = len(body_line) - len(body_line.lstrip())
                if body_indent <= indent:
                    break
                body.append(body_line)
                i += 1
            
            if condition_result:
                execute_block(body)
                
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith("elif ") or next_line.startswith("else:") or next_line == "else":
                        i += 1
                        while i < len(lines):
                            skip_line = lines[i].rstrip()
                            if not skip_line.strip():
                                i += 1
                                continue
                            skip_indent = len(skip_line) - len(skip_line.lstrip())
                            if skip_indent <= indent:
                                break
                            i += 1
                    else:
                        break
            
            continue
        
        # While loop
        if line.startswith("while "):
            condition = line[6:].rstrip(":")
            
            body = []
            i += 1
            while i < len(lines):
                body_line = lines[i].rstrip()
                if not body_line.strip():
                    i += 1
                    continue
                body_indent = len(body_line) - len(body_line.lstrip())
                if body_indent <= indent:
                    break
                body.append(body_line)
                i += 1
            
            max_iterations = 100000
            iteration = 0
            while bool(eval_expr(condition)):
                iteration += 1
                if iteration > max_iterations:
                    raise Exception("While loop exceeded maximum iterations")
                execute_block(body)
            
            continue
        
        # For loop
        if line.startswith("for "):
            match = re.match(r'for\s+(\w+)\s+in\s+(.+?):', line)
            if not match:
                raise Exception(f"Invalid for loop syntax: {line}")
            
            var_name = match.group(1)
            iterable_expr = match.group(2)
            
            body = []
            i += 1
            while i < len(lines):
                body_line = lines[i].rstrip()
                if not body_line.strip():
                    i += 1
                    continue
                body_indent = len(body_line) - len(body_line.lstrip())
                if body_indent <= indent:
                    break
                body.append(body_line)
                i += 1
            
            iterable = eval_expr(iterable_expr)
            saved_var = variables.get(var_name)
            
            for item in iterable:
                variables[var_name] = item
                execute_block(body)
            
            if saved_var is not None:
                variables[var_name] = saved_var
            elif var_name in variables:
                del variables[var_name]
            
            continue
        
        # Try/except
        if line.startswith("try:") or line == "try":
            try_body = []
            i += 1
            while i < len(lines):
                body_line = lines[i].rstrip()
                if not body_line.strip():
                    i += 1
                    continue
                body_indent = len(body_line) - len(body_line.lstrip())
                if body_indent <= indent:
                    break
                try_body.append(body_line)
                i += 1
            
            except_body = []
            if i < len(lines) and lines[i].strip().startswith("except"):
                i += 1
                while i < len(lines):
                    body_line = lines[i].rstrip()
                    if not body_line.strip():
                        i += 1
                        continue
                    body_indent = len(body_line) - len(body_line.lstrip())
                    if body_indent <= indent:
                        break
                    except_body.append(body_line)
                    i += 1
            
            try:
                execute_block(try_body)
            except Exception:
                if except_body:
                    execute_block(except_body)
            
            continue
        
        # Regular statement
        execute_line(line)
        i += 1

# -------------------------
# Main REPL
# -------------------------
if __name__ == "__main__":
    print("Welcome to Uglier - 80% Python-Compatible Interpreter")
    print("Accepts both Python and Uglier syntax!")
    print("Type 'exit' or 'quit' to exit")
    print()
    
    try:
        while True:
            try:
                inp = input(">>> ").strip()
                if inp.lower() in ("exit", "quit"):
                    break
                if inp:
                    execute_block([inp])
            except Exception as e:
                print(f"Error: {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
