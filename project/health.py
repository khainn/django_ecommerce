from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers


@extend_schema(
    tags=['Health'],
    summary="API Health Check",
    description="Simple health check endpoint that confirms the API is running",
    methods=['GET', 'HEAD'],
    responses={
        200: inline_serializer(
            name='HealthCheckResponse',
            fields={
                'status': serializers.CharField(),
            }
        )
    }
)
@api_view(['GET', 'HEAD'])
@permission_classes([])
@authentication_classes([])
def health_check(request):
    """
    Basic health check endpoint.
    Returns a simple status check to confirm the API is running.
    """
    return JsonResponse({
        'status': 'ok',
    })