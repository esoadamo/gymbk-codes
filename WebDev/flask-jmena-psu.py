from flask import Flask, render_template

app = Flask("jmena psu")

@app.route('/')
def uvoka():
    # Pes.html ve slozce templates
    return render_template("pes.html")


if __name__ == "__main__":
    app.run()
