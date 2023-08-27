# Import necessary modules for creating serializers
from rest_framework import serializers
from .models import Category, Server, Channel

# Serializer for Channel model
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"  # Include all fields from the Channel model

# Serializer for Server model
class ServerSerializer(serializers.ModelSerializer):
    # SerializerMethodField to dynamically compute 'num_members'
    num_members = serializers.SerializerMethodField()
    
    # Nested serializer to serialize related Channel objects
    channel_server = ChannelSerializer(many=True)
    
    class Meta:
        model = Server
        exclude = ("member",)  # Exclude 'member' field from serialization

    # Custom method to get the 'num_members' field
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None 

    # Custom representation method to conditionally remove 'num_members' field
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data
