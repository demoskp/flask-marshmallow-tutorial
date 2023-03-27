from marshmallow import validates_schema, validate
from marshmallow.fields import String
from werkzeug.routing import ValidationError

from extensions import ma
from models.users import User


class UserUpdateSchema(ma.SQLAlchemyAutoSchema):
    name = String(required=True, validate=validate.Length(min=3), error_messages={
        "required": "The name is required",
        "invalid": "The name is invalid",
    })

    class Meta:
        model = User
        exclude = ["id"]


class UserSchema(UserUpdateSchema):
    email = String(required=True, validate=validate.Email())

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")

        if User.query.filter_by(email=email).count():
            raise ValidationError(f"User with email: {email} already exists")

