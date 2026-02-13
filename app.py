from flask import Flask, request, render_template, redirect, url_for, session
import subprocess

app = Flask(__name__)
app.secret_key = "crypto_lab_secret_key"

@app.route("/", methods=["GET", "POST"])
def shift_cipher():
    output = ""
    error = ""
    
    # Read the code file
    with open("shiftc.py", "r") as f:
        code = f.read()

    if request.method == "POST":
        try:
            key = request.form["key"]
            text = request.form["text"]
            
            # Store form values in session to preserve them after redirect
            session["shift_key"] = key
            session["shift_text"] = text

            process = subprocess.run(
                ["python", "shiftc.py"],
                input=f"{key}\n{text}\n",
                text=True,
                capture_output=True
            )

            session["output"] = process.stdout
        except Exception as e:
            session["error"] = f"Error: {str(e)}"
        
        return redirect(url_for("shift_cipher"))
    
    # Get from session and clear
    output = session.pop("output", "")
    error = session.pop("error", "")
    key = session.pop("shift_key", "")
    text = session.pop("shift_text", "")

    return render_template("index.html", output=output, error=error, code=code, key=key, text=text)

@app.route("/hill", methods=["GET", "POST"])
def hill_cipher():
    output = ""
    error = ""
    
    # Read the code file
    with open("hillc.py", "r") as f:
        code = f.read()

    if request.method == "POST":
        try:
            text = request.form["text"]
            keysize = request.form["keysize"]
            matrix = request.form["matrix"]
            
            # Store form values in session to preserve them after redirect
            session["hill_text"] = text
            session["hill_keysize"] = keysize
            session["hill_matrix"] = matrix
            
            # Clean up matrix input - remove extra whitespace and ensure proper formatting
            matrix_lines = [line.strip() for line in matrix.strip().split('\n') if line.strip()]
            matrix_formatted = '\n'.join(matrix_lines)
            
            # Format input for hillc.py: text, keysize, then matrix rows
            input_data = f"{text}\n{keysize}\n{matrix_formatted}\n"

            process = subprocess.run(
                ["python", "hillc.py"],
                input=input_data,
                text=True,
                capture_output=True
            )

            # Filter output to show only results
            full_output = process.stdout + process.stderr
            
            # Remove input prompts from output
            lines_to_remove = [
                "*** HILL CIPHER (ENCRYPTION + DECRYPTION) ***",
                "Enter the plain text:",
                "Enter key size n (e.g., 2 or 3):",
            ]
            filtered_lines = []
            for line in full_output.split('\n'):
                # Skip lines that are prompts or matrix input prompts
                if any(prompt in line for prompt in lines_to_remove):
                    continue
                if "matrix as key (each row space-separated):" in line:
                    continue
                filtered_lines.append(line)
            
            filtered_output = '\n'.join(filtered_lines).strip()
            
            session["hill_output"] = filtered_output
        except Exception as e:
            session["hill_error"] = f"Error: {str(e)}"
        
        return redirect(url_for("hill_cipher"))
    
    # Get from session and clear
    output = session.pop("hill_output", "")
    error = session.pop("hill_error", "")
    text = session.pop("hill_text", "")
    keysize = session.pop("hill_keysize", "")
    matrix = session.pop("hill_matrix", "")

    return render_template("hill.html", output=output, error=error, code=code, text=text, keysize=keysize, matrix=matrix)

@app.route("/playfair", methods=["GET", "POST"])
def playfair_cipher():
    output = ""
    error = ""
    
    # Read the code file
    with open("playfair.py", "r") as f:
        code = f.read()

    if request.method == "POST":
        try:
            key = request.form["key"]
            text = request.form["text"]
            
            # Store form values in session to preserve them after redirect
            session["playfair_key"] = key
            session["playfair_text"] = text

            process = subprocess.run(
                ["python", "playfair.py"],
                input=f"{key}\n{text}\n",
                text=True,
                capture_output=True
            )

            session["playfair_output"] = process.stdout
        except Exception as e:
            session["playfair_error"] = f"Error: {str(e)}"
        
        return redirect(url_for("playfair_cipher"))
    
    # Get from session and clear
    output = session.pop("playfair_output", "")
    error = session.pop("playfair_error", "")
    key = session.pop("playfair_key", "")
    text = session.pop("playfair_text", "")

    return render_template("playfair.html", output=output, error=error, code=code, key=key, text=text)

@app.route("/des", methods=["GET", "POST"])
def des_cipher():
    output = ""
    error = ""
    
    # Read the code file
    with open("des.py", "r") as f:
        code = f.read()

    if request.method == "POST":
        try:
            plaintext = request.form["plaintext"]
            key = request.form["key"]
            
            # Store form values in session to preserve them after redirect
            session["des_plaintext"] = plaintext
            session["des_key"] = key
            
            # Validate hex input
            if len(plaintext) != 16 or not all(c in '0123456789ABCDEFabcdef' for c in plaintext):
                raise ValueError("Plaintext must be exactly 16 hex characters (64 bits)")
            if len(key) != 16 or not all(c in '0123456789ABCDEFabcdef' for c in key):
                raise ValueError("Key must be exactly 16 hex characters (64 bits)")

            process = subprocess.run(
                ["python", "des.py"],
                input=f"{plaintext}\n{key}\n",
                text=True,
                capture_output=True
            )

            # Filter output to remove input prompts
            full_output = process.stdout + process.stderr
            lines_to_remove = [
                "Enter 64-bit Plaintext (HEX):",
                "Enter 64-bit Key (HEX):",
            ]
            filtered_lines = []
            for line in full_output.split('\n'):
                if any(prompt in line for prompt in lines_to_remove):
                    continue
                filtered_lines.append(line)
            
            filtered_output = '\n'.join(filtered_lines).strip()
            session["des_output"] = filtered_output
        except ValueError as e:
            session["des_error"] = f"Error: {str(e)}"
        except Exception as e:
            session["des_error"] = f"Error: {str(e)}"
        
        return redirect(url_for("des_cipher"))
    
    # Get from session and clear
    output = session.pop("des_output", "")
    error = session.pop("des_error", "")
    plaintext = session.pop("des_plaintext", "")
    key = session.pop("des_key", "")

    return render_template("des.html", output=output, error=error, code=code, plaintext=plaintext, key=key)

@app.route("/primality", methods=["GET", "POST"])
def primality_test():
    output = ""
    error = ""
    
    # Read the code file
    with open("primality_test.py", "r") as f:
        code = f.read()

    if request.method == "POST":
        try:
            number = request.form["number"]
            method = request.form["method"]
            
            # Store form values in session to preserve them after redirect
            session["primality_number"] = number
            session["primality_method"] = method
            
            # Validate input
            num = int(number)
            if num < 1:
                raise ValueError("Please enter a positive integer.")

            process = subprocess.run(
                ["python", "primality_test.py"],
                input=f"{number}\n{method}\n",
                text=True,
                capture_output=True
            )

            # Filter output to remove input prompts
            full_output = process.stdout + process.stderr
            lines_to_remove = [
                "Enter number to test primality:",
                "Choose Method:",
                "1. Euclidean Method",
                "2. Fermat Test",
                "3. Miller–Rabin Test",
                "Enter choice (1/2/3):",
            ]
            filtered_lines = []
            for line in full_output.split('\n'):
                if any(prompt in line for prompt in lines_to_remove):
                    continue
                filtered_lines.append(line)
            
            filtered_output = '\n'.join(filtered_lines).strip()
            session["primality_output"] = filtered_output
        except ValueError as e:
            session["primality_error"] = f"Error: {str(e)}"
        except Exception as e:
            session["primality_error"] = f"Error: {str(e)}"
        
        return redirect(url_for("primality_test"))
    
    # Get from session and clear
    output = session.pop("primality_output", "")
    error = session.pop("primality_error", "")
    number = session.pop("primality_number", "")
    method = session.pop("primality_method", "1")

    return render_template("primality.html", output=output, error=error, code=code, number=number, method=method)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
