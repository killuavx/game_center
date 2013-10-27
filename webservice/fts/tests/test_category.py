# -*- encoding: utf-8-*-
from fts.helpers import ApiDSL, RestApiTest
from fts import helpers
from taxonomy.models import Category
from pprint import pprint as print

class CategoryRestApiTest(RestApiTest):

    fixtures = ['categories.json']

    def test_fixture_get_ready(self):
        self.assertEqual(18, Category.objects.count())
        self.assertEqual(1, Category.objects.as_root().count())

    def test_category_tree(self):
        ApiDSL.When_i_access_category_list(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        results = self.world.get('content')
        self.assertEqual(1, len(results))
        game = results[0]

    def test_category_detail(self):
        game = Category.objects.as_root().get()
        ApiDSL.When_i_access_category_detail(self, category=game)
        ApiDSL.Then_i_should_receive_success_response(self)
        cat_data = self.world.get('content')
        ApiDSL.Then_i_should_see_category_detail(self, cat_data)

    def test_depth2_category_detail(self):
        game = Category.objects.as_root().get()
        cat_depth2 = game.children.all()[0]
        ApiDSL.When_i_access_category_detail(self, category=cat_depth2)
        ApiDSL.Then_i_should_receive_success_response(self)
        cat_data = self.world.get('content')
        ApiDSL.Then_i_should_see_category_detail(self, cat_data)

    def test_hidden_category_not_show_in_category_page(self):
        new_root_cat = helpers.create_category(name="new root category")
        ApiDSL.When_i_access_category_list(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_the_category_in_category_tree(self,
                                                               new_root_cat)

        new_root_cat.is_hidden = True
        new_root_cat.save()
        ApiDSL.When_i_access_category_list(self)
        ApiDSL.Then_i_should_receive_success_response(self)
        ApiDSL.Then_i_should_see_the_category_in_category_tree(self,
                                                               new_root_cat,
                                                               flag=False)
        ApiDSL.When_i_access_category_detail(self, new_root_cat)
        ApiDSL.Then_i_should_receive_success_response(self)
        cat_data = self.world.get('content')
        ApiDSL.Then_i_should_see_category_detail(self, cat_data)


