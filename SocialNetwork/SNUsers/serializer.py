from rest_framework import serializers
from SNUsers.models import SNUser
 
class SNUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNUser
        fields = '__all__'