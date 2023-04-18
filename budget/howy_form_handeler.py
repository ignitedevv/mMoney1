from django.shortcuts import render, redirect
import requests
import json
from budget.models import Account
from .forms import AddBudgetForm
import random


def handle_sent_forms(request):
    user = request.user

    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    print(request.POST)
    post = request.POST
    list = post['the_list']
    my_list = json.loads(list)
    handeler_id = my_list[0]
    print(handeler_id)


    if handeler_id == 1:
        form = AddBudgetForm()
        form = form.save(commit=False)
        form.user = user
        form.title = my_list[1]
        form.budget_id = random.randint(100000000, 90000000000)
        form.transactions = {"categoryTransactions": []}
        form.current_total = 0
        form.category = 'Miscellaneous'
        form.total_per_month = my_list[2]
        form.users_id = user_id
        form.save()
        print('the add budget form is saved')



    return render(request, 'MainWebsite/index.html')
