import unittest
from project import create_app

flask_app = create_app()


class ProjetUnitTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):

		cls.test_app = flask_app.test_client()

	def test_main_page(self):
		response = self.test_app.get('/')
		assert response.status_code == 200
		assert b"Flask Login Example" in response.data

	def test_affiche_page(self):
		response = self.test_app.get('/affiche')
		assert response.status_code == 200
		assert b"Les utilisateurs" in response.data

	def test_login_page(self):
		response = self.test_app.get('/login')
		assert response.status_code == 200
		assert b"Login" in response.data
