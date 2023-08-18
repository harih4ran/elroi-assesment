from django.db import models

TRANSACTION_TYPE = [
    ('deposit','deposit'),
    ('withdraw','withdraw'),
]

class User(models.Model):
    name = models.CharField(max_length = 100,blank = False)
    account_number = models.IntegerField(blank = False)
    current_balance = models.FloatField(blank = False)
    created_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank = False)
    amount = models.FloatField(blank = False)
    transction_type = models.CharField(max_length = 100,blank = False,choices = TRANSACTION_TYPE)
    transfer_at = models.DateTimeField(auto_now = False)

    def __str__(self):
        return str(self.user.name)

