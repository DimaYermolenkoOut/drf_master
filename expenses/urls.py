from django.urls import path
from . import views


urlpatterns = [
    path('', views.ExpenseListView.as_view(), name='expenses'),
    path('<int:id>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
]

