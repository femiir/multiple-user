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


class UserDetailSchema(Schema):
    id: int
    username: str
    nickname: str
    user_role: Optional[RolesSchema] = None  
