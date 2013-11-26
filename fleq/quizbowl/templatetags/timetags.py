from django import template
import datetime
register = template.Library()

def add_hours(d, value):
    return d + datetime.timedelta(minutes=value*60)

register.filter(add_hours)