from .models import BudgetItems
from budget.models import Account
from .models import BudgetUsers
from .functions import savings_calculator, extract_numbers

def action_check(resp, user, request):
    print('user ', user)
    account = Account.objects.filter(pk=request.user.pk)
    user_id = account.model.get_user_id(self=user)
    budget_user = BudgetUsers.objects.get(users_id=user_id)

    if resp == "You now have a new budget":
        qa_id = 1
        message = 'Yes I can build you a budget.'
        packaged_messages = ['What is the title of your budget?', 'What is the budget total?', 'Your budget has been added']
        return [True, message, packaged_messages, qa_id, 'Y']
    # Code for checking to see if they should build a budget and how much they can allocate into a budget
    if resp == 'build budget potential':
        qa_id = 2
        income = budget_user.average_income
        all_budgets = BudgetItems.objects.filter(users_id=user_id)
        total = 0
        for budget in all_budgets:
            total += int(budget.total_per_month)
        if income * .75 > total:
            responce_message = f'Yes you could add a new budget. Your current total monthly income is: {income} and all of your budgets add up tp {total}. '
        else:
            responce_message = f'you currently dont have enough Income for a new Budget. Your current total monthly income is: {income} and all of your budgets add up tp {total}. This would leave you with a surplus of {income - total}'
        message = 'I will check that for you'
        packaged_messages = [f'{responce_message}']
        return [True, message, packaged_messages, qa_id, 'N']

    if resp == "25":
        qa_id = 3
        message = 'Let me check.'
        current_savings = float(input("Enter your current savings: "))
        monthly_income = float(input("Enter your monthly income: "))
        monthly_expenses = float(input("Enter your monthly expenses: "))
        target_amount = 1000

        months_to_reach_goal = savings_calculator(current_savings, monthly_income, monthly_expenses, target_amount)

        if months_to_reach_goal <= 0:
            print("You can already afford a dog!")
        else:
            print(f"It will take approximately {months_to_reach_goal:.1f} months to save for a dog.")

        packaged_messages = ''
        return [True, message, packaged_messages, qa_id, 'Y']

    if resp == 'X in x years':
        qa_id = 4
        message = 'Let me check how many years it will take.'
        numbers = extract_numbers(resp)
        print(numbers)



        packaged_messages = ['I think you can ']
        return [True, message, packaged_messages, qa_id, 'Y']




    else:
        return False, 'test'



