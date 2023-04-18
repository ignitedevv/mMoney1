from .forms import AddBudgetForm
import random
from budget.models import Account
from django.shortcuts import render, redirect


def create_budget(request):
    user = request.user
    if user.is_active and user.has_budget == True:
        student_user = Account.objects.filter(pk=request.user.pk)
        user_id = student_user.model.get_user_id(self=user)
        monthly_income = int(5000)

        categories = [
            ['Food and Dining', 'Food and Drink'],
            ['Transportation', 'Transportation'],
            ['Shops', 'Shops'],
            ['Housing', 'Payment'],
            ['Entertainment', 'Payment'],
            ['Subscriptions', 'Subscription'],
            ['Miscellaneous', 'Miscellaneous'],
        ]

        index = 0
        while index < len(categories):
            form = AddBudgetForm()
            form = form.save(commit=False)
            form.user = user
            form.title = categories[index][0]
            form.budget_id = random.randint(100000000, 90000000000)
            form.category = categories[index][1]
            form.transactions = {"categoryTransactions": []}
            number = monthly_income / len(categories)
            form.current_total = 0
            form.total_per_month = number
            form.users_id = user_id
            form.save()
            index += 1

        return redirect('/budget/budget')
    else:
        return render(request, 'MainWebsite/index.html')

def add_budget():
    pass


def package_transaction(tran_title, transaction_category, amount, category1, category2, transaction_id):
    new_packaged_transaction = {
        "date": "2017-01-29",
        "name": f"{tran_title}",
        "associated_budget": f"{transaction_category}",
        "amount": amount,
        "checked": "yes",
        "category": [
            f"{category1}",
            f"{category2}"
        ],
        "location": {
            "lat": 40.740352,
            "lon": -74.001761,
            "city": "San Francisco",
            "region": "CA",
            "address": "300 Post St",
            "country": "US",
            "postal_code": "94108",
            "store_number": "1235"
        },
        "transaction_id": f"{transaction_id}",
        "category_id": "19013000",

    }

    return new_packaged_transaction


def savings_calculator(current_savings, monthly_income, monthly_expenses, target_amount):
    net_monthly_savings = monthly_income - monthly_expenses
    months_to_reach_goal = (target_amount - current_savings) / net_monthly_savings
    return months_to_reach_goal

def extract_numbers(s):
    return ''.join([char for char in s if char.isdigit()])