import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import altair as alt
    import matplotlib.pyplot as plt

    # https://github.com/datasciencedojo/datasets/blob/master/titanic.csv
    titanic = pd.read_csv("titanic.csv")
    return mo, titanic


@app.cell
def _(mo, titanic):
    _df = mo.sql(
        f"""
        SELECT * FROM titanic;
        """
    )
    return


if __name__ == "__main__":
    app.run()
