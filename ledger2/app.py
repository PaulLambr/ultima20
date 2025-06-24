from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/run_ledger2", methods=["POST"])
def run_ledger2():
    try:
        print("📨 Received export trigger...")
        result = subprocess.run(["python", "ledger2.py"], capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Error running script:")
            print(result.stderr)
            return jsonify({"status": "error", "details": result.stderr}), 500

        print("✅ Script completed:")
        print(result.stdout)
        return jsonify({"status": "success", "output": result.stdout})

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
