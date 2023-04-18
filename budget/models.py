from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings



# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('users must have an email')
        if not username:
            raise ValueError('users must have a usernanme')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Account(AbstractBaseUser):
    # Basic Setup Information
    email = models.EmailField(verbose_name='email', max_length=30, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


    # all other information
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name


    user_id = models.CharField(max_length=12, null=True, blank=True)

    def get_user_id(self):
        return self.user_id








# Budget Users
class BudgetUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    users_id = models.CharField(max_length=100, null=True, blank=True)
    networth_timeline = models.JSONField(null=True, blank=True)
    checking_savings_total = models.FloatField(null=True, blank=True)
    credit_avaliable = models.FloatField(null=True, blank=True)
    investments = models.FloatField(null=True, blank=True)
    loans = models.FloatField(null=True, blank=True)
    real_estate = models.FloatField(null=True, blank=True)

    average_income = models.FloatField(null=True, blank=True)


# Goals
class Goal(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='goalImages/')
    current_amount = models.IntegerField(null=True, blank=True)
    users_id = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)

    CATAGORIES = [
        ('Food and Drink', 'Food and Drink'),
        ('Transportation', 'Transportation'),
        ('Shops', 'Shops'),
        ('Transfer', 'Transfer'),
        ('Service', 'Service'),
        ('Payment', 'Payment'),
        ('Income', 'Income'),

    ]
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATAGORIES)





class BudgetItems(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    budget_id = models.CharField(max_length=100, null=True, blank=True)
    CATAGORIES = [
        ('Food and Drink', 'Food and Drink'),
        ('Transportation', 'Transportation'),
        ('Shops', 'Shops'),
        ('Transfer', 'Transfer'),
        ('Service', 'Service'),
        ('Payment', 'Payment'),
        ('Income', 'Income'),
        ('Subscription', 'Subscription'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=200, null=True, blank=True, choices=CATAGORIES)
    total_per_month = models.IntegerField(null=True, blank=True)
    current_total = models.FloatField(null=True, blank=True)
    users_id = models.CharField(max_length=100, null=True, blank=True)
    transactions = models.JSONField(null=True, blank=True)



class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    users_id = models.CharField(max_length=100, null=True, blank=True)




class MonthlySummary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    account_transactions = models.JSONField(null=True, blank=True)
    all_transactions = models.JSONField(null=True, blank=True)
    users_id = models.CharField(max_length=100, null=True, blank=True)

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name