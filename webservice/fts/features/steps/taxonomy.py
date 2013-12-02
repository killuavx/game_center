# -*- coding: utf-8 -*-
from behave import *
from should_dsl import should_not
from fts.features.app_dsls.taxonomy import factory_dsl
from fts.features.app_dsls.web import factory_dsl as factory_web_dsl
from django.contrib.contenttypes.models import ContentType


def content_type_get_object_for_this_type(
        content_type, object_field, object_value):
    content_type |should_not| be(None)
    ct = ContentType.objects.get(model=content_type)
    obj = ct.get_object_for_this_type(**{
        object_field: object_value
    })
    return obj

@given('topic exists such below')
def create_topics_on_below(context):
    TaxonomyDSL = factory_dsl(context)
    for row in context.table:
        TaxonomyDSL.create_topic(context, **row.as_dict())

@given('topic slug "{slug}" have own items such below')
def add_to_topic_on_below(context, slug):
    TaxonomyDSL = factory_dsl(context)
    topic = TaxonomyDSL.get_taxonomy_by(slug=slug)
    for row in context.table:
        obj = content_type_get_object_for_this_type(
            content_type=row.get('content_type'),
            object_field=row.get('object_field'),
            object_value=row.get('object_value')
        )
        TaxonomyDSL.add_to_topic(context=context,
                                 topic=topic,
                                 content=obj,
                                 ordering=row.get('ordering'))

@when('I visit topic detail page slug "{slug}"')
def visit_topic_detail_page(context, slug):
    TaxonomyDSL = factory_dsl(context)
    TaxonomyDSL.visit_topic_detail_page(
        context=context, topic=TaxonomyDSL.get_taxonomy_by(slug=slug))

    factory_web_dsl(context).response_to_world(context)

@given('category "{name}" as root already exists')
def create_category_as_root(context, name):
    TaxonomyDSL = factory_dsl(context)
    TaxonomyDSL.create_category(context, name)

@given('category tree exists')
def category_tree_already_exists(context):
    TaxonomyDSL = factory_dsl(context)
    TaxonomyDSL.category_tree_already_exists(context)

@given('I hide the category')
@given('I hide the category name "{name}"')
def hide_the_category(context, name=None):
    TaxonomyDSL = factory_dsl(context)
    if name is not None:
        focus_on_category(context, name)
    category = context.world.get('the_category')
    TaxonomyDSL.hide_the_category(context, category)

@given('I focus on category "{name}"')
def focus_on_category(context, name):
    TaxonomyDSL = factory_dsl(context)
    category = TaxonomyDSL.get_category_by(name)
    context.world.update(dict(the_category=category))

@when('I visit category page')
def visit_category_page(context):
    TaxonomyDSL = factory_dsl(context)
    TaxonomyDSL.visit_category_page(context)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

@when('I visit package list of category {field} "{name}"')
@when('I visit package list of category {field} "{name}" paginate by "{page_size:d}"')
def visit_the_package_list_of_category(context, field, name, page_size=None):
    TaxonomyDSL = factory_dsl(context)
    TaxonomyDSL.visit_the_package_list_of_category(
        context,
        page_size,
        **{field: name})

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)

@then('I should see the category {is_in:in?} result tree')
@then('I should see the category "{name}" {is_in:in?} result tree')
def should_category_in_reuslt_tree(context, is_in, name=None):
    if name is not None:
        focus_on_category(context, name)
    the_category = context.world.get('the_category')

    step_str_1 = 'Then I should see list result without pagination'
    step_str_2 = 'contains the name of element is "%s"' % the_category.name
    _template = "%s %s" if is_in else "%s not %s"
    context.execute_steps(_template %(step_str_1, step_str_2))

@when('I visit the category detail page')
def visit_category_detail_page(context):
    the_category = context.world.get('the_category')
    TaxonomyDSL = factory_dsl(context)
    TaxonomyDSL.visit_category_detail_page(context, the_category)

    WebDSL = factory_web_dsl(context)
    WebDSL.response_to_world(context)
