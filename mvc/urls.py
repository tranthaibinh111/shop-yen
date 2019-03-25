from rest_framework import routers
from mvc.apis import *

urlpatterns = []

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name="users")

urlpatterns += router.urls
