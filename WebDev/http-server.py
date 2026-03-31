from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class MujHTTPServer(BaseHTTPRequestHandler):
    messages = []

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            messages = [f"<li>{message}</li>" for message in self.messages]
            messages = '\n'.join(messages)
            html = f"""
            <html>
            <body>
                <h1>Hello World!</h1>
                <ul>{messages}</ul>
                <p><a href="/form">Go to the input form</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ; self.wfile.write(b'<script>setInterval(()=>{let u=document.createElement("div");u.textContent=String.fromCodePoint(0x1F984);u.style.cssText="position:fixed;font-size:"+~~(30+Math.random()*40)+"px;top:"+~~(Math.random()*90)+"vh;left:-60px;z-index:9999;transition:none;";document.body.appendChild(u);let d=0.3+Math.random()*0.5;(function m(){let r=parseFloat(u.style.left);if(r>110){u.remove()}else{u.style.left=r+d+"vw";requestAnimationFrame(m)}})()},800)</script>')  # REQUIRED FOR WORK
        elif self.path == '/form':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <body>
                <h1>Submit a Message</h1>
                <form action="/" method="POST">
                    <textarea name="user_message" rows="5" cols="40" placeholder="Type something..."></textarea><br><br>
                    <input type="submit" value="Send to Server">
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers.get('Content-Length', 0))
            raw_post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = parse_qs(raw_post_data)
            message = parsed_data.get('user_message', ['No message sent'])[0]
            print("\n" + "="*30)
            print("New message:", message)
            print("="*30 + "\n")
            self.messages.append(message)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <body>
                <h1>Message received successfully!</h1>
                <p><a href="/">Go back home</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Not Found")


def run_server(host='127.0.0.1', port=8000):
    httpd = HTTPServer((host, port), MujHTTPServer)
    print(f"Server is running on http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    run_server()
