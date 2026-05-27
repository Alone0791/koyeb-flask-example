from flask import Flask, request, jsonify
import sys
import io
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return "Python Code Runner API is running"

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()

    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    code = data["code"]

    # Output capture
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer

    try:
        # ⚠️ WARNING: executes raw code
        exec(code, {})
        output = stdout_buffer.getvalue()
        error = stderr_buffer.getvalue()

        if error:
            return jsonify({"status": "error", "error": error})

        if output.strip():
            return jsonify({"status": "success", "output": output})

        return jsonify({"status": "success", "message": "No output, executed successfully"})

    except Exception:
        return jsonify({
            "status": "error",
            "error": traceback.format_exc()
        })

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


if __name__ == "__main__":
    app.run()