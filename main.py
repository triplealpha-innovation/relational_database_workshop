# %%

import os
from internal_modules import DataBase
from models import Cliente, Articulo, Venta
from pandas import read_csv

db = DataBase(
    driver_name='postgresql',
    username='test_user',
    password='triple',
    host='localhost',
    port='5432',
    database='db_database_workshop',
    echo=True
)
# db.create_all()
session = db.get_session()
# %%
a1 = Articulo.as_unique(session=session, producto='boli', precio=0.25)
# %%
ROOT = os.path.dirname(__file__)
data = read_csv(os.path.join(ROOT, 'data.csv'))

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
    t = session.merge(t)
    session.add(t)
# %%
session.commit()
# %%
db.commit_transactions(transactions=transactions)