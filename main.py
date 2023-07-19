# %%

import os
from internal_modules import DataBase
from models import Cliente, Articulo, Venta
from pandas import read_csv

db = DataBase(
    engine_name='postgresql',
    user='test_user',
    pwd='triple',
    db_name='db_database_workshop',
    host='localhost',
    port='5432',
    echo=True
)
db.create_all()

# %%
ROOT = os.path.dirname(__file__)
data = read_csv(os.path.join(ROOT, 'data.csv'))
session = db.get_session()

## Creación de instancias
# %%
transactions = []
for index, row in data.iterrows():
    t = Venta(
        cliente=Cliente(
            id=f"{row['nombre']}_{row['apellido']}",
            nombre=row['nombre'],
            apellido=row['apellido']
        ),
        articulo=Articulo(
            producto=row['producto'],
            precio=row['precio']
        ),
        cantidad=row['cantidad']
    )
    transactions.append(t)
# %%
db.commit_transactions(transactions=transactions)