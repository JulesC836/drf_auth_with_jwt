from django.contrib.auth.models import Group
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)       
    
    class Meta:
        model = User
        fields = ['url','first_name','last_name','email','gender','birthdate','password','password_confirm', 'profile', 'groups']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm') # On retire le champ de confirmation
        user = User.objects.create_user(**validated_data)
        return user

    
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.EmailField(label=_("Email ou nom d'utilisateur"), required=True)
#     password = serializers.CharField(label=_("Mot de pass"), required=True)

#     class Meta:
#         fields = ['password', 'password_cofirm']

#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')

#         if username and password:
            
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)

#             # L'objet 'user' sera 'None' si l'authentification échoue.
#             if not user:
#                 msg = _('Impossible de se connecter avec les identifiants fournis.')
#                 raise serializers.ValidationError(msg, code='authorization')

#         else:
#             msg = _('Vous devez inclure "username" et "password".')
#             raise serializers.ValidationError(msg, code='authorization')

#         # Si l'authentification réussit, nous stockons l'objet 'user'
#         # dans les données validées pour une utilisation ultérieure.
#         data['user'] = user
#         return data
        

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']