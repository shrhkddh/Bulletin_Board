from django.test import (
    TestCase,
    Client
)

from .models import Board

TestCase.maxDiff = None

class BoardViewTest(TestCase):
    def setUp(self):
        client = Client()
        board = Board.objects.create(
            id          = 1,
            name        = '홍길동',
            password    = 'ghdrlfehd1!',
            title       = '홍길동전',
            description = '아버지를 아버지라 부르지 못하고',
            user_ip     = '127.0.0.1',
        )

    def tearDown(self):
        Board.objects.all().delete()

    def test_get_boardview_success(self):
        client = Client()
        response = self.client.get('/board/posting')
        self.assertEqual(response.json(), {
            'Board' : [{
                'id'          : 1,
                'name'        : '홍길동',
                'password'    : 'ghdrlfehd1!',
                'title'       : '홍길동전',
                'description' : '아버지를 아버지라 부르지 못하고',
                'user_ip'     : '127.0.0.1',
                'updated_at'   : '2020-08-13'
            }]
        })
        self.assertEqual(response.status_code, 200)