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
def _(mo):
    mo.md(
        r"""
        ## Fichier CSV
        A l'import quelques problèmes dans la structure du CSV :  
        ![](https://github.com/antoinebugeia/bdloc-cleaning/blob/main/pb_csv.PNG?raw=true)

        ![](https://github.com/antoinebugeia/bdloc-cleaning/blob/main/pb_csv2.PNG?raw=true)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Contenu

        On voit très rapidemment que régulièrement la colonne 'LIBEL_ABR' ne contient plus l'information initiale sur le nom propre, ex :  
        - 'Cimetière de Naniouni' dans 'LIBELLE' devient 'Cim.'  
        - 'Station d'épuration James Cook' devient 'Epur.'

        """
    )
    return


@app.cell
def _(mo, pd):
    url = 'https://raw.githubusercontent.com/antoinebugeia/bdloc-cleaning/refs/heads/main/BDLOC_6626732514566488014.csv'

    # df = pd.read_csv('BDLOC_6626732514566488014.csv', sep=',', lineterminator="\n", skip_blank_lines=True)
    df = pd.read_csv(url, lineterminator="\n", skip_blank_lines=True)
    mo.ui.dataframe(df)

    return df, url


@app.cell
def _(mo):
    mo.md(
        r"""
        Test de l'affichage d'une ligne ayant un problème de structure dans le csv avec des paramètres spécifiques : (lineterminator="\n", skip_blank_lines=True)  
        Ca fonctionne.
        """
    )
    return


@app.cell
def _(df):
    df[df['OBJECTID'] == 19970] # le load fonctionne
    return


@app.cell
def _(mo):
    mo.md("""Obervation du nombre d'individus et du nbde colonnes :""")
    return


@app.cell
def _(df):
    df_filtered = df[(df['SOURCE'] != 'ATLAS') & (df['SOURCE'] != 'REFIL')].copy() # on ne s'occupe pas de ces 2 sources
    df_filtered.shape
    return (df_filtered,)


@app.cell
def _(mo):
    mo.md(r"""Recherche des doublons : il n'y en a pas.""")
    return


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
def _(mo):
    mo.md("""## Contenus uniques""")
    return


@app.cell
def _(cat_col_to_unique, df_filtered, mo):


    for _col in cat_col_to_unique:
        if df_filtered[_col].nunique() < 500:
            mo.output.append("Nom de la colonne : " + _col)
            mo.output.append(df_filtered[_col].unique())
    return


@app.cell
def _(cat_col_to_unique, df_filtered):
    for _col in cat_col_to_unique:
        if df_filtered[_col].nunique() >= 500:
            print(_col)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Certaines lignes sont marqués 'NON' dans la colonne 'DIFFUSION'.  
        La catégorie des stations services est d'ailleurs étonnante.
        """
    )
    return


@app.cell
def _(df_filtered):
    df_filtered[df_filtered['DIFFUSION'] == 'NON']
    return


@app.cell
def _(mo):
    mo.md(r"""Etude des 2 colonnes qui concernent le libellé.""")
    return


@app.cell
def _(df_filtered):
    cols_to_analyse = ['LIBELLE', 'LIBEL_ABR']
    df_filtered[cols_to_analyse]
    return (cols_to_analyse,)


@app.cell
def _(mo):
    mo.md(r"""Beaucoup de LIBEL_ABR sont identiques aux LIBELLE :""")
    return


@app.cell
def _(cols_to_analyse, df_filtered):
    df_filtered[df_filtered['LIBELLE'] == df_filtered['LIBEL_ABR']][cols_to_analyse].shape

    return


@app.cell
def _(mo):
    mo.md(
        r"""
        On effectue ici une recherche auto des abbréviations utilisées dans la colonne LIBELLE.  
        Il peut y en avoir d'autres, par exemple BCI (et non B.C.I.) mais elles ne peuvent pas être cherchées de façon auto car énormément des mots sont également intégrallement en majuscules.
        """
    )
    return


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
def _(mo):
    mo.md(r"""Elements uniques de la recherche :""")
    return


@app.cell
def _(df_filtered):
    df_filtered['abbreviations'].unique()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
