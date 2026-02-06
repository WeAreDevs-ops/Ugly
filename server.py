from flask import Flask, request, jsonify
from uglier import execute_block
import sys

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json.get("code", "")
    output = []

    # capture print
    class Capturer:
        def write(self, txt): output.append(txt)
        def flush(self): pass

    old_stdout = sys.stdout
    sys.stdout = Capturer()

    try:
        execute_block(code.splitlines())
    except Exception as e:
        output.append(f"Error: {e}")

    sys.stdout = old_stdout
    return jsonify({"output": "".join(output)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
