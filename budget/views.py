from django.shortcuts import render, redirect
from .models import Account
from .models import Goal, BudgetItems, BudgetUsers, BankAccount
import environ
import requests
from .forms import UpdateChangedTransactions, AddBudgetForm
import random
from .plaid_integrations import plaid_get_Transactions, plaid_get_account_balance
from .functions import package_transaction
import datetime as dt
from django.shortcuts import render, redirect
from .models import Room

# creating env object
env = environ.Env()
# reading .env file
environ.Env.read_env()

# plaid information
CLIENT_ID = env("CLIENT_ID")
SECRET = env("SECRET")


# add an account
def addAccount(request):
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

    context = {
        'link_token': link_token
    }

    return render(request, 'Budget/add_account.html', context=context)



# Authenticaction for plaid
def oauth(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    if request.POST.get('action') == 'post':
        print('this is accounts test')
        public = request.POST['public_token']

        url = 'https://development.plaid.com/item/public_token/exchange'

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "client_id": f"{CLIENT_ID}",
            "secret": f"{SECRET}",
            "public_token": f"{public}",

        }

        r = requests.post(url, headers=headers, json=data)
        print(r.json())

        access_token = r.json()['access_token']

        print(access_token)

    return render(request, 'Budget/oauth.html')

def refresh(request):
    print('REFRESH')
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    budget_user = BudgetUsers.objects.get(users_id=user_id)

    current_date = dt.date.today()
    start_date = str(current_date).split("-")
    start_date[1] = '01'
    start_date = '-'.join(start_date)

    url = 'https://development.plaid.com/link/token/create'

    headers = {
        'Content-Type': 'application/json'
    }

    CLIENT_ID = '64233564b2767700140073ac'
    SECRET = 'cd964c942048169ce2eb7d73800c82'

    data = {
        "client_id": f"{CLIENT_ID}",
        "secret": f"{SECRET}",
        "client_name": "mMoney",
        "user": {"client_user_id": "123"},
        "country_codes": ["US"],
        "language": "en",
        "webhook": "https://127.0.0.1:8000/budget/dashboard",
        "access_token": "access-development-bcb77a00-4e57-4bd5-8e74-6df3e064a0ab",
        "redirect_uri": "https://127.0.0.1:8000/budget/oauth.html"
    }

    r = requests.post(url, headers=headers, json=data).json()
    print(r)






    # Saving total checking and savings balances
    balances = plaid_get_account_balance(CLIENT_ID, SECRET, 'access-development-bcb77a00-4e57-4bd5-8e74-6df3e064a0ab', start_date, current_date)
    budget_user.checking_savings_total = balances
    budget_user.save()
    print('saved')

    return redirect('/budget/dashboard')


# Create your views here.
def budget_dashboard(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    budget_user = BudgetUsers.objects.get(users_id=user_id)
    checking_and_savings_total = budget_user.checking_savings_total
    credit_avaliable = budget_user.credit_avaliable
    investments = budget_user.investments
    loans = budget_user.loans
    real_estate = budget_user.real_estate
    bank_accounts = BankAccount.objects.filter(users_id=user_id)

    goals = Goal.objects.filter(users_id=user_id)
    current_date = dt.date.today()

    start_date = str(current_date).split("-")
    start_date[1] = '01'
    start_date = '-'.join(start_date)
    print(start_date)



    print(bank_accounts)
    # receiving AJAX from changing a transaction category
    if request.POST.get('action') == 'post':
        public = request.POST
        print(public)

    context = {
        'transaction_data': transactions,
        'checking_and_savings_total': checking_and_savings_total,
        'credit_avaliable': credit_avaliable,
        'investments': investments,
        'loans': loans,
        'real_estate': real_estate
    }


    return render(request, 'Budget/dashboard.html', context=context)

# Goals Page
def goals(request):
    user = request.user
    my_goals = Goal.objects.filter(user=request.user)

    context = {
        'myGoals': my_goals,

    }
    return render(request, 'Budget/Goals/goals.html', context=context)


# Page to add goals
def add_goals(request):
    user = request.user
    return render(request, 'Budget/Goals/add_goal.html')

# View individual goal
def view_goal(request, id):
    user = request.user
    goal = Goal.objects.get(pk=id)
    title = goal.title
    currentAmount = goal.current_amount
    totalAmount = goal.cost
    image = goal.image
    print(image)

    context = {
        'title': title,
        'currentAmount': currentAmount,
        'totalAmount': totalAmount,
        'image': image,

    }

    return render(request, 'Budget/Goals/view_goal.html', context=context)

def transactions(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    budget_categories = BudgetItems.objects.filter(users_id=user_id)
    current_date = dt.date.today()

    start_date = str(current_date).split("-")
    start_date[1] = '01'
    start_date = '-'.join(start_date)
    print(start_date)


    transaction_data = plaid_get_Transactions(CLIENT_ID, SECRET, 'access-development-bcb77a00-4e57-4bd5-8e74-6df3e064a0ab', start_date, current_date)['transactions']

    for transaction in transaction_data:
        print(transaction['transaction_id'])
        for budget in budget_categories:
            print(budget.title)
            for tran in budget.transactions['categoryTransactions']:
                if transaction['transaction_id'] == tran['transaction_id']:
                    transaction['checked'] = 'true'
                    transaction['associated_budget'] = f'{budget.title}'

                    print(transaction)
                    pass






    print(current_date)
    if request.POST.get('action') == 'post':
        print('transaction coming in ')
        print(request.POST)
        public = request.POST
        transaction_id = public['the_id']
        amount = public['amount'].partition('$')[2]
        tran_title = public['tran_title']
        transaction_date = public['transaction_date']
        print(transaction_date)

        amount = float(amount)
        category1 = public['category1']
        category2 = public['category2']
        transaction_budget = public['budget']

        new_packaged_transaction = package_transaction(tran_title, transaction_budget, amount, category1, category2,
                                                       transaction_id)

        print(transaction_budget)

        # Specific budget category
        budget_category = BudgetItems.objects.get(budget_id=transaction_budget, users_id=user_id)
        print('budget category: ', budget_category.title)

        all_budgets = BudgetItems.objects.filter(users_id=user_id)
        for budg in all_budgets:
            category_transactions = budg.transactions['categoryTransactions']
            # Checking to see if the transaction has been in any budgets
            if (transaction_budget == budg.budget_id):
                category_transactions.append(new_packaged_transaction)
                budget_category.transactions['categoryTransactions'] = category_transactions
                budget_category.current_total = budget_category.current_total + amount
                budget_category.save()
                print('its saved')




    context = {
        'budget_categories': budget_categories,
        'transaction_data': transaction_data
    }

    return render(request, 'Budget/transactions.html', context=context)

# budget page
def budget(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    all_budgets = BudgetItems.objects.filter(users_id=user_id)
    budget_user = BudgetUsers.objects.get(users_id=user_id)

    average_income = budget_user.average_income
    print(all_budgets)

    context = {
        'all_budgets': all_budgets,
        'average_income': average_income,
    }
    return render(request, 'Budget/budget.html', context=context)

# Page for adding budget
def add_budget(request):
    user = request.user
    student_user = Account.objects.filter(pk=request.user.pk)
    user_id = student_user.model.get_user_id(self=user)
    if request.method == 'POST':
        form = AddBudgetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.transactions = {"categoryTransactions": []}
            instance.budget_id = random.randint(100000000, 90000000000)
            instance.users_id = user_id
            instance.current_total = 0
            instance.save()
            return redirect('/budget/dashboard')
    else:
        form = AddBudgetForm(request.POST)

    context = {
        'form': form
    }
    return render(request, 'Budget/add_budget.html', context=context)

# Page for viewing budget
def view_budget(request, id):
    user = request.user
    student_user = Account.objects.filter(pk=request.user.pk)
    student_budget = BudgetItems.objects.get(budget_id=id)
    budget_categories = student_budget.CATAGORIES

    budget_purchases = student_budget.transactions

    if request.method == 'POST':
        post = request.POST
        print(request.POST)
        budget_name = post['budget-title']
        budget_max = post['Max-amount']
        budget_category = post['Category']
        print('changed budget')

        for categories in budget_categories:
            if categories[0] == budget_category:
                num = categories[0]

        student_budget.title = budget_name
        student_budget.total_per_month = budget_max
        student_budget.category = num
        student_budget.save()

        return redirect('/budget/budget')

    context = {
        'student_budget': student_budget,
        'budget_categories': budget_categories,
        'budget_purchases': budget_purchases
    }
    return render(request, 'Budget/view_budget.html', context=context)

# Page for deleting budget
def delete_budget(request, id):
    user = request.user
    student_budget = BudgetItems.objects.get(budget_id=id)
    student_budget.delete()
    return redirect('/budget/budget')

# accounts page
def accounts(request):
    user = request.user

# notifications page
def notifications(request):
    user = request.user
    return render(request, 'Budget/notifications.html')






def index(request):
    rooms = Room.objects.all()
    return render(request, 'Budget/chat/index.html', {'rooms': rooms})

def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        Room.objects.create(name=room_name)
        return redirect('Budget:index')
    return render(request, 'Budget/chat/create_room.html')

def join_room(request, room_name):
    room = Room.objects.get(name=room_name)
    return render(request, 'Budget/chat/room.html', {'room': room})

