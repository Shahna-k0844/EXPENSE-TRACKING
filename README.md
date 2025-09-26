Expense Tracker API
A Django REST Framework API for tracking expenses with user authentication, category management, and monthly summary reports.

Setup Instructions:

Python 3.13
SQLite

Design Choices:
Database Schema
Category Model:

name: Unique category name with max length 100

description: Optional text field for category details

Rationale: Simple structure allowing for flexible categorization
Expense Model:

user: ForeignKey to Django's User model (CASCADE delete)

category: ForeignKey to Category model (CASCADE delete)

amount: DecimalField with 10 digits and 2 decimal places

description: Optional text field for expense details

date: DateField with auto_now_add for creation timestamp

Key Design Decisions:

Decimal for amounts: Avoids floating-point precision issues

CASCADE delete: Ensures data integrity when users/categories are deleted

Foreign keys: Maintains relational integrity between expenses, users, and categories

Indexing: Django automatically indexes foreign keys for better performance

Assumptions:
User Authentication: Currently uses basic user_id passing for simplicity; production would require proper authentication

# Implementation example
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ExpenseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
