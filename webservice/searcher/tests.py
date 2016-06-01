"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from searcher.models import TipsWord

class WordTipsTest(TestCase):

    def _create_tipsword(self, **default):
        return TipsWord.objects.create(**default)

    def test_basic_create(self):
        word = self._create_tipsword(keyword='愤怒的小鸟',
                                     weight=300)
        self.assertEqual(word.keyword, '愤怒的小鸟')
        self.assertEqual(word.weight, 300)

    def test_order_weight(self):
        word1 = self._create_tipsword(keyword='愤怒的小鸟',
                                     weight=200)
        word2 = self._create_tipsword(keyword='植物大战僵尸',
                                     weight=1000)

        ws = TipsWord.objects.order_weight().all()
        ws = list(ws)
        first = ws[0]
        second = ws[1]
        self.assertEqual(first.keyword, '植物大战僵尸')
        self.assertEqual(first.weight, 1000)
        self.assertEqual(second.keyword, '愤怒的小鸟')
        self.assertEqual(second.weight, 200)

    def test_between_weight(self):
        w1= self._create_tipsword(keyword='愤怒的小鸟',
                                  weight=100)
        w2 = self._create_tipsword(keyword='魔兽世界',
                                   weight=200)
        w3  = self._create_tipsword(keyword='水果忍者',
                                    weight=300)
        w4  = self._create_tipsword(keyword='蜘蛛侠',
                                    weight=400)
        w5  = self._create_tipsword(keyword='我叫MT',
                                    weight=500)
        w6  = self._create_tipsword(keyword='生化危机',
                                    weight=600)
        w7  = self._create_tipsword(keyword='地牢围攻',
                                    weight=700)
        ws = TipsWord.objects.between_weight(300, 600).all()
        ws = list(ws)
        self.assertEqual(len(ws), 4)
        head = ws[0]
        tail=ws[-1]
        self.assertEqual(tail.keyword, '水果忍者')
        self.assertEqual(head.keyword, '生化危机')

    def test_order_random(self):
        w1= self._create_tipsword(keyword='愤怒的小鸟',
                                      weight=100)
        w2 = self._create_tipsword(keyword='魔兽世界',
                                      weight=200)
        w3  = self._create_tipsword(keyword='水果忍者',
                                      weight=300)
        w4  = self._create_tipsword(keyword='蜘蛛侠',
                                      weight=400)
        w5  = self._create_tipsword(keyword='我叫MT',
                                    weight=500)
        w6  = self._create_tipsword(keyword='生化危机',
                                    weight=600)
        w7  = self._create_tipsword(keyword='地牢围攻',
                                    weight=700)
        w8  = self._create_tipsword(keyword='罪恶之城',
                                    weight=800)
        w9  = self._create_tipsword(keyword='现代战争',
                                    weight=900)
        w10  = self._create_tipsword(keyword='蝙蝠侠',
                                    weight=1000)
        ws = TipsWord.objects.order_random().all()[0:5]
        ws = list(ws)
        self.assertEqual(len(ws), 5)
        self.assertNotEqual(
            ws,
            (w1, w2, w3, w4, w5)
        )
