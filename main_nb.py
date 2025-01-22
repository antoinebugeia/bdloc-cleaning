import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(pd):
    df = pd.read_csv('BDLOC_6626732514566488014.csv', sep=',', lineterminator="\n", skip_blank_lines=True)
    df
    return (df,)


@app.cell
def _(df):
    df[df['OBJECTID'] == 19970]
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
def _(cat_col, df2):
    for col in cat_col:
        if df2[col].nunique() < 1000:
            print(col)
            print(df2[col].unique())
    return (col,)


@app.cell
def _(df, re):
    def detect_abbreviations(label):
        # Motif pour repérer les abréviations (exemple : majuscules et/ou points)
        pattern = r'\b(?:[A-Z]{2,}|(?:[A-Z]\.){2,})\b'
        return re.findall(pattern, label)

    # Appliquer la détection sur la colonne 'label'
    df['abbreviations'] = df['label'].apply(lambda x: detect_abbreviations(x) if isinstance(x, str) else [])

    return (detect_abbreviations,)


if __name__ == "__main__":
    app.run()
