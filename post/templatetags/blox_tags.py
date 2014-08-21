#-*- coding: utf-8 -*-
import os
from django import template
from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template

register = template.Library()

@register.filter
def debug_dir(o):
    """ Basit bir debug filter'i. """
    return str(dir(o))
