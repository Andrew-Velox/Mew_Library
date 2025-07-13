
from django.contrib import admin
from django.urls import path,include
from core.views import HomeView


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name = 'homepage'),
    path('categories/<slug:category_slug>/', HomeView, name = 'categories'),
    path('account/', include('account.urls')),
    path('transactions/', include('transactions.urls')),
    path('books/', include('books.urls')),
    

]


urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)