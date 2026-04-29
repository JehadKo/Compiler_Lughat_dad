import os
import subprocess
from flask import Flask, request, jsonify, render_template

# 1. Initialize Flask
app = Flask(__name__)

# Set the base directory to where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Route to serve your HTML page
@app.route('/')
def index():
    # Make sure your HTML file is in a folder named 'templates'
    return render_template('index.html')

# 3. Route to handle the code execution
@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    if not data or 'code' not in data:
        return jsonify({'output': "❌ Error: No code provided", 'isError': True}), 400
        
    arabic_code = data.get('code', '')

    my_env = os.environ.copy()
    my_env["PYTHONIOENCODING"] = "utf-8"
    my_env["PYTHONUTF8"] = "1"

    try:
        # Avoid shell=True for security.
        process = subprocess.Popen(
            ['java', '-Dfile.encoding=UTF-8', '-cp', BASE_DIR, 'LughatDad.LughatDad'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=BASE_DIR,
            env=my_env
        )

        stdout, stderr = process.communicate(input=arabic_code)

        # Distinguish between error and normal output
        if stderr.strip():
            return jsonify({'output': stderr.strip(), 'isError': True})
        
        return jsonify({
            'output': stdout.strip() if stdout.strip() else "تم التنفيذ بنجاح (بدون مخرجات)", 
            'isError': False
        })

    except subprocess.SubprocessError as e:
        return jsonify({'output': f"❌ Subprocess Error: {str(e)}", 'isError': True}), 500
    except Exception as e:
        return jsonify({'output': f"❌ System Error: {str(e)}", 'isError': True}), 500

# 4. START THE SERVER
if __name__ == '__main__':
    print("--- LughatDad Server is starting! ---")
    print("--- Open http://127.0.0.1:5000 in your browser ---")
    app.run(debug=True, port=5000)
