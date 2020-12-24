from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from newsletters.models import Newsletter
from tags.models import Tag


class NewslettersActionTestCase(APITestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.admin = User.objects.create_superuser('juana', 'juana@gmail.com', '1234')
        self.admin.save()

        self.admin_2 = User.objects.create_superuser('luis', 'luis@gmail.com', '1234')
        self.admin_2.save()

        self.user = User(username='ana')
        self.user.set_password('1234')
        self.user.save()

        self.tag = Tag.objects.create(
            name='Ciencia',
            slug='slug',
            creation_date='2020-12-16T12:57:09.350200-06:00'
        )
        self.tag.save()

        self.boletin = Newsletter.objects.create(
            name='Boletin uno',
            description='la descripcion',
            image='img/img',
            frequency='semanal',
            creation_date='2020-12-16T12:57:09.350200-06:00',
            owner=self.admin
        )
        self.boletin.save()

        resp = self.client.post(
            f'{self.url}/api/token/', {"username": self.admin.username, "password": '1234'}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        self.token = resp.data["access"]

    def test_create_newsletter_admin_owner(self):
        response = self.client.post(f'{self.url}/newsletter_api/api/v1/newsletters/',
                                    {
                                        'name': 'test Primer boletin',
                                        'description': 'la descripcion',
                                        'image': 'img/img',
                                        'target': [],
                                        'frequency': 'semanal',
                                        'creation_date': '2020-12-16T12:57:09.350200-06:00',
                                        'owner': self.admin.id,
                                        'guests': [],
                                        'likes': [],
                                        'subscribers': []
                                    },
                                    HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 201)

    def test_create_newsletter_user_owner(self):
        response = self.client.post(f'{self.url}/newsletter_api/api/v1/newsletters/',
                                    {
                                        'name': 'Primer boletin',
                                        'description': 'la descripcion',
                                        'image': 'img/img',
                                        'target': [],
                                        'frequency': 'semanal',
                                        'creation_date': '2020-12-16T12:57:09.350200-06:00',
                                        'owner': self.user.id,
                                        'guests': [],
                                        'likes': [],
                                        'subscribers': []
                                    },
                                    HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 400)

    def test_get_owner(self):
        response_owner = self.client.get(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/owner/',
                                         {}, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response_owner.data['id'], self.admin.id)

    def test_get_guests(self):
        self.boletin.guests.add(self.admin_2)

        response_guests = self.client.get(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/guests/',
                                          {}, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response_guests.data['id'], self.admin_2.id)

    def test_guest_admin(self):
        response = self.client.post(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/guest_admin/',
                                    {
                                        'users': [self.admin_2.id, self.user.id]
                                    },
                                    HTTP_AUTHORIZATION='Bearer {0}'.format(self.token), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.boletin.guests.all().count(), 1)

    def test_tags(self):
        response = self.client.post(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/tags/',
                                    {
                                        'tags': [self.tag.id]
                                    },
                                    HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.boletin.tags.all()), 1)

        response = self.client.get(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/tags/',
                                   {}, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.data[0]['id'], self.tag.id)

        response = self.client.delete(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/tags/',
                                      {
                                          'tags': [self.tag.id]
                                      },
                                      HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.boletin.tags.all()), 0)

    def test_target_votar(self):
        response = self.client.post(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/target_votar/',
                                    {
                                        'users': [self.user.id]
                                    },
                                    HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.boletin.target.all()), 1)

        response = self.client.get(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/target_votar/',
                                   {}, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.data[0]['id'], self.user.id)

        response = self.client.delete(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/target_votar/',
                                      {
                                          'users': [self.user.id]
                                      },
                                      HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.boletin.target.all()), 0)

    def test_suscriptions(self):
        response = self.client.post(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/suscriptions/',
                                    {
                                        'users': [self.user.id]
                                    },
                                    HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.boletin.subscribers.all()), 1)

        response = self.client.get(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/suscriptions/',
                                   {}, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.data[0]['id'], self.user.id)

        response = self.client.delete(f'{self.url}/newsletter_api/api/v1/newsletters/{self.boletin.id}/suscriptions/',
                                      {
                                          'users': [self.user.id]
                                      },
                                      HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(self.boletin.subscribers.all()), 0)

    def test_filter_by_tags(self):
        self.boletin.tags.add(self.tag)

        query = f'tags={self.tag.name}'
        response = self.client.get(f'{self.url}/newsletter_api/api/v1/newsletters/?{query}',
                                   {}, HTTP_AUTHORIZATION='Bearer {0}'.format(self.token))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['name'],
            self.boletin.name
        )
