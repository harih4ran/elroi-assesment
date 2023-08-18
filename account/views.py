from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User,Transaction
import csv
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from account.serializers import *

@api_view(['GET','POST'])
def UserAPI(request):
    if request.method == "GET":
        user = User.objects.all()
        serializer = UserSerializer(user,many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = UserSerializer(data = request.data)
        return Response(serializer.data)
    return Response('only supports get,post')

@api_view(['GET','POST'])
def TransactionAPI(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        serializer = TransactionSerializer(transaction,many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TransactionSerializer(data = request.data)
        return Response(serializer.data)
    return Response('only supports get,post')

@api_view(['POST'])
def MiniStatementAPI(request):
    if request.method == "POST":
        transaction = Transaction.objects.filter(user__account_number = data["account_number"],transfer_at__date__range = [data["start_date"],data["end_date"]])
        serializer = TransactionSerializer(transaction,many = True)
        return Response(serializer.data)
    return Response('only supports get,post')


def index(request):
    context = {
        "user":User.objects.all(),
        "transaction":Transaction.objects.all()
    }
    return render(request,'index.html',context)

def create_user(request):
    if request.method == "POST":
        if User.objects.filter(account_number = request.POST["account_number"]).exists():
            messages.add_message(request, messages.INFO, "Already Account Exists",extra_tags="create_user")
            return redirect('index')
        else:
            User.objects.create(
                name = request.POST["name"],
                account_number = request.POST["account_number"],
                current_balance = 0
            )
    else:
        return redirect('index')

def transfer_amount(request):
    if request.method == "POST":
        if not Transaction.objects.filter(user__account_number = request.POST["account_number"]).exists():
            messages.add_message(request, messages.INFO, "Invalid Account Number",extra_tags="transaction")
            return redirect('index')
        else:
            user = User.objects.get(account_number = request.POST["account_number"])
            Transaction.objects.create(
                amount = request.POST["amount"],
                transction_type = request.POST["transaction_type"],
                transfer_at = datetime.now(),
                user = user
            )

            if request.POST["transaction_type"] == "deposit":
                user.current_balance += float(request.POST["amount"])
                user.save()

            elif request.POST["transaction_type"] == "withdraw":
                user.current_balance -= float(request.POST["amount"])
                user.save()
    else:
        return redirect('index')

def download_csv(request):
    if request.method == "POST":
        if not Transaction.objects.filter(user__account_number = request.POST["account_number"]).exists():
            messages.add_message(request, messages.INFO, "Invalid Account Number",extra_tags="download_csv")
            return redirect('index')
        else:
            data = request.POST
            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = "attachment;filename=report.csv"
            writer = csv.writer(response)
            writer.writerow(["Name","Account_Number","Transaction_Date","Amount","Transaction_Type"])
            transaction = Transaction.objects.filter(user__account_number = data["account_number"],transfer_at__date__range = [data["start_date"],data["end_date"]])
            
            for i in transaction:
                writer.writerow([i.user.name,i.user.account_number,i.transfer_at,i.amount,i.transction_type])
            return response
    else:
        return redirect('index')
    