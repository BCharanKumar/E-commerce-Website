from app.models import *
def data_user(request):
    UO=None
    if request.user.is_authenticated:
        email=request.session.get('email')
        if email:
            try:
                UO=Customer.objects.get(email=email)
            except Customer.DoesNotExiist:
                UO=None
    return {"UO":UO}
