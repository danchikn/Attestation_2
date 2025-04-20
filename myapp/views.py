from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import ExpenseForm, CategoryForm
from .models import Expense, Category
from django.db.models import Sum
from django.http import HttpResponse

import json
import csv
from datetime import datetime, date, timedelta
from django.utils.timezone import now


@login_required
def index(request):
    # Обработка добавления расхода или категории
    if request.method == "POST":
        if 'add_expense' in request.POST:
            form = ExpenseForm(request.POST, user=request.user)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
        elif 'add_category' in request.POST:
            cat_form = CategoryForm(request.POST)
            if cat_form.is_valid():
                category = cat_form.save(commit=False)
                category.user = request.user
                category.save()

    # Все расходы пользователя
    expenses = Expense.objects.filter(user=request.user)
    form = ExpenseForm(user=request.user)
    cat_form = CategoryForm()

    # Фильтрация
    category_filter = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category_filter and category_filter != "all":
        expenses = expenses.filter(category__name=category_filter)
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)

    # Суммы по категориям
    categorical_sums = expenses.values('category__name').annotate(sum=Sum('amount')).order_by('category__name')

    # Суммы за последние 30 дней
    thirty_days_ago = date.today() - timedelta(days=30)
    daily_sums = expenses.filter(date__gt=thirty_days_ago).values('date').annotate(sum=Sum('amount')).order_by('date')

    # Преобразование в JSON
    categorical_sums_json = json.dumps(list(categorical_sums))
    daily_sums_serializable = [{'date': d['date'].strftime('%Y-%m-%d'), 'sum': d['sum']} for d in daily_sums]
    daily_sums_json = json.dumps(daily_sums_serializable)

    # Все категории текущего пользователя
    all_categories = Category.objects.filter(user=request.user).values_list('name', flat=True)

    # Общая сумма
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Сумма за текущий месяц (бонус)
    current_month = now().month
    current_year = now().year
    monthly_total = expenses.filter(
        date__year=current_year,
        date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'myapp/index.html', {
        'expense_form': form,
        'category_form': cat_form,
        'expenses': expenses,
        'categorical_sums_json': categorical_sums_json,
        'daily_sums_json': daily_sums_json,
        'all_categories': all_categories,
        'current_category': category_filter or 'all',
        'current_from': date_from or '',
        'current_to': date_to or '',
        'total_amount': total_amount,
        'monthly_total': monthly_total,
    })


@login_required
def edit(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'myapp/edit.html', {'expense_form': form})


@login_required
def delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect('index')
    return render(request, 'myapp/confirm_delete.html', {'expense': expense})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expenses.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Amount', 'Category', 'Date'])

    for exp in expenses:
        writer.writerow([exp.name, exp.amount, exp.category.name, exp.date])

    return response
