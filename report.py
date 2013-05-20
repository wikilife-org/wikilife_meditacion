
from questions.models import *
import settings
import os


def xls():
    
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    
    polls = Poll.objects.all()
    for p in polls:
        print p
    person = Person.objects.all()
    
    

if __name__ == "__main__":
    xls()