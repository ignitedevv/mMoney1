from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreateBudgetUserForm
import random
import datetime
from django.contrib.auth import login as djlogin

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
            user.set_password(form.cleaned_data['password'])
            print(user.password)
            user.last_login = datetime.datetime.now()
            user.save()
            budgetUserForm = CreateBudgetUserForm(request.POST, request.FILES)
            if budgetUserForm.is_valid():
                budgetUser = budgetUserForm.save(commit=False)
                budgetUser.first_name = 'test'
                budgetUser.save()
            djlogin(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/budget/')

    return render(request, 'MainWebsite/onboarding/register.html')

def pick_plan(request):
    return render(request, 'MainWebsite/onboarding/pick-plan.html')