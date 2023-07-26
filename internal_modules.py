from __future__ import (
    unicode_literals,
    annotations
)
from typing import List
from sqlalchemy import (
    create_engine,
    ColumnElement,
    URL,
    inspect
)
from sqlalchemy.orm import (
    DeclarativeBase,
    RelationshipProperty,
    sessionmaker,
    InstanceState,
    Session
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
    
    def get_state(self, repr: bool=True):
        name = self.__class__.__name__
        memory = id(self)
        state_object: InstanceState = inspect(self)
        for s in ['transient', 'pending', 'detached', 'persistent', 'expired', 'deleted']:
            if getattr(state_object, s):
                current_state = s.upper()
                break
            else:
                current_state = '???'

        return f"{name} at {memory} > {current_state}" if repr else current_state.lower()

    @classmethod
    def as_unique(cls, session: Session, *arg, **kw):
        cache = getattr(session, 'info', None)
        key = (cls, *kw.values())
        if key in cache:
            return cache[key]
        else:
            with session.no_autoflush:
                pks = [col.name for col in cls.__table__.primary_key]
                pk_kw = {}
                for k, v in kw.items():
                    if k in pks:
                        pk_kw[k] = v
                obj = session.query(cls).filter_by(**pk_kw).first()
                if not obj:
                    obj = cls(*arg, **kw)
            cache[key] = obj
            return obj

    # def _todict(self) -> dict:
    #     column_collection: List[ColumnElement] = self.__mapper__.columns
    #     relation_props: List[RelationshipProperty] = filter(lambda prop: isinstance(prop, RelationshipProperty), self.__mapper__.iterate_properties)
    #     relation_dict = {}

    #     for relation in relation_props:
    #         for local, remote in relation.local_remote_pairs:
    #             local_col_name = getattr(local, 'key')
    #             relation_key = getattr(relation, 'key')
    #             remote_col_name = getattr(remote, 'key')
    #             relation_dict[local_col_name] = {'rel_key': relation_key, 'target_col': remote_col_name}

    #     for col in column_collection:
    #         col_name = getattr(col, 'key')
    #         if col_name in vars(self):
    #             yield col_name, getattr(self, col_name)

    #         elif col_name in relation_dict:
    #             rel_key = relation_dict[col_name]['rel_key']
    #             target_col = relation_dict[col_name]['target_col']
    #             target_obj = getattr(self, rel_key)
    #             yield col_name, getattr(target_obj, target_col) if target_obj else None
            
    #         elif hasattr(col, 'default'):
    #             yield col_name, getattr(col, 'default')

    #         else:
    #             yield col_name, None

    # def __repr__(self):
    #         class_name = self.__class__.__name__
    #         try:
    #             params = ',\n   '.join(f'{k}={v}' for k, v in self._todict())
    #             location = id(self)
    #             # loc_repr = '-'.join([location[:3], location[3:8], location[8:]]) 
    #             return f"{class_name}([mem: {location}]\n   {params}\n)"
    #         except:
    #             return super().__repr__()
    

class DataBase():
    
    def __init__(
        self,
        driver_name: str,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        echo: bool=True) -> None:

        self.host = host
        self.port = port
        url_object = URL.create(
            drivername=driver_name,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database
        )
        self._engine = create_engine(url_object, echo=echo)
        self._metadata = Base.metadata
        self._session_factory = sessionmaker(bind=self._engine)
    
    def __repr__(self) -> str:
        return f"<Database object at {self.host}:{self.port}>"

    def get_tables(self):
        return list(self._metadata.tables.keys())
    
    def get_session(self):
        return self._session_factory()
    
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
        print(f'Creando: {self._metadata.tables.keys()}')
        self._metadata.create_all(bind=self._engine)
    
    def reflect(self):
        self._metadata.reflect(bind=self._engine)