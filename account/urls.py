from django.urls import path
from account.views import *

urlpatterns = [

    # jinja
    path('', index,name="index"),
    path('download_csv', download_csv,name="download_csv"),
    path('create_user', create_user,name="create_user"),
    path('transfer_amount', transfer_amount,name="transfer_amount"),

    # api
    path('api/v1/user', UserAPI),
    path('api/v1/transaction', TransactionAPI),
    path('api/v1/ministatement', MiniStatementAPI),
]
