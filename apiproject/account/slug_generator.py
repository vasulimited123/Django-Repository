from django.utils.text import slugify
from account.models import *
from django.db import models
import random
import string

def random_string_generator(size):
    rnd = ""
    chars = string.ascii_lowercase + string.digits
    for i in range(size):
        rnd = rnd + random.choice(chars)
    return rnd

def unique_slug_generator(instance,new_slug=None):
    if new_slug is not None:
        slug = new_slug

    else:
        slug = slugify(instance.company)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{rndstr}".format(slug=slug,rndstr=random_string_generator(size=4))
        return unique_slug_generator(instance,new_slug)

    return slug           
