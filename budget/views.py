from django.shortcuts import render, redirect
from .models import Account
from .models import Goal, BudgetItems, BudgetUsers, BankAccount
import environ
import requests
from .forms import UpdateChangedTransactions, AddBudgetForm
import random
from .plaid_integrations import plaid_get_Transactions, plaid_get_checking_account_balance, get_checking_accounts, plaid_get_accounts, plaid_get_rec_payments, plaid_updpate, get_savings_accounts, plaid_get_savings_account_balance
from .plaid_integrations import get_investment_account_balances, plaid_get_investment_accounts
from .functions import package_transaction, add_month, days_to_date
import datetime as dt
from django.shortcuts import render, redirect
from .models import Room
import calendar

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
        "products": ["auth", "investments"],
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


# Recouring payments page
def rec_payments_all(request):
    # Collecting dates
    current_date = dt.date.today()
    start_date = str(current_date).split("-")
    start_date[1] = '01'
    start_date = '-'.join(start_date)

    year = current_date.year



    month = current_date.month
    current_month = calendar.monthrange(year, month)[1]
    print(current_month)
    print(current_date)

    # This month
    month = current_date.month - 1
    last_month = calendar.monthrange(year, month)[1]
    print(last_month)


    date_str = f'2023-{month}-{last_month}'
    date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    day = date_obj.strftime('%A')
    print(day)

    accounts = plaid_get_accounts(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    reccPayments = plaid_get_rec_payments(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', accounts)[
        'outflow_streams']
    sorted_recc_data = sorted(reccPayments, key=lambda x: dt.datetime.strptime(x['first_date'], '%Y-%m-%d'))

    for data in sorted_recc_data:
        print(data['is_active'])
        if data['is_active'] == True:
            first_date = data['first_date']
            last_date = data['last_date']
            date_str = add_month(f"{last_date}")
            days_remaining = days_to_date(date_str)
            data['numdays'] = days_remaining



    context = {
        'sorted_recc_data': sorted_recc_data,
        'day_of_week': day,
        'last_month_lastday': last_month,
        'current_date_lastday': current_month

    }

    return render(request, 'Budget/upcoming payments/all_upcoming_payments.html', context=context)




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

        accounts = Account.objects.get(user_id=user_id)
        accounts.accounts['accounts'].append(r.json())
        accounts.save()


        print(access_token)

    return render(request, 'Budget/oauth.html')








# For updating link token
def update_plaid(request):
    link_token = (plaid_updpate(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', '123'))

    context = {
        'link_token': link_token
    }

    return render(request, 'Budget/token_update.html', context=context)


# Refreshing data
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



    # Saving total checking and savings balances
    balances = plaid_get_checking_account_balance(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    savings_accounts = get_savings_accounts(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    investment_accounts = get_investment_account_balances(CLIENT_ID, SECRET, 'access-development-6e0f7b45-e3e5-4a64-89b3-c5bf14be3d5b')



    # For handling to see if there are savings accounts
    if savings_accounts == []:
        budget_user.savings_total = 0.0
        budget_user.save()
    else:
        budget_user.savings_total = plaid_get_savings_account_balance(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)

    # for handeling to see if there are investment accounts
    if investment_accounts == []:
        budget_user.investments = 0.0
        budget_user.save()
    else:
        budget_user.investments = get_investment_account_balances(CLIENT_ID, SECRET, 'access-development-6e0f7b45-e3e5-4a64-89b3-c5bf14be3d5b')
        budget_user.save()


    budget_user.checking_savings_total = balances
    budget_user.save()
    print('saved')

    # Code for getting reacurring payments
    accounts = plaid_get_accounts(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55',
                                  start_date, current_date)
    reccPayments = plaid_get_rec_payments(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', accounts)
    print(reccPayments['inflow_streams'])
    total_income = 0.0
    for i in reccPayments['inflow_streams']:
        if i['is_active'] == True:
            print(i['average_amount']['amount'])
            total_income += float(i['average_amount']['amount'])
    budget_user.average_income = total_income
    budget_user.save()







    return redirect('/budget/dashboard')


# Create your views here.
def budget_dashboard(request):
    user = request.user
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    budget_user = BudgetUsers.objects.get(users_id=user_id)
    checking_and_savings_total = budget_user.checking_savings_total
    savings_total = budget_user.savings_total
    credit_avaliable = budget_user.credit_avaliable
    investments = budget_user.investments
    loans = budget_user.loans
    real_estate = budget_user.real_estate
    bank_accounts = BankAccount.objects.filter(users_id=user_id)
    goals = Goal.objects.filter(users_id=user_id)
    budgets = BudgetItems.objects.filter(users_id=user_id)




    # Collecting dates
    current_date = dt.date.today()
    start_date = str(current_date).split("-")
    start_date[1] = '01'
    start_date = '-'.join(start_date)
    print(start_date)


    # receiving AJAX from changing a transaction category
    if request.POST.get('action') == 'post':
        public = request.POST
        print(public)



    # Code to get packaged checking / savings accounts
    checking_accounts = get_checking_accounts(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    savings_accounts = get_savings_accounts(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    investment_accounts = plaid_get_investment_accounts(CLIENT_ID, SECRET, 'access-development-6e0f7b45-e3e5-4a64-89b3-c5bf14be3d5b')

    # Code for getting reacurring payments
    accounts = plaid_get_accounts(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)
    reccPayments = plaid_get_rec_payments(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', accounts)['outflow_streams']
    sorted_recc_data = sorted(reccPayments, key=lambda x: dt.datetime.strptime(x['first_date'], '%Y-%m-%d'))
    for data in sorted_recc_data:
        print(data['is_active'])
        if data['is_active'] == True:
            first_date = data['first_date']
            last_date = data['last_date']
            date_str = add_month(f"{last_date}")
            days_remaining = days_to_date(date_str)
            print(f"It will take {days_remaining} days to get to {date_str}.")
            data['numdays'] = days_remaining
            print(data)


    context = {
        'checking_accounts': checking_accounts,
        'savings_accounts': savings_accounts,
        'savings_total': savings_total,
        'checking_and_savings_total': checking_and_savings_total,
        'credit_avaliable': credit_avaliable,
        'investment_accounts': investment_accounts,
        'investments': investments,
        'loans': loans,
        'real_estate': real_estate,
        'sorted_recc_data': sorted_recc_data,
        'goals': goals,
        'budgets': budgets

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


    transaction_data = plaid_get_Transactions(CLIENT_ID, SECRET, 'access-development-24934c76-5453-4288-912c-6ae4ab74cd55', start_date, current_date)['transactions']

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
    return render(request, 'chat/index.html')