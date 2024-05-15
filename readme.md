# Creating a scalable Django project with multiple user types using using proxy models and 🥷🏾🥷🏾Django-ninja 🥷🏾🥷🏾
Some kinds of projects may have authentication requirements for which [Django's](https://docs.djangoproject.com/en/5.0/) built-in User model is not always appropriate.

Often times you have to create a project that has multiple user types models, for example, a project that has business users and client users, Doctors, Nurses and Patient, or even a School administration system where you have Students, Teachers and Admin etc. This is not an uncommon requirements in projects and it is important to know how to implement this in.

Django allows you to override the default user model by providing a value for the AUTH_USER_MODEL setting that references a custom model

> There are several ways to implement this in Django
- Ceate a single user model with a user_type field that defines the type of user
- Use Boolean Fields
- Concrete models

Dare i say Django comes shipped with an authentication system that covers most average system requirements. Knowing this allows you to capitalize on this 

Django has a way to handle this using proxy models. Proxy models allow you to create a new model with the same fields as an existing model. This is useful when you want to change the behavior of the original model, but don’t want to change the original model itself. Proxy models are created using the ```Meta``` option proxy = ```True.```

In this tutorial, we will create a Django project that has two user types, business users, and client users. We will use proxy models to create the two user types and django-ninja to create an API for the project.

> Prerequisites
- Basic knowledge of Django
- Basic knowledge of RESTful API's
- Virtual Enviroments 

### Create env with tool of your choice.
*conda is used for this tutorial. Feel free to use any env manager of choice*
```zsh
conda create -n multipleuser
```

### Activate the model
```zsh
conda activate multipleuser
```

###  Install the packages
```zsh
pip install Django django-ninja
```
### start a django project

```zsh
django-admin startproject config
```
### Start an app 
```zsh
django-admin startapp accounts
```

# Create custom user
The easiest way to construct a compliant custom user model is to inherit from ```AbstractBaseUser```. ```AbstractBaseUser``` provides the core implementation of a user model, including hashed passwords and tokenized password resets.

>**AbstractUser:** Use this option if you are happy with the existing fields on the user model and just want to remove the username field.

>**AbstractBaseUser:** Use this option if you want to start from scratch by creating your own, completely new user model.


### we choose AbstractUser for simplicity.
To read more about this topic check out the following
- scoops of django by Audrey Greenfeld and Daniel Roy Greenfeld
- https://testdriven.io/blog/django-custom-user-model/
- https://docs.djangoproject.com/en/5.0/topics/auth/customizing/

# Approach to this design
>I like the make my models as flexible as possible which sees me trying to reduce the amount of hard coding i have to do.<br>So i create a Roles model that will allow for as many user types to be created.What this allows me to do is link this model to my user table in any requirements my system needs either as <br>- foriegn keys(roles can be updated)<br>- One to one(user can be of specific type)<br>- Many to many(user can have multiple roles)

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import BusinessManager, ClientManager


# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```
> always good to create a Timestamped model where other models can inherit from
```python
class Roles(TimeStampedModel):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        db_table = 'roles'

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)
    user_role = models.ForeignKey(
        Roles, on_delete=models.CASCADE, null=True, blank=True
    )


class Business(User):
    objects = BusinessManager()

    def save(self, *args, **kwargs):
        if not self.user_role:
            self.user_role, created = Roles.objects.get_or_create(
                name='Business', description='Business User Account'
            )
        super().save(*args, **kwargs)

    class Meta:
        proxy = True


class Client(User):
    objects = ClientManager()

    def save(self, *args, **kwargs):
        if not self.user_role:
            self.user_role, created = Roles.objects.get_or_create(
                name='Client', description='Client User Account'
            )
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
```
### create the manager in accounts/managers.py
```python
# accounts/managers.py
from django.db import models
from django.db.models.query import QuerySet


class BusinessManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(user_role__name='Business')


class ClientManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(user_role__name='Client')
```
    

>Dont forget to point to the custom user in settings.py ```AUTH_USER_MODEL = 'accounts.User'```

```python
# accounts/admin.py
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Roles, Business, Client
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Roles)
admin.site.register(Business)
admin.site.register(Client)
```

> Now is a good time to make migrations and migrate our user model
```zsh
python manage.py makemigrations
python manage.py migrate
```
Now you have yourself a pluggable user app you can use for all your needs.


#### create the super user 
```zsh
python manage.py createsuperuser
```

### create the api app
You can call me the 🥷🏾🥷🏾[Django-ninja](https://django-ninja.dev/)🥷🏾🥷🏾 evangelist/disciple...I love love love the project and i try to introduce it any way or shape i can. Nothing against OG DjangoRestFramework.

you can should definetly give the project a try 😎😎
```zsh
django-admin startapp api
```

### register the new app in config/settings.py
```python
# config/settings.py

...
INSTALLED_APPS = [
    ...
    'api.apps.ApiConfig',
    ...
]
...
```

### Create a schema, router, and api scripts
```zsh
touch api/schema.py
touch api/routers.py
touch api/scripts.py
```

>Schema in django-ninja is what serializers are to DjangoRestFramework

>Router in django-ninja is where I configure my URL's

>api can be seen as views 

*you can delete the ~~api/admin~~, ~~api/views~~, ~~api/models~~*
### Schema
Schema converts django ORM to native pydantic types which gives you quick field validation out of the box. eg Enums, email, IPAddress, URLs, JSON,.It also gives you the ability to validate Fields, Nested models, and even create custom fields.

```python
# api/schema.py
from typing import Optional
from ninja import ModelSchema, Schema
from accounts.models import User, Roles

class RolesSchema(ModelSchema):
    class Meta:
        model = Roles
        fields = [
            'id',
            'name',
            'description',
        ]

class UserRegisterSchema(ModelSchema):
    user_role: str
    class Meta:
        model = User
        fields = [
            'username',
            'nickname',
            'password',
            'user_role',
        ]

# a response schema 👍🏾
class UserDetailSchema(Schema):
    id: int
    username: str
    nickname: str
    user_role: Optional[RolesSchema] = None  
```
### Routers
If you are familiar with djangorestframework and  understand viewsets and routers, then you will understand the concept of routers in django-ninja.

```python
# api/routers.py
from ninja import NinjaAPI
from .api import router as user_router

api = NinjaAPI()

api.add_router('/user', user_router)

```

### API
This is where the magic happens. This is where you define your views and the logic that goes with it.
we design the api to create a user and list users based on the user type.

```python
# api/api.py
from ninja import Router
from .schema import UserRegisterSchema, UserDetailSchema
from accounts.models import Business, Client, User
from typing import List, Union

router = Router()
# Create your views here.
@router.post('create_user', response=UserDetailSchema)
def create_user(request, payload: UserRegisterSchema):
    payload_dict = payload.dict()
    user_role = payload_dict.pop('user_role')
    password = payload_dict.pop('password')

    if user_role == 'business':
        user = Business(**payload_dict)
    elif user_role == 'client':
        user = Client(**payload_dict)
    
    # Hash the password
    user.set_password(password)
    user.save()
    return user


@router.get('', response=Union[List[UserDetailSchema], dict])
def list_users(request, user_type: str = 'all'):
    if user_type == 'business':
        queryset = Business.objects.all()
        total_user = f'Total business users: {queryset.count()}'
    elif user_type == 'client':
        queryset = Client.objects.all()
        total_user = f'Total client users: {queryset.count()}'
    else:
        queryset = User.objects.all()
        total_user = f'Total users[Business/Client]: {queryset.count()}'

    serialized_data = []
    for user in queryset:
        user_dict = UserDetailSchema.from_orm(user).dict()

        # Check if user_role is None and if the user is a superuser
        if user_dict['user_role'] is None and user.is_superuser:
            user_dict['user_role'] = {
                'id': None,
                'name': 'Superuser',
                'description': 'Superuser Account',
            }

        serialized_data.append(user_dict)

    return {'total_user': total_user, 'users': serialized_data}
```
>Notice how you need only one endpoint to create users of different types. This is the power of proxy models and the managers we created earlier.

```python
# config/urls.py
from django.contrib import admin
from django.urls import path
from api import routers  # import routers from api

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('api/', routers.api.urls),
]
```
You can run the server ```python.manage.py runserver``` and test the api endpoints by navigating to ```localhost:8000/api/docs```.

🥷🏾🥷🏾Ninja 🥷🏾🥷🏾 out of the box provides documentation that allows you to test your endpoints. You can also test the endpoints using postman or any other API testing tool of your choice.

> you can clone this project from [github](git@github.com:femiir/multiple-user.git) and run the project to see how it works.

> At the end of the project your folder structure should look like 
```bash
├── config
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts
│   ├── migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py
│   ├── tests.py
│   ├── views.py
│   └── managers.py
├── api
│   ├── migrations
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── apps.py
│   ├── api.py
│   ├── tests.py
│   ├── routers.py
│   └── schema.py
├── manage.py
├── db.sqlite3
```

## To move this project to production you want to consider looking into the following suggestions
- managing secrets, keys and passwords
- using something like hacksoft django project style-guide or cookiecutter for managing consistent best practice
- use a production ready database like postgres
- containerization 
- adding extra fields to the user roles 

### This project focus on using ninja and django to develop a mutilple user system that is scalable 

> I hope you enjoyed this tutorial. If you have any questions or suggestions, feel free to reach out to me on [Twitter](https://twitter.com/femiiir) or [LinkedIn](https://www.linkedin.com/in/femiir/). I would love to hear from you.



