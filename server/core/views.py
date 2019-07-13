# core/view.py
from rest_framework.views import APIView
from rest_framework.response import Response


class UserDetails(APIView):
    """Get basic details of user"""

    def get(self, request):
        return Response({
            'name': request.user.first_name
        })
