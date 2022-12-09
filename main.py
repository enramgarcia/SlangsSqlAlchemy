import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

USER = "root"
PASSWORD = "secret"
PORT = 3808
DB = "slangs"
SERVER = "localhost"

Base = declarative_base()


class Dictionary(Base):
    __tablename__ = 'dictionary'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    word = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True)
    description = sqlalchemy.Column(sqlalchemy.String(length=255))


def seed():
    words = [
        {'word': 'Xopa', 'description': 'Forma coloquial de decir Hola.'},
        {'word': 'Chantin', 'description': 'Casa'}
    ]

    for definition in words:
        result_set = session.query(Dictionary).filter_by(word=definition['word'])

        if result_set.count() > 0:
            continue

        word_definition = Dictionary(word=definition['word'], description=definition['description'])

        session.add(word_definition)

    session.commit()


def print_word(definition):
    print(f"{definition.word}: {definition.description}")


def show(word):
    result_set = session.query(Dictionary).filter_by(word=word)

    if result_set.count() == 0:
        print(f'No se encontró la palabra: {word}')
        return

    for result in result_set:
        print_word(result)


def show_all():
    words_list = session.query(Dictionary).all()

    for definition in words_list:
        print_word(definition)


def update(word, description):
    result_set = session.query(Dictionary).filter_by(word=word)

    if result_set.count() == 0:
        print(f'No se encontró la palabra: {word}')
        return

    for result in result_set:
        result.description = description

    session.commit()


def add():
    word = input('Palabra: ')
    description = input('Definicion: ')

    result_set = session.query(Dictionary).filter_by(word=word)

    if result_set.count() > 0:
        print(f'La palabra {word} ya existe.')
        return

    add_word = Dictionary(word=word, description=description)
    session.add(add_word)
    session.commit()


def delete(word):
    session.query(Dictionary).filter_by(word=word).delete()
    session.commit()


if __name__ == '__main__':
    connection_string = f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{SERVER}:{PORT}"

    print(connection_string)

    db_engine = sqlalchemy.create_engine(connection_string)

    db_engine.execute(f'Create Database if not exists {DB}')

    engine = sqlalchemy.create_engine(f"{connection_string}/{DB}")

    Base.metadata.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    seed()

    while True:
        print('Menu')
        print('1- Mostrar todo')
        print('2- Agregar')
        print('3- Buscar palabra')
        print('4- Actualizar palabra')
        print('5- Borrar palabra')
        print('6- Salir')
        option = int(input('Opcion (1-6): '))

        if option == 1:
            show_all()
        elif option == 2:
            add()
        elif option == 3:
            search_word = input('Palabra: ')
            show(search_word)
        elif option == 4:
            search_word = input('Palabra: ')
            update_description = input('Definicion: ')
            update(search_word, update_description)
        elif option == 5:
            search_word = input('Palabra: ')
            delete(search_word)
        else:
            break


