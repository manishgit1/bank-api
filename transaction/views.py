
from activation.models import AppUser
from .models import Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from .seriliazers import TransactionSerializer
from rest_framework import status, permissions
from django.db import models
from django.shortcuts import get_object_or_404
from knox.auth  import TokenAuthentication
from .permissions import IsVerified





#logic for handling fund transfers
class BalanceTransferView(APIView):
      permission_classes = (permissions.IsAuthenticated, IsVerified, )
      authentication_classes = (TokenAuthentication, )
     
      def post(self, request):
            #balance transfer logic here
        
            sender = request.user
            receiver_name = request.data['receiver_name']
            receiver_account_number = request.data['receiver_account_number']
            amount = int(request.data['amount'])
            transaction_pin = str(request.data['transaction_pin'])
            remarks = request.data.get('remarks')
        
           # print( receiver_name, receiver_account_number, amount, transaction_pin, remarks, sender.transaction_pin)
            


            try:
                  receiver = get_object_or_404(AppUser, account_number=receiver_account_number, name=receiver_name)


            except AppUser.DoesNotExist:
                  return Response({'error': 'Recipient not found!! '}, status=status.HTTP_404_NOT_FOUND)
            
            if sender.account_number == receiver.account_number:
                  return Response({'error': 'Transaction not allowed!!!'}, status=status.HTTP_400_BAD_REQUEST)
            
            if sender.account_balance < amount:
                  return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            
            if transaction_pin != sender.transaction_pin:
                 return Response({'error': 'Invalid Transaction Pin'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if receiver.is_verified is not True:
                  return Response({'error': 'Cannot make transaction to this receiver account'}, status=status.HTTP_400_BAD_REQUEST)
            
            #update account balance
            sender.account_balance -= amount
            receiver.account_balance += amount


            #create transaction record
            transaction = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount, remarks=remarks, status=True)

            sender.save()
            receiver.save()

            serializer = TransactionSerializer(transaction)
            

            return Response(serializer.data, status=status.HTTP_201_CREATED)
      

#return the current balance of user 
class BalanceCheckView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsVerified)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
          balance = request.user.account_balance
          return Response({'account-balance': balance}, status=status.HTTP_200_OK)    


#return transaction records of user
class TransactionHistoryView(APIView):
      permission_classes = (permissions.IsAuthenticated, IsVerified)
      authentication_classes = (TokenAuthentication,)

      def get(self, request):
            user = request.user

            #Retrieve the user's transaction history
            transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

            #serializer the transactions
            serializer = TransactionSerializer(transactions, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
      

class TransactionSummary(APIView):
      permission_classes = (permissions.IsAuthenticated,IsVerified)
      authentication_classes = (TokenAuthentication,)


      def get(self,request):
            user = request.user
            sent_transactions = Transaction.objects.filter(sender=user)
            received_transactions = Transaction.objects.filter(receiver=user)


            total_expenses = sent_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0
            total_income = received_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0

            return Response({
                  'total_income': total_income,
                  'total_expenses': total_expenses
            }, status=status.HTTP_200_OK)
      


