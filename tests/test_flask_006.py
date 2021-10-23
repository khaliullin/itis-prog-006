from flask_006 import __version__
from flask_006.flaskapp import app

def test_version():
    assert __version__ == '0.1.0'


def test_index_is_ok():
    app.testing = True
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    # page_content = response.response[0].decode('UTF-8')
    # assert 'Hello Flask! This is our posts' in page_content
