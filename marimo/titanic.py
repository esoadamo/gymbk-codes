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
    return mo, pd, plt, titanic


@app.cell
def _(mo, titanic):
    _df = mo.sql(
        f"""
        SELECT * FROM titanic;
        """
    )
    return


@app.cell
def _(mo, titanic):
    X = mo.sql(
        f"""
        CREATE OR REPLACE TABLE training AS SELECT Pclass, Sex, Age, Fare FROM titanic ORDER BY PassengerId;
        UPDATE training SET Sex=0 WHERE Sex='male';
        UPDATE training SET Sex=1 WHERE Sex='female';
        SELECT * FROM training;
        """,
        output=False
    )
    return (X,)


@app.cell
def _(mo, titanic):
    y = mo.sql(
        f"""
        SELECT Survived FROM titanic ORDER BY PassengerId;
        """,
        output=False
    )
    return (y,)


@app.cell
def _(X, plt, y):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix, classification_report
    from sklearn.tree import DecisionTreeClassifier, plot_tree

    # 1. Split the data: 70% for training, 30% for testing
    # random_state ensures we get the exact same random split every time we run this cell
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 2. Fit the model ONLY on the 70% training data
    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X_train, y_train)

    # 3. Make predictions on the 30% unseen testing data
    y_pred = clf.predict(X_test)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    # 5. Visualize the newly trained tree
    fig, ax = plt.subplots(figsize=(14, 8))
    plot_tree(
        clf, 
        feature_names=['Pclass', 'Sex', 'Age', 'Fare'], 
        class_names=['Perished', 'Survived'], 
        filled=True, 
        rounded=True, 
        fontsize=10,
        ax=ax
    )

    plt.title("Titanic Survival Decision Tree (Trained on 70% of Data)")

    # Output the figure
    fig
    return X_train, clf, fn, fp, tn, tp, y_train


@app.cell(hide_code=True)
def _(fn, fp, mo, tn, tp):
    # Render the Confusion Matrix as a formatted Markdown table
    preccision = tp / (tp+ fp)
    recall = tp / (tp + fn)

    matrix_ui = mo.md(f"""
    ### Confusion Matrix

    | | **Předpovězeno: Přežil (Survived)** | **Předpovězeno: Nepřežil (Perished)** |
    |---|:---:|:---:|
    | **Skutečnost: Přežil** | ✅ **TP: {tp}** <br> *(True Positive)* | ❌ **FN: {fn}** <br> *(False Negative)* |
    | **Skutečnost: Nepřežil** | ❌ **FP: {fp}** <br> *(False Positive)* | ✅ **TN: {tn}** <br> *(True Negative)* |

    - Preccision: {int(preccision * 10000) / 100} %
    - Recall: {int(recall * 10000) / 100} %
    """)

    explanations = mo.callout(
        mo.md("""
        ### 📖 Vysvětlení pojmů

        * **True Positives (TP) – Skutečně pozitivní:** Model správně předpověděl, že cestující **přežije**. *(Trefa do černého)*.
        * **True Negatives (TN) – Skutečně negativní:** Model správně předpověděl, že cestující **nepřežije**. *(Smutná, ale přesná předpověď)*.
        * **False Positives (FP) – Falešně pozitivní:** Falešný poplach (Chyba 1. druhu). Model předpověděl, že cestující přežije, ale ve skutečnosti **nepřežil**. *(Fatální omyl modelu)*.
        * **False Negatives (FN) – Falešně negativní:** Přehlédnutí (Chyba 2. druhu). Model předpověděl, že cestující nepřežije, ale on ve skutečnosti **přežil**. *(Příjemné překvapení)*.

        ---

        **Pokročilé metriky (Classification Report):**
        * **Precision (Přesnost):** $\\frac{TP}{TP + FP}$ — Když model tvrdí, že někdo přežije, jaká je šance, že se to opravdu stane?
        * **Recall:** $\\frac{TP}{TP + FN}$ — Ze všech lidí, kteří skutečně přežili, jakou část z nich model dokázal správně identifikovat?
        """),
        kind="info"
    )

    # Display them stacked vertically in your notebook
    mo.vstack([matrix_ui, explanations])
    return


@app.cell(hide_code=True)
def _(clf, pd):
    def will_survive(pclass: int, sex: str, age: float, fare: float) -> bool:
        sex_numeric = 1 if sex.lower().strip() == 'female' else 0
        passenger_df = pd.DataFrame({
            'Pclass': [pclass],
            'Sex': [sex_numeric],
            'Age': [age],
            'Fare': [fare]
        })
        prediction = clf.predict(passenger_df)[0]
        return bool(prediction)

    return (will_survive,)


@app.cell(hide_code=True)
def _(mo):
    pclass_ui = mo.ui.radio(
        options={"1st Class": 1, "2nd Class": 2, "3rd Class": 3}, 
        value="3rd Class", 
        label="Passenger Class"
    )

    sex_ui = mo.ui.radio(
        options={"Female": "female", "Male": "male"}, 
        value="Female", 
        label="Sex"
    )

    age_ui = mo.ui.slider(
        start=0.5, stop=100.0, step=0.5, value=28.0, 
        label="Age (Years)"
    )

    fare_ui = mo.ui.slider(
        start=0.0, stop=500.0, step=1.0, value=32.0, 
        label="Ticket Fare (£)"
    )

    ui_row = mo.hstack(
        [pclass_ui, sex_ui, age_ui, fare_ui], 
        justify="space-between",
        gap=1
    )

    mo.md(
        f"""
        {ui_row}
        """
    )
    return age_ui, fare_ui, pclass_ui, sex_ui


@app.cell(hide_code=True)
def _(age_ui, fare_ui, mo, pclass_ui, sex_ui, will_survive):
    current_pclass = pclass_ui.value
    current_sex = sex_ui.value
    current_age = age_ui.value
    current_fare = fare_ui.value

    survived = will_survive(current_pclass, current_sex, current_age, current_fare)

    if survived:
        result = mo.callout(
            mo.md(f"### 🎉 **SURVIVED!** \nThe model predicts this {current_age}-year-old {current_sex} in class {current_pclass} makes it to a lifeboat."), 
            kind="success"
        )
    else:
        result = mo.callout(
            mo.md(f"### 🧊 **PERISHED.** \nThe model predicts this {current_age}-year-old {current_sex} in class {current_pclass} goes down with the ship."), 
            kind="danger"
        )

    result
    return


@app.cell
def _(X_train, y_train):
    # 1. Combine training features and target so we can see correlations with survival
    train_data = X_train.copy()
    train_data['Survived'] = y_train

    # 2. Calculate the correlation matrix
    # We use Pearson correlation by default, which ranges from -1.0 to 1.0
    corr_matrix = train_data.corr()

    # 3. Apply a color gradient (coolwarm: blue for negative, red for positive)
    corr_matrix.style.background_gradient(
        cmap='coolwarm', axis=None, vmin=-1, vmax=1
    ).format(precision=2)
    return


if __name__ == "__main__":
    app.run()
