from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username','password','email','confirm_password','first_name','last_name']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        # validate passwords
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # hashes the password
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


