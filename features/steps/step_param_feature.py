from behave import given, when, then
from features.main.Blender import Blender
from features.main.Frobulator import Frobulator
from features.main.company_model import CompanyModel
from features.main.test_util import NamedNumber
from hamcrest import assert_that, has_items
from hamcrest.library.collection.issequence_containinginanyorder \
    import contains_inanyorder


@given('I put "{thing}" in a blender')
def step_given_put_thing_into_blender(context, thing):
    context.blender = Blender()
    context.blender.add(thing)


@when('I switch the blender on')
def step_when_switch_blender_on(context):
    context.blender.switch_on()


@then('it should transform into "{other_thing}"')
def step_then_should_transform_into(context, other_thing):
    other_thing.should.equal(context.blender.result)


@given('a sample text loaded into the frobulator')
def step_impl(context):
    frobulator = getattr(context, "frobulator", None)
    if not frobulator:
        context.frobulator = Frobulator()
    context.frobulator.text = context.text  # STEP-DATA from context.text


@when('we activate the frobulator')
def step_impl(context):
    context.frobulator.activate()


@then('we will find it similar to {language}')
def step_impl(context, language):
    language.should.equal(context.frobulator.seems_like_language())


@given('a set of specific users')
def step_impl(context):
    model = getattr(context, "model", None)
    if not model:
        context.model = CompanyModel()
    for row in context.table:
        context.model.add_user(row["name"], deparment=row["department"])


@when('we count the number of people in each department')
def step_impl(context):
    context.model.count_persons_per_department()


@then('we will find {count} people in "{department}"')
def step_impl(context, count, department):
    count_ = NamedNumber.from_string(count)
    count_.should.equal(context.model.get_headcount_for(department))


@then('we will find one person in "{department}"')
def step_impl(context, department):
    (1).should.equal(context.model.get_headcount_for(department))


@then('we will have the following people in "{department}"')
def step_impl(context, department):
    """
    Compares expected with actual persons in a department.
    NOTE: Unordered comparison (ordering is not important).
    """
    department_ = context.model.departments.get(department, None)
    if not department_:
        raise AssertionError("Department {} is unknown".format(department))
    # -- NORMAl-CASE:
    expected_persons = [row["name"] for row in context.table]
    actual_persons = department_.members

    # -- UNORDERED TABLE-COMPARISON (using: pyhamcrest)
    assert_that(contains_inanyorder(*expected_persons), actual_persons)


@then('we will have at least the following people in "{department}"')
def step_impl(context, department):
    """
    Compares subset of persons with actual persons in a department.
    NOTE: Unordered subset comparison.
    """
    department_ = context.model.departments.get(department, None)
    if not department_:
        assert_that(False, "Department %s is unknown" % department)
        # -- NORMAl-CASE:
    expected_persons = [row["name"] for row in context.table]
    actual_persons = department_.members

    # -- TABLE-SUBSET-COMPARISON (using: pyhamcrest)
    assert_that(has_items(*expected_persons), actual_persons)
