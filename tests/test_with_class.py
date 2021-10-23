from flask_006.flaskapp import app

class TestView:

    def setup(self):
        app.testing = True
        self.client = app.test_client()
        print('setup')

    def teardown(self):
        print('teardown')

    def test_first(self):
        self.client.get('/')
        assert 1 + 1 == 2
