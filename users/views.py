from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Login 

class LoginStatsView(APIView):
    def get(self, request):
        logins = Login.objects.all()  
        login_count = logins.count()
        
        return Response({
            'login_count': login_count,
            'logins': [{'user': login.user.email, 'timestamp': login.timestamp} for login in logins]
        })
