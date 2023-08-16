from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user."""

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
  """
  This serializer defines two fields for authentication:
    * username
    * password.
  It will try to authenticate the user with when validated.
  """
  username = serializers.CharField(
    label="Username",
    write_only=True
  )
  password = serializers.CharField(
    label="Password",
    # This will be used when the DRF browsable API is enabled
    style={'input_type': 'password'},
    trim_whitespace=False,
    write_only=True
  )

  def validate(self, attrs):
    # Take username and password from request
    username = attrs.get('username')
    password = attrs.get('password')

    if username and password:
      # Try to authenticate the user using Django auth framework.
      user = authenticate(request=self.context.get('request'),
                          username=username, password=password)
      if not user:
        # If we don't have a regular user, raise a ValidationError
        msg = 'Access denied: wrong username or password.'
        raise serializers.ValidationError(msg, code='authorization')
    else:
      msg = 'Both "username" and "password" are required.'
      raise serializers.ValidationError(msg, code='authorization')
    # We have a valid user, put it in the serializer's validated_data.
    # It will be used in the view.
    attrs['user'] = user
    return attrs