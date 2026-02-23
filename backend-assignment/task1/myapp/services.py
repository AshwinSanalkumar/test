from .models import User

class AuthService:
    @staticmethod
    def register_user(validated_data: dict) -> User:
        """
        Business Logic: Normalizes data and persists user.
        Note: password_confirm is handled by the serializer, not here.
        """
        return User.objects.create_user(
            email=validated_data['email'].lower().strip(),
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'].strip().capitalize(),
            last_name=validated_data['last_name'].strip().capitalize()
        )
    