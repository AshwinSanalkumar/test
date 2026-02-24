from django.contrib.auth.models import User # This uses Django's built-in User

class AuthService:
    @staticmethod
    def register_user(validated_data: dict) -> User:
        """
        Business Logic: Normalizes data and persists user.
        """
        return User.objects.create_user(
            username=validated_data['username'].lower().strip(),
            email=validated_data['email'].lower().strip(),
            password=validated_data['password'],
            first_name=validated_data['first_name'].strip().capitalize(),
            last_name=validated_data['last_name'].strip().capitalize()
        )
    
class ArithmeticService:
    @staticmethod
    def add(num1,num2):
        try:
            return float(num1) + float(num2)
        except (ValueError,TypeError):
            return None
        
    @staticmethod
    def difference(num1,num2):
        try:
            return float(num1) - float(num2)
        except (ValueError,TypeError):
            return None
        
    @staticmethod
    def quotient(num1 , num2):
        try:
            if float(num2)==0:
                return None
            return float(num1) / float (num2)
        except (ValueError,TypeError):
            return None