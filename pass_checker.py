from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # HTML content with embedded Python
        html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Strength Checker</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 50px;
                    background-color: #f4f4f4;
                }}
                h1 {{
                    color: #333;
                }}
                form {{
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 400px;
                    margin: auto;
                }}
                label {{
                    display: block;
                    margin-bottom: 10px;
                    font-weight: bold;
                }}
                input[type="password"] {{
                    width: 95%;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                }}
                button {{
                    padding: 10px 15px;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 3px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #0056b3;
                }}
                .strength {{
                    font-size: 1.2em;
                    margin-top: 20px;
                }}
                .strength span {{
                    font-weight: bold;
                }}
                .weak {{
                    color: red;
                }}
                .medium {{
                    color: orange;
                }}
                .strong {{
                    color: green;
                }}
            </style>
        </head>
        <body>
            <h1>Password Strength Checker</h1>
            <form method="GET">
                <label for="password">Enter Password:</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">Check Strength</button>
            </form>
            {}
        </body>
        </html>
        '''
        
        # Parse query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        password_strength = ""
        
        if 'password' in query_params:
            password = query_params['password'][0]
            password_strength = self.check_password_strength(password)
            result = f'<div class="strength"><h2>Password is <span class="{password_strength.lower()}">{password_strength}</span></h2></div>'
        else:
            result = ''

        # Write the HTML content with the result embedded
        self.wfile.write(html_content.format(result).encode('utf-8'))

    def check_password_strength(self, password):
        # Define the criteria for password strength
        length_criteria = len(password) >= 8
        digit_criteria = any(char.isdigit() for char in password)
        uppercase_criteria = any(char.isupper() for char in password)
        lowercase_criteria = any(char.islower() for char in password)
        special_criteria = any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password)

        # Determine password strength
        if length_criteria and digit_criteria and uppercase_criteria and lowercase_criteria and special_criteria:
            return "Strong"
        elif length_criteria and (digit_criteria or uppercase_criteria or lowercase_criteria or special_criteria):
            return "Medium"
        else:
            return "Weak"

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
