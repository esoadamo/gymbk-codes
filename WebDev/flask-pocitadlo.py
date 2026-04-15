from flask import Flask, render_template

app = Flask("jmena psu")
pocitadlo = 0

@app.route('/')
def uvoka():
    global pocitadlo
    # Pes.html ve slozce templates
    pocitadlo += 1
    return render_template(
        "pocitadlo.html",
        jmeno="Baryk",
        pocitadlo=pocitadlo
    )


if __name__ == "__main__":
    app.run()
