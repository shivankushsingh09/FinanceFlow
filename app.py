from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import os
from sqlalchemy import extract
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.title}>'

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Budget {self.category} - {self.month}/{self.year}>'
    
    @property
    def month_year(self):
        return f"{self.month:02d}/{self.year}"

class RecurringExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly, yearly
    next_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RecurringExpense {self.title} - {self.frequency}>'

@app.route('/')
def index():
    # Get filter parameters
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = Expense.query
    
    # Apply filters
    if search:
        query = query.filter(Expense.title.contains(search) | Expense.description.contains(search))
    
    if category_filter:
        query = query.filter(Expense.category == category_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= date_to_obj)
        except ValueError:
            pass
    
    expenses = query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    categories = db.session.query(Expense.category, db.func.sum(Expense.amount).label('total')).group_by(Expense.category).all()
    
    # Get all unique categories for filter dropdown
    all_categories = db.session.query(Expense.category).distinct().all()
    all_categories = [cat[0] for cat in all_categories]
    
    return render_template('index.html', 
                         expenses=expenses, 
                         total_amount=total_amount, 
                         categories=categories,
                         all_categories=all_categories,
                         search=search,
                         category_filter=category_filter,
                         date_from=date_from,
                         date_to=date_to)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form.get('title')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        expense_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        description = request.form.get('description')
        
        expense = Expense(
            title=title,
            amount=amount,
            category=category,
            date=expense_date,
            description=description
        )
        
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_expense.html')

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if request.method == 'POST':
        expense.title = request.form.get('title')
        expense.amount = float(request.form.get('amount'))
        expense.category = request.form.get('category')
        expense.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        expense.description = request.form.get('description')
        
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/analytics')
def analytics():
    expenses = Expense.query.all()
    
    # Monthly expenses
    monthly_data = {}
    for expense in expenses:
        month_key = expense.date.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = 0
        monthly_data[month_key] += expense.amount
    
    # Category breakdown
    category_data = {}
    for expense in expenses:
        if expense.category not in category_data:
            category_data[expense.category] = 0
        category_data[expense.category] += expense.amount
    
    # Get current month budgets and spending
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    budgets = Budget.query.filter_by(month=current_month, year=current_year).all()
    budget_status = []
    
    for budget in budgets:
        # Calculate spending for this category in current month
        category_spending = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.category == budget.category,
            db.extract('month', Expense.date) == current_month,
            db.extract('year', Expense.date) == current_year
        ).scalar() or 0.0
        
        remaining = budget.amount - category_spending
        percentage_used = (category_spending / budget.amount * 100) if budget.amount > 0 else 0
        
        budget_status.append({
            'category': budget.category,
            'budget': budget.amount,
            'spent': category_spending,
            'remaining': remaining,
            'percentage_used': percentage_used,
            'status': 'danger' if percentage_used > 100 else 'warning' if percentage_used > 80 else 'success'
        })
    
    return render_template('analytics.html', 
                         monthly_data=monthly_data, 
                         category_data=category_data,
                         expenses=expenses,
                         budget_status=budget_status)

@app.route('/budgets', methods=['GET', 'POST'])
def budgets():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        
        # Check if budget already exists for this category and month
        existing_budget = Budget.query.filter_by(category=category, month=month, year=year).first()
        if existing_budget:
            existing_budget.amount = amount
            flash('Budget updated successfully!', 'success')
        else:
            budget = Budget(category=category, amount=amount, month=month, year=year)
            db.session.add(budget)
            flash('Budget added successfully!', 'success')
        
        db.session.commit()
        return redirect(url_for('budgets'))
    
    # Get all budgets
    budgets = Budget.query.order_by(Budget.year.desc(), Budget.month.desc()).all()
    
    # Get current month/year for form defaults
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    return render_template('budgets.html', budgets=budgets, current_month=current_month, current_year=current_year)

@app.route('/delete_budget/<int:id>', methods=['POST'])
def delete_budget(id):
    budget = Budget.query.get_or_404(id)
    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/export')
def export_expenses():
    # Get filter parameters (same as index)
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = Expense.query
    
    # Apply filters
    if search:
        query = query.filter(Expense.title.contains(search) | Expense.description.contains(search))
    
    if category_filter:
        query = query.filter(Expense.category == category_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= date_to_obj)
        except ValueError:
            pass
    
    expenses = query.order_by(Expense.date.desc()).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Title', 'Amount', 'Category', 'Date', 'Description', 'Created At'])
    
    # Data
    for expense in expenses:
        writer.writerow([
            expense.title,
            expense.amount,
            expense.category,
            expense.date.strftime('%Y-%m-%d'),
            expense.description or '',
            expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=expenses_export.csv'
    response.headers['Content-type'] = 'text/csv'
    
    return response

@app.route('/recurring_expenses', methods=['GET', 'POST'])
def recurring_expenses():
    if request.method == 'POST':
        title = request.form.get('title')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        frequency = request.form.get('frequency')
        next_date = datetime.strptime(request.form.get('next_date'), '%Y-%m-%d').date()
        description = request.form.get('description')
        
        recurring = RecurringExpense(
            title=title,
            amount=amount,
            category=category,
            frequency=frequency,
            next_date=next_date,
            description=description
        )
        
        db.session.add(recurring)
        db.session.commit()
        flash('Recurring expense added successfully!', 'success')
        return redirect(url_for('recurring_expenses'))
    
    recurring_expenses = RecurringExpense.query.filter_by(is_active=True).order_by(RecurringExpense.next_date).all()
    return render_template('recurring_expenses.html', recurring_expenses=recurring_expenses)

@app.route('/process_recurring_expenses')
def process_recurring_expenses():
    today = date.today()
    processed_count = 0
    
    recurring_expenses = RecurringExpense.query.filter_by(is_active=True).filter(RecurringExpense.next_date <= today).all()
    
    for recurring in recurring_expenses:
        # Create expense from recurring expense
        expense = Expense(
            title=recurring.title,
            amount=recurring.amount,
            category=recurring.category,
            date=recurring.next_date,
            description=f"[Recurring] {recurring.description or ''}"
        )
        
        db.session.add(expense)
        
        # Update next date based on frequency
        if recurring.frequency == 'daily':
            recurring.next_date = recurring.next_date + timedelta(days=1)
        elif recurring.frequency == 'weekly':
            recurring.next_date = recurring.next_date + timedelta(weeks=1)
        elif recurring.frequency == 'monthly':
            recurring.next_date = recurring.next_date + timedelta(days=30)
        elif recurring.frequency == 'yearly':
            recurring.next_date = recurring.next_date + timedelta(days=365)
        
        processed_count += 1
    
    db.session.commit()
    flash(f'Processed {processed_count} recurring expenses!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_recurring_expense/<int:id>', methods=['POST'])
def delete_recurring_expense(id):
    recurring = RecurringExpense.query.get_or_404(id)
    recurring.is_active = False
    db.session.commit()
    flash('Recurring expense deactivated!', 'success')
    return redirect(url_for('recurring_expenses'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
