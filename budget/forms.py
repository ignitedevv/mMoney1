from django import forms
from .models import Goal, MonthlySummary, BudgetItems

# Form for adding goals
class AddGoalForm(forms.ModelForm):

    class Meta:
        model = Goal
        fields = ['title', 'user', 'cost']

# Form for updating changed transactions
class UpdateChangedTransactions(forms.ModelForm):

    class Meta:
        model = MonthlySummary
        fields = ['account_transactions']

# Form for adding budgets
class AddBudgetForm(forms.ModelForm):

    class Meta:
        model = BudgetItems
        fields = ['user', 'title', 'category', 'total_per_month', 'users_id']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input budget w-input', 'placeholder': 'Title'}),
            'total_per_month': forms.TextInput(attrs={'class': 'input budget w-input', 'placeholder': 'Total Per Month'}),
            'category': forms.Select(choices=BudgetItems.CATAGORIES, attrs={'class': 'input budget w-input', 'name': 'Total Per Month', 'data-name': 'Category'})

        }

# Form for howy
class MyForm(forms.Form):
    input_field = forms.CharField(max_length=100)

    fields = ['input_field']
    widgets = {
        'input_field': forms.TextInput(attrs={'id': 'form-input', 'style': 'display:none;'}),
    }