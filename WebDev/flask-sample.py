from flask import Flask

app = Flask("My app")

@app.route('/')
def uvodka():
    return "Ahoj svete!"

@app.route('/druha')
def druha():
    return "Ahoj svete 2222!"

if __name__ == "__main__":
    app.run()
