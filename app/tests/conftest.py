import pytest
from app.__init__ import *
from app.models import AuthUser
                    

@pytest.fixture(scope='session')
def app():
    app = create_app(test_mode=True)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:'
    })

    with app.app_context():
        user = AuthUser(id = 100000, username='testuser', password='password', email='test@example.com')
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='session')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function', autouse=True)
def session(app):
    with app.app_context():

        connection = db.engine.connect()
        transaction = connection.begin()

        options = dict(bind=connection)
        session = db._make_scoped_session(options=options)
        session.no_autoflush
        db.session = session
        
        yield session

        transaction.rollback()
        connection.close()
        session.remove()

