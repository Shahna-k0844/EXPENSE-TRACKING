from django.urls import path
from . views import *

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<int:id>/', CategoryView.as_view(), name='category-detail'),
    path('users/', UserView.as_view(), name='users'),
    path('users/<int:id>/', UserView.as_view(), name='user-detail'),
    path('expenses/', ExpenseView.as_view(), name='expenses'),
    path('expenses/<int:id>/', ExpenseView.as_view(), name='expense-detail'),
    path('reports/monthly_summary', ExpenseSummaryView.as_view(), name='reports'),
]
