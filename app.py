from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import io
import traceback

app = Flask(__name__)

# -------------------------
# HOME UI
# -------------------------
@app.route('/')
def home():
    return render_template("index.html")

# -------------------------
# TERMINAL COMMAND RUNNER
# -------------------------
@app.route('/terminal', methods=['POST'])
def terminal():
    cmd = request.json.get("cmd")

    try:
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True
        )
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"output": str(e)})

# -------------------------
# PYTHON CODE RUNNER
# -------------------------
@app.route('/run', methods=['POST'])
def run_python():
    code = request.json.get("code")

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer

    try:
        exec(code, {})
        output = stdout_buffer.getvalue()
        error = stderr_buffer.getvalue()

        if error:
            return jsonify({"output": error})

        if output.strip():
            return jsonify({"output": output})

        return jsonify({"output": "Executed successfully (no output)"})

    except Exception:
        return jsonify({"output": traceback.format_exc()})

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)