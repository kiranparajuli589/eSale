from django.contrib.auth.models import User


def after_scenario(context, scenario):
    User.objects.filter(id__gt=1).delete()
