import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="XRF-Spektren",
    page_icon="🩻",
    layout="wide",  # Enables full-width layout
    initial_sidebar_state="expanded"
)


def main():
    
    file = st.sidebar.file_uploader('Datei hochladen')
    if file:
        option: int = st.sidebar.selectbox(
            'Spektrum auswählen', (1, 2, 3))
        slider_x = st.sidebar.slider('x range', 0, 60, (0, 60))

        x, y = read_spectrum(file, option)

        slider_y = st.sidebar.slider(
            'y range', 0.0, float(max(y)), (0.0, float(max(y))))

        elements = annotations()

        fig = plot_spectrum(x, y, slider_x, slider_y,
                            elements, get_exponent(y))

        st.divider()
        st.write(fig)


def read_spectrum(file, option: int) -> list[float]:

    df = pd.read_csv(file, sep=r'\t')
    keys: str = df.keys()

    x: list[float] = pd.to_numeric(df[keys[0]], errors='coerce')

    y: list[float] = (
        df[keys[option]]
        .astype(str)
        .str.replace('.', '', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
    )
    return x, y


def annotations() -> list[dict]:
    df = pd.DataFrame(
        [
            {
                "Element": "",
                "x-Koordinate": "",
                "y-Koordinate": "",
                "show annotation": True,
            },
        ]
    )
    edited_df = st.data_editor(df, num_rows="dynamic")
    return edited_df


def get_exponent(y) -> int:
    exp = len(str(int(max(y))))-1
    return int(exp)


def plot_spectrum(x: list[float], y: list[float], slider_x, slider_y, elements, exp: int):
    ONE_MM = 1 / 25.4

    plt.rc('figure', autolayout=True)
    plt.rc('font', size=8)
    fig, ax = plt.subplots(figsize=(180*ONE_MM, 70*ONE_MM))
    ax.plot(x, y, linewidth=0.25, color='black')

    # just looks
    ax.set_xlabel('Energie in keV')
    ax.set_ylabel('Intensität')
    ax.spines.right.set_color(None)
    ax.spines.top.set_color(None)
    ax.spines.bottom.set_bounds(slider_x)
    ax.spines.left.set_bounds(min(slider_y), max(slider_y))
    ax.set_xticks(np.arange(min(slider_x), max(slider_x), 1), minor=True)
    ax.set_xticks(np.arange(min(slider_x), max(slider_x)+1, 5))
    ax.set_xlim(min(slider_x)-(max(slider_x)/100), max(slider_x))
    ax.set_ylim(min(slider_y)-(max(slider_y)/25), max(slider_y))

    # annotation
    for i in range(len(elements)):
        if elements.iloc[i, 1] and elements.iloc[i, 2] and elements.iloc[i, 3] == True:
            ax.annotate(elements.iloc[i, 0], xy=(
                float(elements.iloc[i, 1]), float(elements.iloc[i, 2])*10**exp))
    return fig


if __name__ == "__main__":
    main()
