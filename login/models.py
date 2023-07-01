from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    has_account = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.account_number

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    receiver_account_number = models.CharField(max_length=20, default=None, null=True)

    def __str__(self):
        return f"Transaction {self.transaction_id}"

# class Beneficiary(models.Model):
#     beneficiary_id = models.AutoField(primary_key=True)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     beneficiary_account_number = models.CharField(max_length=20)
#     beneficiary_name = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.beneficiary_name

# class Loan(models.Model):
#     loan_id = models.AutoField(primary_key=True)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
#     loan_status = models.CharField(max_length=100)
#     repayment_period = models.CharField(max_length=100)
    
#     def __str__(self):
#         return f"Loan {self.loan_id}"
