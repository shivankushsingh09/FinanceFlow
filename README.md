# FinanceFlow

A modern web-based expense tracking application built with Flask that helps you manage your personal finances with powerful features and intuitive design.

## Features

- Add, edit, and delete expenses
- Categorize expenses (Food, Transport, Shopping, Entertainment, Bills, Healthcare, Education, Other)
- View expense history with filtering options
- Analytics dashboard with charts
- Monthly expense trends
- Category-wise expense breakdown
- Responsive design for mobile and desktop

## Installation

1. Install Python 3.7 or higher
2. Clone or download this project
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Navigate to the project directory
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://localhost:5000`

## Usage

1. **Add Expense**: Click "Add Expense" to record a new expense with title, amount, category, date, and description
2. **View Expenses**: See all your expenses on the dashboard with total amount and category breakdown
3. **Edit/Delete**: Use the action buttons to modify or remove expenses
4. **Analytics**: View charts and statistics about your spending patterns

## Project Structure

```
FinanceFlow/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── USER_GUIDE.md         # Comprehensive user guide
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard
│   ├── add_expense.html  # Add expense form
│   ├── edit_expense.html # Edit expense form
│   ├── analytics.html    # Analytics dashboard
│   ├── budgets.html      # Budget management
│   └── recurring_expenses.html # Recurring expenses
├── static/
│   └── css/
│       └── style.css     # Custom styles
└── expenses.db          # SQLite database (created automatically)
```

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript, Chart.js
- **Database**: SQLite
- **Styling**: Custom CSS with Bootstrap

## Database Schema

The application uses a single `Expense` model with the following fields:
- `id`: Primary key
- `title`: Expense title (required)
- `amount`: Expense amount (required)
- `category`: Expense category (required)
- `date`: Expense date (required)
- `description`: Optional description
- `created_at`: Timestamp when expense was created
