from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User


# Create your tests here.
class TestSession(TestCase):
    def setUp(self):
        User.objects.create_user(username='swerbernjagermanjensen',
                                 email='hewasnumberone@example.com',
                                 password='hunter2')


    def test_valid_login(self):
        client = APIClient()
        response = client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})

        assert response.status_code == 201
        assert response.data['username'] == 'swerbernjagermanjensen'


    def test_invalid_login(self):
        client = APIClient()
        response = client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter43526'})

        assert response.status_code == 400


    def test_get_current_session(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.get('/api/sessions')
        assert response.status_code == 200
        assert response.data['username'] == 'swerbernjagermanjensen'

    def test_get_guest_session(self):
        client = APIClient()
        response = client.get('/api/sessions')

        assert response.status_code == 200
        assert response.data['username'] == ''

    def test_logout(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.delete('/api/sessions')
        assert response.status_code == 202
        response = client.get('/api/sessions')
        assert response.status_code == 200
        assert response.data['username'] == ''

class TestUsers(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='swerbernjagermanjensen',
                                 email='hewasnumberone@example.com',
                                 password='hunter2')



    def test_get_single_user(self):
        client = APIClient()
        response = client.get('/api/users/{}/'.format(self.user.id))
        assert response.status_code == 200
        assert response.data['username'] == 'swerbernjagermanjensen'

    def test_list_users(self):
        client = APIClient()
        response = client.get('/api/users/')
        assert response.status_code == 200
        assert response.data[0]['username'] == 'swerbernjagermanjensen'


class TestToDos(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='swerbernjagermanjensen',
                                 email='hewasnumberone@example.com',
                                 password='hunter2')
    def test_create_valid_todos(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        assert response.data['text'] == 'gjdgrnjg'
        assert response.data['done'] is True

    def test_create_invalid_todos(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.post('/api/todos/', {})
        assert response.status_code == 400

    def test_create_valid_todo_guest(self):
        client = APIClient()
        response = client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        assert response.status_code == 403

    def test_list_user_todos(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        response = client.get('/api/todos/')
        assert response.data[0]['text'] == 'gjdgrnjg'
        assert response.data[0]['done'] is True

    def test_list_guest_todos(self):
        client = APIClient()
        response = client.get('/api/todos/')
        assert response.status_code == 403

    def test_edit_todo(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        edit_response = client.put('/api/todos/' + str(response.data['id']) + '/',
                                   {'text': 'wifjskf', 'done': False})
        assert edit_response.data['text'] == 'wifjskf'
        assert edit_response.data['done'] is False

    def test_edit_todo_guest(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        client.delete('/api/sessions')
        edit_response = client.put('/api/todos/' + str(response.data['id']) + '/',
                                   {'text': 'wifjskf', 'done': False})
        assert edit_response.status_code == 403

    def test_delete_todo(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        delete_response = client.delete('/api/todos/' + str(response.data['id']) + '/')
        assert delete_response.status_code == 204

    def test_delete_todo_guest(self):
        client = APIClient()
        client.post('/api/sessions', {'username': 'swerbernjagermanjensen',
                                                 'password': 'hunter2'})
        response = client.post('/api/todos/', {'text': 'gjdgrnjg', 'done': True})
        client.delete('/api/sessions')
        delete_response = client.delete('/api/todos/' + str(response.data['id']) + '/')
        assert delete_response.status_code == 403
