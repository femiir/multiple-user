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
    if user_role == 'business':
        user = Business(**payload_dict)
        user.save()
    elif user_role == 'client':
        user = Client(**payload_dict)
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
