from behave import step

from behaving.personas.persona import Persona
from behaving.personas.persona import persona_vars


@step('"{name}" as the persona')
def given_a_persona(context, name):

    if name not in context.personas:
        context.personas[name] = Persona()
    context.persona = context.personas[name]

    if hasattr(context, 'browser'):
        context.execute_steps('Given browser "%s"' % name)


@step('I set "{key}" to "{val}"')
@persona_vars
def set_variable(context, key, val):
    assert context.persona is not None, 'no persona is setup'
    context.persona[key] = val


@step('"{key}" is set to "{val}"')
@persona_vars
def key_is_val(context, key, val):
    assert context.persona is not None, 'no persona is setup'
    assert key in context.persona, 'key not set'
    assert context.persona[key] == val, '%s != %s, values do not match' % (context.persona[key], val)
