# Import necessary modules
from rest_framework import viewsets
from .serializer import ServerSerializer, CategorySerializer
from .models import Server, Category
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs
from drf_spectacular.utils import extend_schema

# Create a viewset for handling server list operations


class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ServerListViewSet(viewsets.ViewSet):
    # Set the initial queryset to include all Server objects
    queryset = Server.objects.all()
    # permission_classes = [IsAuthenticated]

    # Define the list method to handle GET requests for the server list
    @server_list_docs
    def list(self, request):
        # Get query parameters from the request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("serverid")
        with_num_members = request.query_params.get(
            "with_num_members") == "true"

        # Check if the request is trying to filter by user, and if so, check authentication
        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Apply category filter if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Apply user filter if provided
        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed

        # Annotate the queryset with the count of members if requested
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Apply quantity limit if provided
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Apply server ID filter if provided
        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(
                    detail=f"Server with id {by_serverid} not found")

        # Serialize the queryset using the ServerSerializer
        serializer = ServerSerializer(self.queryset, many=True, context={
                                      "num_members": with_num_members})

        # Return the serialized data as a response
        return Response(serializer.data)
