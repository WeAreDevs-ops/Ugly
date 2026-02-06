# Uglier Interpreter Phase 6 - Roblox ready
import sys
import requests

variables = {}
functions = {}

# Roblox helper functions
def roblox_get_user(username_or_id):
    url = f"https://users.roblox.com/v1/users/{username_or_id}" if username_or_id.isdigit() else f"https://api.roblox.com/users/get-by-username?username={username_or_id}"
    r = requests.get(url)
    return r.json()

def roblox_get_game(game_id):
    url = f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={game_id}"
    r = requests.get(url)
    return r.json()

# Expression evaluator
def eval_expr(expr):
    expr = expr.strip()
    
    # Handle arrays
    if expr.startswith("[") and expr.endswith("]"):
        items = expr[1:-1].split(",")
        return [eval_expr(x) for x in items]
    
    # Array indexing: arr[0]
    if "[" in expr and "]" in expr:
        var_name, index = expr.split("[")
        index = int(index[:-1])
        if var_name in variables:
            return variables[var_name][index]
        else:
            print(f"Unknown variable: {var_name}")
            return None
    
    # Built-in Roblox calls
    if expr.startswith("roblox_get_user("):
        arg = expr[17:-1].strip().strip('"')
        return roblox_get_user(arg)
    if expr.startswith("roblox_get_game("):
        arg = expr[17:-1].strip()
        return roblox_get_game(arg)
    
    # Basic math
    for op in ["+", "-", "*", "/", "%"]:
        if op in expr:
            left, right = expr.split(op)
            left_val = eval_expr(left)
            right_val = eval_expr(right)
            if op == "+": return left_val + right_val
            if op == "-": return left_val - right_val
            if op == "*": return left_val * right_val
            if op == "/": return left_val // right_val
            if op == "%": return left_val % right_val

    # Variable or literal
    if expr in variables:
        return variables[expr]
    try:
        return int(expr)
    except:
        return expr.strip('"')

def execute_block(block_lines):
    i = 0
    while i < len(block_lines):
        line = block_lines[i]

        if line.startswith("print "):
            print(eval_expr(line[6:]))

        elif line.startswith("let "):
            parts = line.split("=",1)
            left = parts[0].split()[1].strip()
            right = parts[1].strip()
            variables[left] = eval_expr(right)

        elif line.startswith("call "):
            func_name = line[5:]
            if func_name in functions:
                execute_block(functions[func_name])
            else:
                print(f"Unknown function: {func_name}")

        elif line.startswith("def "):
            func_name = line[4:-1].strip()
            func_block = []
            i += 1
            while i < len(block_lines) and block_lines[i].startswith("    "):
                func_block.append(block_lines[i][4:])
                i += 1
            i -= 1
            functions[func_name] = func_block

        # For loops
        elif line.startswith("for "):
            parts = line[4:-1].split()
            var = parts[0]
            start = int(eval_expr(parts[2]))
            end = int(eval_expr(parts[3]))
            loop_block = []
            i += 1
            while i < len(block_lines) and block_lines[i].startswith("    "):
                loop_block.append(block_lines[i][4:])
                i += 1
            i -= 1
            for val in range(start, end+1):
                variables[var] = val
                execute_block(loop_block)

        # While loops
        elif line.startswith("while "):
            condition = line[6:-1].strip()
            var, op, value = condition.split()
            loop_block = []
            i += 1
            while i < len(block_lines) and block_lines[i].startswith("    "):
                loop_block.append(block_lines[i][4:])
                i += 1
            i -= 1
            def eval_condition():
                l = eval_expr(var)
                r = eval_expr(value)
                if op == "==": return l == r
                elif op == ">": return l > r
                elif op == "<": return l < r
                elif op == ">=": return l >= r
                elif op == "<=": return l <= r
                elif op == "!=": return l != r
                return False
            while eval_condition():
                execute_block(loop_block)

        # If statements
        elif line.startswith("if "):
            condition = line[3:-1].strip()
            var, op, value = condition.split()
            left = eval_expr(var)
            right = eval_expr(value)
            do_block = []
            i += 1
            while i < len(block_lines) and block_lines[i].startswith("    "):
                do_block.append(block_lines[i][4:])
                i += 1
            i -= 1
            execute = False
            if op == "==": execute = left == right
            elif op == ">": execute = left > right
            elif op == "<": execute = left < right
            elif op == ">=": execute = left >= right
            elif op == "<=": execute = left <= right
            elif op == "!=": execute = left != right
            if execute:
                execute_block(do_block)

        # Web requests
        elif line.startswith("http_get "):
            url = eval_expr(line[9:])
            try:
                r = requests.get(url)
                print(r.text[:200])
            except Exception as e:
                print("HTTP GET failed:", e)

        elif line.startswith("http_post "):
            parts = line.split()
            url = parts[1]
            data = {}
            for kv in parts[2:]:
                k,v = kv.split("=")
                data[k]=v
            try:
                r = requests.post(url, data=data)
                print(r.text[:200])
            except Exception as e:
                print("HTTP POST failed:", e)

        i += 1

# Read file
if len(sys.argv) < 2:
    print("Usage: python uglier.py <file.ug>")
    sys.exit(1)

filename = sys.argv[1]
with open(filename,"r") as f:
    lines = [l.rstrip() for l in f if l.strip() and not l.strip().startswith("#")]

# Parse functions first
i=0
while i < len(lines):
    line = lines[i]
    if line.startswith("def "):
        func_name = line[4:-1].strip()
        func_block = []
        i+=1
        while i < len(lines) and lines[i].startswith("    "):
            func_block.append(lines[i][4:])
            i+=1
        i-=1
        functions[func_name] = func_block
    i+=1

# Execute main
execute_block(lines)
