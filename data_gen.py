import pandas as pd

data = {
    "nombre": ["Pepe", "Manolo", "Maria", "Manuel", "Andres"],
    "apellido": ["Rdguez", "Devesa", "Santos", "Santos", "Rdguez"],
    "producto": ["Boligrafo", "Goma", "Lapiz", "Folio", "Estuche"],
    "cantidad": [1, 3, 7, 100, 8],
    "precio": [0.25, 0.25, 0.30, 0.03, 20]
}

df = pd.DataFrame(data=data)
with open('data.csv', 'w', newline="") as f:
    df.to_csv(f, index=False)