import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo, pd):
    df = pd.read_csv('BDLOC_6626732514566488014.csv', sep=',', lineterminator="\n", skip_blank_lines=True)
    mo.ui.dataframe(df)
    return (df,)


@app.cell
def _(df):
    df[df['OBJECTID'] == 19970] # le load fonctionne
    return


@app.cell
def _(df):
    df2 = df[(df['SOURCE'] != 'ATLAS') & (df['SOURCE'] != 'REFIL')]
    df2.shape
    return (df2,)


@app.cell
def _(df2):
    df2[df2.duplicated()]
    return


@app.cell
def _(df2):
    df2.info()
    return


@app.cell
def _(df2):
    cat_col = [col for col in df2.columns if df2[col].dtype == 'object']
    print('Categorical columns :',cat_col)
    num_col = [col for col in df2.columns if df2[col].dtype != 'object']
    print('Numerical columns :',num_col)
    return cat_col, num_col


@app.cell
def _():
    cat_col_to_unique = ['LIBELLE', 'LIBEL_ABR', 'TYPE', 'CATEGORIE', 'SOURCE', 'ORIGINE', 'PROVINCE']
    return (cat_col_to_unique,)


@app.cell
def _(cat_col_to_unique, df2):
    for _col in cat_col_to_unique:
        if df2[_col].nunique() < 500:
            print(_col)
            print(df2[_col].unique())
    return


@app.cell
def _(cat_col_to_unique, df2):
    for _col in cat_col_to_unique:
        if df2[_col].nunique() >= 500:
            print(_col)
    return


@app.cell
def _(df2):
    df2[df2['DIFFUSION'] == 'NON']
    return


@app.cell
def _(df2):

    cols_to_analyse = ['LIBELLE', 'LIBEL_ABR']
    df2[cols_to_analyse]

    return (cols_to_analyse,)


@app.cell
def _(df2):
    import re

    pattern = r'\b[A-Z]{2,}(?:\.[A-Z]{2,})?|\b(?:[A-Z]\.){2,}|\b[A-Za-z]{1,4}\.\b'


    # Fonction pour détecter les abréviations et acronymes
    def detect_abbreviations(_df, _column, _pattern):
        return _df[_column].apply(lambda x: re.findall(_pattern, x) if isinstance(x, str) else [])

    # Appliquer sur une colonne spécifique
    df2['abbreviations'] = detect_abbreviations(df2, 'LIBELLE', pattern)
    df2[df2['abbreviations'] != '[]']
    return detect_abbreviations, pattern, re


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
