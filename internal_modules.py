from __future__ import (
    unicode_literals,
    annotations
)
from typing import List
from sqlalchemy import (
    create_engine,
    ColumnElement
)
from sqlalchemy.orm import (
    Session, 
    DeclarativeBase,
    RelationshipProperty
)
from pandas import DataFrame


class Base(DeclarativeBase):

    @classmethod
    def info(cls):
        data = {
            'campo': [],
            'tipo_dato': [],
            'primary_key': [],
            'nullable': [],
            'foreing_key': []
        }

        cols: List[ColumnElement] = cls.__table__.columns
        
        for c in cols:
            data['campo'].append(getattr(c, 'name'))
            data['tipo_dato'].append(getattr(c, 'type'))
            data['primary_key'].append(getattr(c, 'primary_key'))
            data['nullable'].append(getattr(c, 'nullable'))
            data['foreing_key'].append(True if getattr(c, 'foreign_keys') else False)
        
        return DataFrame(data=data)

    def _todict(self) -> dict:
        column_collection: List[ColumnElement] = self.__mapper__.columns
        relation_props: List[RelationshipProperty] = filter(lambda prop: isinstance(prop, RelationshipProperty), self.__mapper__.iterate_properties)
        relation_dict = {}

        for relation in relation_props:
            for local, remote in relation.local_remote_pairs:
                local_col_name = getattr(local, 'key')
                relation_key = getattr(relation, 'key')
                remote_col_name = getattr(remote, 'key')
                relation_dict[local_col_name] = {'rel_key': relation_key, 'target_col': remote_col_name}

        for col in column_collection:
            col_name = getattr(col, 'key')
            if col_name in vars(self):
                yield col_name, getattr(self, col_name)

            elif col_name in relation_dict:
                rel_key = relation_dict[col_name]['rel_key']
                target_col = relation_dict[col_name]['target_col']
                target_obj = getattr(self, rel_key)
                yield col_name, getattr(target_obj, target_col) if target_obj else None
            
            elif hasattr(col, 'default'):
                yield col_name, getattr(col, 'default')

            else:
                yield col_name, None

    def __repr__(self):
            class_name = self.__class__.__name__
            try:
                params = ',\n   '.join(f'{k}={v}' for k, v in self._todict())
                return f"{class_name}(\n   {params}\n)"
            except:
                return super().__repr__()

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
        self.session = None

    def get_tables(self):
        return list(self.metadata.tables.keys())
    
    def get_session(self):
        if not self.session:
            self.session = Session(bind=self.engine)
        return self.session
    
    def commit_transactions(self, transactions: list, concile=True):
        session = self.get_session()
        if concile:
            for t in transactions:
                try:
                    session.merge(t)
                    session.commit()
                except Exception:
                    session.rollback()
            session.close()
        else:
            session.add_all(transactions)
            try:
                session.commit()
            except Exception:
                session.rollback()
            finally:
                session.close()

    def get_model_base(self):
        return Base
    
    def create_all(self):
        print(f'Creando: {self.metadata.tables.keys()}')
        self.metadata.create_all(bind=self.engine)
    
    def reflect(self):
        self.metadata.reflect(bind=self.engine)