import marimo

__generated_with = "0.10.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import requests


    return mo, pd, requests


@app.cell
def _(mo, pd):
    url = 'https://raw.githubusercontent.com/antoinebugeia/bdloc-cleaning/refs/heads/main/BDLOC_6626732514566488014.csv'

    # df = pd.read_csv('BDLOC_6626732514566488014.csv', sep=',', lineterminator="\n", skip_blank_lines=True)
    df = pd.read_csv(url, lineterminator="\n", skip_blank_lines=True)
    mo.ui.dataframe(df)

    return df, url


@app.cell
def _(df):
    df[df['OBJECTID'] == 19970] # le load fonctionne
    return


@app.cell
def _(df):
    df_filtered = df[(df['SOURCE'] != 'ATLAS') & (df['SOURCE'] != 'REFIL')].copy()
    df_filtered.shape
    return (df_filtered,)


@app.cell
def _(df_filtered):
    df_filtered[df_filtered.duplicated()]
    return


@app.cell
def _(df_filtered):
    cat_col = [col for col in df_filtered.columns if df_filtered[col].dtype == 'object']
    print('Categorical columns :',cat_col)
    num_col = [col for col in df_filtered.columns if df_filtered[col].dtype != 'object']
    print('Numerical columns :',num_col)
    return cat_col, num_col


@app.cell
def _():
    cat_col_to_unique = ['LIBELLE', 'LIBEL_ABR', 'TYPE', 'CATEGORIE', 'SOURCE', 'ORIGINE', 'PROVINCE']
    return (cat_col_to_unique,)


@app.cell
def _(cat_col_to_unique, df_filtered):
    for _col in cat_col_to_unique:
        if df_filtered[_col].nunique() < 500:
            print(_col)
            print(df_filtered[_col].unique())
    return


@app.cell
def _(cat_col_to_unique, df_filtered):
    for _col in cat_col_to_unique:
        if df_filtered[_col].nunique() >= 500:
            print(_col)
    return


@app.cell
def _(df_filtered):
    df_filtered[df_filtered['DIFFUSION'] == 'NON']
    return


@app.cell
def _(df_filtered):
    cols_to_analyse = ['LIBELLE', 'LIBEL_ABR']
    df_filtered[cols_to_analyse]
    return (cols_to_analyse,)


@app.cell
def _(df_filtered):
    import re

    pattern = r'\b(?:[a-zA-Z]\.)+[a-zA-Z]*|\b[a-zA-Z]{2,}\.'

    # Fonction pour détecter les abréviations et acronymes
    def detect_abbreviations(_df, _column, _pattern):
        return _df[_column].apply(
            lambda _x: tuple(sorted(set(re.findall(_pattern, _x)))) if isinstance(_x, str) else ()
        )
    # Appliquer sur une colonne spécifique
    df_filtered['abbreviations'] = detect_abbreviations(df_filtered, 'LIBELLE', pattern)
    df_filtered[df_filtered['abbreviations'].apply(lambda x: len(x) > 0)][['LIBELLE', 'abbreviations']].groupby('abbreviations').first().reset_index()
    return detect_abbreviations, pattern, re


@app.cell
def _(df_filtered):
    df_filtered['abbreviations'].unique()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
