# 🪲 DarkReport 
Sometimes you dont find a tool than satisfies your requirements. 
DarkReport is my own way of reporting tools. 
I write in with Django Framework, with only two goals in mind:
- Make it easy to use.
- Make it fast on doing reports. 

## Advise!!
Modify  DEBUG = True to false if you run in production
remember to adjust settings.py for static if you are on production
Run like any django project
``` 
python manage.py runserver
```

# Setup admin
``` 
python manage.py shell
```
now in the django shell:
```
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user(username="admin", password="admin")
```

## **Under development!!** 