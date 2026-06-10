from django.urls import path, i18n_patterns
from . import views

urlpatterns = i18n_patterns(
    path('', views.menu_list, name='menu_list'),
    path('<int:pk>/', views.menu_detail, name='menu_detail'),
    path('admin/', views.admin_view, name='admin_view'),
    prefix_default_language=True,
)

