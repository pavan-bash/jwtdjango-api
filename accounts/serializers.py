from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
import re


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile=validated_data['mobile']
        )
        user.save()
        return user

    def validate(self, validated_data):
        # email validation
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError(
                {'emailError': "An account with this email already exists"})

        # password validation
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'passwordError': e})

        if password != password2:
            raise serializers.ValidationError(
                {'password2Error': "Passwords must match"})

        # mobile validation
        mobile = validated_data.get('mobile')
        if not re.fullmatch(r'^[6-9][0-9]{9}$', str(mobile)):
            raise serializers.ValidationError(
                {'mobileError': "Enter a valid mobile number"})

        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError(
                {'mobileError': 'This mobile number is already registered'})

        return validated_data

    class Meta:
        model = User
        fields = ['email', 'password', 'password2',
                  'first_name', 'last_name', 'mobile']
        extra_kwargs = {
            'password': {"write_only": True}
        }
