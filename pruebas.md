Pruebas con Session

```
from sqlalchemy.orm import Session
sess1 = Session(bind=db.engine, autoflush=False)
sess2 = Session(bind=db.engine, autoflush=True)

a1 = Articulo(producto='boli', precio=0.25)
a2 = Articulo(producto='boli2', precio=0.25)
```


PRUEBA 1 ->
a1 se encuentra en la base de datos, entonces:

```
sess1.get(Articulo, 'boli')
```

- Debería dar el objeto contenido en la base de datos. SI
- Si lo almacenamos en a1_get_sess1_test1 es igual a a1? NO
- Al hacer sess1.get el objeto obtenido pasa a formar parte de la sesión? NO (Session.new = vacio)

```
sess2.get(Articulo, 'boli')
```

- Debería dar el objeto contenido en la base de datos. SI
- Si lo almacenamos en a1_get_sess2_test1 es igual a a1_get? NO

A priori parece que Session.get cuando Session.new = vacio funciona como se espera

PRUEBA2 ->
a1 se encuentra en la base de datos y lo añadimos a la sesión con Session.add(a1)

```
sess1.add(a1)
sess1.get(Articulo, 'boli')
```

- Esto funciona como se espera (a priori)
- Si almacenamos el resultado del .get en a1_get_sess1_test2 será igual a a1? NO
  - Esto da que pensar que el .get no coge el objeto de la sesión directamente
- Será igual a a1_get_sess1_test1 (el objeto obtenido de la BD en la prueba anterior) SI

Iteramos la Prueba2 para la sess2 donde autoflush==True

```
sess2.add(a1)
sess2.get(Articulo, 'boli')
```

- No se puede añadir el mismo objeto (a1) a dos sesiones diferentes!

```
sess1.expunge(a1)
sess2.add(a1)
sess2.get(Articulo, 'boli')
```

- Esto funciona como se espera (a priori)
- Si almacenamos el resultado del .get en a1_get_sess2_test2 será igual a a1? NO
  - Esto da que pensar que el .get no coge el objeto de la sesión directamente
- Será igual a a1_get_sess2_test1 (el objeto obtenido de la BD en la prueba anterior) SI
- Será igual a a1_get_sess1_test1 (el objeto obtenido de la BD con la sesión1) NO
  - Parece que entre sesiones no se captura el mismo objeto
