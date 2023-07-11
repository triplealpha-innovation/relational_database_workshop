from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, declared_attr
from pandas import DataFrame

class Base(DeclarativeBase):
    @declared_attr
    def info(cls):
        def f():
            data = {
                'campo': [],
                'tipo_dato': [],
                'primary_key': [],
                'nullable': [],
                'foreing_key': []
            }
            
            for c in cls.__table__.columns:
                data['campo'].append(c.name)
                data['tipo_dato'].append(c.type)
                data['primary_key'].append(c.primary_key)
                data['nullable'].append(c.nullable)
                data['foreing_key'].append(list(c.foreign_keys))
            
            return DataFrame(data=data)
        return f

class DataBase():
    
    def __init__(
        self,
        engine_name: str,
        user: str,
        pwd: str,
        db_name: str,
        host: str,
        port: int,
        echo: bool=True) -> None:

        self.conn_str = f'{engine_name}://{user}:{pwd}@{host}:{port}/{db_name}'
        self.engine = create_engine(self.conn_str, echo=echo)
        self.metadata = Base.metadata

    def get_tables(self):
        return list(self.metadata.tables.keys())
    
    def get_session(self):
        return Session(bind=self.engine)
    
    def get_model_base(self):
        return Base
    
    def create_all(self):
        print(f'Creando: {self.metadata.tables.keys()}')
        self.metadata.create_all(bind=self.engine)
    
    def reflect(self):
        self.metadata.reflect(bind=self.engine)
    
    def drop_duplicates(self, session: Session):
        o_types = set([type(o) for o in session.new])
        for o_type in o_types:
            for o in session.new:
                if isinstance(o, o_type):
                    pass