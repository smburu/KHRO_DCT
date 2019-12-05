from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, Serializer,
    ReadOnlyField)

from khro_app.authentication.models import (CustomUser, CustomGroup,)

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'title', 'gender', 'email', 'postcode', 'username',
            'location']


class CustomGroupSerializer(ModelSerializer):
    group_id = ReadOnlyField(source='group.id')
    class Meta:
        model = CustomGroup
        fields = ['group_id', 'group_manager']
