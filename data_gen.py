import pandas as pd

data = {
    "nombre": ["Pepe", "Manolo", "Maria", "Maria", "Pepe"],
    "apellido": ["Rdguez", "Devesa", "Santos", "Santos", "Rdguez"],
    "producto": ["Boligrafo", "Boligrafo", "Lapiz", "Folio", "Folio"],
    "cantidad": [1, 3, 7.2, 100, 8],
    "precio": [0.25, 0.25, 0.30, 0.03, 0.03]
}

df = pd.DataFrame(data=data)
with open('data.csv', 'w', newline="") as f:
    df.to_csv(f, index=False)