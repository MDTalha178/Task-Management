import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from django.db import IntegrityError, DatabaseError
from apps.users.models import User
from apps.utils.messages import CustomError

logger = logging.getLogger(__name__)


class SignupSerializer(serializers.ModelSerializer):
    """
    This serializer class is used to serialize a signup data
    """

    name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(255)],
        error_messages={
            'required': CustomError.NAME_REQUIRED,
            'blank': CustomError.NAME_REQUIRED
        }
    )
    mobile = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(255)],
        error_messages={
            'required': CustomError.EMAIL_REQUIRED,
            'blank': CustomError.EMAIL_REQUIRED
        }
    )
    password = serializers.CharField(
        required=True, allow_null=False, allow_blank=False,
        error_messages={
            'required': CustomError.PASSWORD_REQUIRED,
            'blank': CustomError.PASSWORD_BLANK
        }
    )

    @staticmethod
    def validate_email(value):
        """
        This function is used to validate that the email is unique.
        """
        try:
            user = User.objects.get(email__iexact=value)
            raise serializers.ValidationError(CustomError.EMAIL_ALREADY_EXISTS)
        except ObjectDoesNotExist:
            pass
        return value

    def to_representation(self, obj):
        """
        This method is used to exclude the password from the response data.
        """
        attr = super().to_representation(obj)
        if 'password' in attr:
            attr.pop('password')
        return attr

    def create(self, validated_data):
        """
        This method is used to create a new user with the provided data.
        """
        try:
            password = validated_data.pop('password')
            user_obj = User.objects.create(**validated_data)
            print(validated_data)
            user_obj.set_password(password)
            user_obj.save()

            logger.info(f"User {user_obj.email} created successfully.")
            return user_obj

        except IntegrityError as e:
            logger.error(f"IntegrityError occurred: {str(e)}. Failed to create user.")
            raise serializers.ValidationError(CustomError.SERVER_NOT_ABLE_PROCESS_REQUEST)
        except DatabaseError as e:
            logger.error(f"DatabaseError occurred: {str(e)}. Failed to create user.")
            raise serializers.ValidationError(CustomError.SERVER_NOT_ABLE_PROCESS_REQUEST)
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating user: {str(e)}.")
            raise serializers.ValidationError(CustomError.SOMETHING_WENT_WRONG)

    class Meta:
        """
        Metaclass for SignupSerializer
        """
        model = User
        fields = ('email', 'name', 'mobile', 'password',)


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'mobile',)
        read_only_fields = fields
