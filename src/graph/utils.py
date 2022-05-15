
from matplotlib import pyplot as plt


def bartext(x: float, y: float, text: str, barwidth: float, vector: str = 'left') -> None:
    x = x - barwidth / 2 if vector == 'left' else x + barwidth / 2
    y = y / 2
    plt.text(x, y, text, ha='center', bbox=dict(facecolor='#fff'))
