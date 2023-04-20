from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreateBudgetUserForm
import random
import datetime as dt
from django.contrib.auth import login as djlogin
from budget.models import Account
import environ
import requests
from budget.plaid_integrations import plaid_get_checking_account_balance, plaid_get_accounts, plaid_get_Transactions
from budget.plaid_integrations import plaid_get_Transactions

# creating env object
env = environ.Env()
# reading .env file
environ.Env.read_env()

# plaid information
CLIENT_ID = env("CLIENT_ID")
SECRET = env("SECRET")


# Create your views here.
def home_page(request):
    return render(request, 'MainWebsite/index.html')

# Create your views here.
def about_us(request):
    return render(request, 'MainWebsite/about.html')

# Register Page
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            created_user_id = random.randint(100000000000, 999999990000)
            user.user_id = created_user_id
            user.username = created_user_id
            user.accounts = {"accounts": []}
            user.set_password(form.cleaned_data['password'])
            print(user.password)
            user.last_login = dt.datetime.now()
            user.save()
            budgetUserForm = CreateBudgetUserForm(request.POST, request.FILES)
            if budgetUserForm.is_valid():
                budgetUser = budgetUserForm.save(commit=False)
                budgetUser.first_name = 'test'
                budgetUser.save()
            djlogin(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/budget/')

    return render(request, 'MainWebsite/onboarding/register.html')


# Page where users pick their plan
def pick_plan(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)





    return render(request, 'MainWebsite/onboarding/pick-plan.html')


# Page for onboarding for free account
def onboarding_free(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)

    url = 'https://development.plaid.com/link/token/create'

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "client_id": f"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "client_name": "mMoney",
        "user": {"client_user_id": f"{user_id}"},
        "products": ["auth"],
        "country_codes": ["US"],
        "language": "en",
        "webhook": "https://127.0.0.1:8000/budget/dashboard",
        "redirect_uri": "https://127.0.0.1:8000/budget/oauth.html"
    }

    link_token = requests.post(url, headers=headers, json=data).json()['link_token']
    print(link_token)


    # Account information handling
    accounts = Account.objects.get(user_id=user_id).accounts['accounts']
    print(accounts)
    if accounts == []:
        print('there isnt an account')
    else:
        print('there is an account')
        account_list = []
        for account in accounts:
            print(account['access_token'])

    current_date = dt.date.today()
    start_date = str(current_date).split("-")
    start_date[1] = '01'
    start_date = '-'.join(start_date)
    balances = plaid_get_Transactions(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    packaged_accounts = []
    for account in balances['accounts']:
        name = account['name']
        mask = account['mask']
        account_id = account['account_id']

        packaged_acc = {'name': name, 'mask': mask, 'account_id': account_id}
        packaged_accounts.append(packaged_acc)


    context = {
        'link_token': link_token,
        'packaged_accounts': packaged_accounts
    }

    return render(request, 'MainWebsite/onboarding/onboarding-free.html', context=context)



def welcome_video(request):
    return render(request, 'MainWebsite/onboarding/welcome-video.html')