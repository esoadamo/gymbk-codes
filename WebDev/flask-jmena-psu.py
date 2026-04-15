from flask import Flask, render_template
from flask import request

app = Flask("jmena psu")
jmena_psu = []

@app.route('/', methods=["GET", "POST"])
def uvoka():
    jmeno = ""
    if request.method == "POST":
        jmeno = request.form['jmeno']
        jmena_psu.append(jmeno)
    # Pes.html ve slozce templates
    return render_template(
        "pes.html",
        jmeno=jmeno,
        jmena_psu=jmena_psu
    )


if __name__ == "__main__":
    app.run()
