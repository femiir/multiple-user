from ninja import Router
from .schema import UserRegisterSchema, UserDetailSchema
from accounts.models import Business, Client, User
from typing import List, Union
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth # Import the HttpJwtAuth class from ninja_simple_jwt

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
