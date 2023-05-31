from django import template
from jdatetime import datetime 


register = template.Library()

@register.simple_tag(name='j_date_time')
def j_date_time(d):
    return datetime.fromgregorian(date=d).strftime(' %H:%M:%S - %Y/%m/%d ')
    
    

