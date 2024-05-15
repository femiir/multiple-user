## Implementing JWT Authentication with django-ninja and Dockerizing the application

This tutorial builds off from the last project we developed in the previous tutorial. We will be adding JWT authentication to the project and dockerizing the application.

> you can clone the project from [github](git@github.com:femiir/multiple-user.git) and run the follow with the tutorial


I am a huge fan of the Django Ninja project i love to call myself the ninja disciple.

I say this all the time, but I will say it again. Authentication is a crucial part of any application. It is the process of verifying the identity of a user. There are several ways to implement authentication in an application. One of the most popular ways is to use JSON Web Tokens (JWT). 

JWT is a compact, URL-safe means of representing claims to be transferred between two parties. The claims in a JWT are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) structure or as the plaintext of a JSON Web Encryption (JWE) structure, enabling the claims to be digitally signed or integrity protected with a Message Authentication Code (MAC) and/or encrypted.

There have several packages that can be used to implement JWT authentication using ninja.Django-ninja implements several defaults options that you can use and allows you to implement your own custom authentication methods.

In this tutorial, we will be using the [`django-ninja-simple-jwt`]('https://github.com/oscarychen/django-ninja-simple-jwt) package. This package is a simple JWT authentication package that is easy to use and implement. It extends Django-ninja Bearer Authentication hence you do not need to worry about dependencies or other complexities.

Enough with the boring stuffs lets get to this.

### Step 1: Install the necessary packages

```zsh
pip install django-ninja-simple-jwt
```

### register the new app in `config/settings.py`
```python
# config/settings.py

...
INSTALLED_APPS = [
    ...
    # 3rd party apps
    'ninja_simple_jwt',
    # project apps
    'accounts.apps.AccountsConfig',
    'api.apps.ApiConfig',
    ...
]
...

```

### run the command below to generate the RSA keys that will be used to sign the JWT tokens
```zsh
python manage.py make_rsa
```

## update the following files with the new code

```python
# api/api.py
from ninja import Router...
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth # Import the HttpJwtAuth class from ninja_simple_jwt


...

@router.get('', response=Union[List[UserDetailSchema], dict], auth=HttpJwtAuth()) # auth=HttpJwtAuth() is used to authenticate the user
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
>Now we need to update routers to expose the access and refresh token endpoints

```python
from ninja_simple_jwt.auth.views.api import web_auth_router # Import the web_auth_router from ninja_simple_jwt

api = NinjaAPI()

api.add_router('/user', router)
api.add_router("/auth/", web_auth_router)
```

>I ran through this code this fast cause i want to challenge to try read the repo of the package and understand how it works or even fork the repo and try to implement your own custom authentication method.

### Step 2: Dockerize the application

[Docker](https://www.docker.com/) is becoming a default requirements for the development process.Docker is a platform for developing, shipping, and running applications in containers. It enables you to separate your applications from your infrastructure so you can deliver software quickly.

```zsh
docker init
```
> This command will create the following files with sensible defaults for your project: 
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

> The utility will ask you a few questions about your application platform, version, port, and command to run your app. It will then create the necessary files with the information you provided.

your terminal output should look like this depending on the version of python you are using
```zsh                                
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.12.3
? What port do you want your app to listen on? 8000
? What is the command you use to run your app? gunicorn 'config.wsgi' --bind=0.0.0.0:8000

✔ Created → .dockerignore
✔ Created → Dockerfile
✔ Created → compose.yaml
✔ Created → README.Docker.md

→ Your Docker files are ready!
  Review your Docker files and tailor them to your application.
  Consult README.Docker.md for information about using the generated files.

! Warning → No requirements.txt file found. Create one with the dependencies for your application, including an entry for the gunicorn package, before running it.

What's next?
  Start your application by running → docker compose up --build
  Your application will be available at http://localhost:8000
```


### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.


> you can clone this project from [github]('https://github.com/femiir/multiple-user/tree/jwt')


> I hope you enjoyed this tutorial. If you have any questions or suggestions, feel free to reach out to me on [Twitter](https://twitter.com/femiiir) or [LinkedIn](https://www.linkedin.com/in/femiir/). I would love to hear from you.



('https://github.com/femiir/multiple-user/tree/jwt')
### References
* [Docker's Python guide](https://docs.docker.com/language/python/)


