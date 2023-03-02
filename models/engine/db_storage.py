from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User


class DBStorage:
    '''
    Handles database engine
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
        Create engine for database
        '''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        query for all objects on the current database session
        '''
        classes = {
            "City": City,
            "State": State,
            "User": User,
        }
        result = {}
        query_rows = []

        if cls:
            '''Query for all objects belonging to cls'''
            for name, value in classes.items():
                if name == cls:
                    query_rows = self.__session.query(value)
                    for obj in query_rows:
                        key = '{}.{}'.format(name, obj.id)
                        result[key] = obj
            return result
        else:
            '''Query for all types of objects'''
            for name, value in classes.items():
                query_rows = self.__session.query(value)
                for obj in query_rows:
                    key = '{}.{}'.format(name, obj.id)
                    result[key] = obj
            return result

    def new(self, obj):
        '''add the object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete obj from the current database session'''
        self.__session.delete(obj)

    def reload(self):
        '''
        - create all tables in the database
        - create the current database session from the engine
        '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
