from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework.permissions import AllowAny
from django.db.models import Q, Sum

# Create your views here.
class CategoryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            name = request.data.get("name", "")
            if Category.objects.filter(name=name).exists():
                return Response(
                    {"error": "Category already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, id=None):
        try:
            if id:
                try:
                    category = Category.objects.get(id=id)
                    serializer = CategorySerializer(category)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                except Category.DoesNotExist:
                    return Response(
                        {"error": "Category doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)

            if not categories.exists():
                return Response({"message": "No categories found."}, status=status.HTTP_200_OK)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, id):
        try:
            try:
                category = Category.objects.get(id=id)
            except Category.DoesNotExist:
                return Response(
                    {"error": "Category doesn't exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            name = request.data.get("name")
            if Category.objects.filter(name=name).exclude(id=id).exists():
                return Response(
                    {"error": "Category already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, id):
        try:
            try:
                category = Category.objects.get(id=id)
                category.delete()
                return Response(
                    {"message": "Category deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Category.DoesNotExist:
                return Response(
                    {"error": "Category not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def get(self, request, id=None):
        try:
            if id:
                try:
                    user = User.objects.get(id=id)
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response(
                        {"error": "User doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )

            users = User.objects.all()
            if not users.exists():
                return Response({"message": "No users found."}, status=status.HTTP_200_OK)

            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ExpenseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        
        
    def get(self, request, id=None):
        try:
            if id:
                try:
                    expense = Expense.objects.get(id=id)
                    serializer = ExpenseSerializer(expense)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                except Expense.DoesNotExist:
                    return Response(
                        {"error": "Expense doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )   
            filters = Q()
            user_id = request.query_params.get('user_id')
            if user_id:
                filters &= Q(user__id=user_id)

            expenses = Expense.objects.filter(filters).select_related('user', 'category').order_by('-date')
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def put(self, request, id):
        try:
            try:
                expense = Expense.objects.get(id=id)
            except Expense.DoesNotExist:
                return Response(
                    {"error": "Expense doesn't exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ExpenseSerializer(expense, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, id):
        try:
            try:
                expense = Expense.objects.get(id=id)
                expense.delete()
                return Response(
                    {"message": "Expense deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Expense.DoesNotExist:
                return Response(
                    {"error": "Expense not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ExpenseSummaryView(APIView):
    permission_classes = [AllowAny]        

    def get(self, request):
        try:
            filters = Q()
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            user_id = request.query_params.get('user_id')
            
            if user_id:
                filters &= Q(user__id=user_id)
            if year:
                filters &= Q(date__year=year)
            if month:
                filters &= Q(date__month=month)

            total_expenses = Expense.objects.filter(filters).select_related('user','category').aggregate(total=Sum('amount'))['total'] or 0
            
            expenses_by_category = Expense.objects.filter(filters).select_related('user','category').values('category__name').annotate(
                total_amount=Sum('amount')
            ).order_by('-total_amount')
            
            return Response({
                "total_expenses": str(total_expenses),
                "expenses_by_category": [
                    {
                        "category_name": item['category__name'] or "Uncategorized",
                        "total_amount": str(item['total_amount'])
                    }
                    for item in expenses_by_category
                ]
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )