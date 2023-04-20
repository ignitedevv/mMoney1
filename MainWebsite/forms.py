from django import forms
from budget.models import Account, BudgetUsers

# Account registration for students
class RegistrationForm(forms.ModelForm):
    email = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'text-field w-input', 'id': 'email'}))

    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'class': 'text-field w-input', 'placeholder': '**********'}))
    password2 = forms.CharField(label='Repeat password', required=True, widget=forms.PasswordInput(attrs={'class': 'text-field w-input', 'placeholder': '**********'}))

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'accounts']

class CreateBudgetUserForm(forms.ModelForm):

    class Meta:
        model = BudgetUsers
        fields = ['first_name', 'last_name', 'users_id']