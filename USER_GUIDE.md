# 📚 FinanceFlow User Guide

## 🚀 Getting Started

### Installation
1. Make sure you have Python 3.7+ installed
2. Navigate to the project directory
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`
5. Open your browser and go to `http://localhost:5000`

### First Time Setup
- The database will be created automatically
- You can start adding expenses immediately
- No registration or login required

---

## 📋 Features Overview

### 1. **Dashboard (Home)**
- View all your expenses at a glance
- See total spending amount
- Filter and search expenses
- Export data to CSV

### 2. **Add Expenses**
- Record new expenses with details
- Categorize your spending
- Add descriptions for context
- Set custom dates

### 3. **Recurring Expenses**
- Set up automatic recurring payments
- Support for daily, weekly, monthly, yearly
- Process due expenses automatically
- Never miss regular payments

### 4. **Budget Management**
- Set monthly budgets by category
- Track spending vs. budget
- Visual progress indicators
- Alerts when approaching limits

### 5. **Analytics & Reports**
- Monthly expense trends
- Category-wise breakdown
- Budget status overview
- Visual charts and insights

---

## 📖 Step-by-Step Guide

### Adding Your First Expense

1. **Navigate to Add Expense**
   - Click "Add Expense" in the navigation menu
   - Or click the "Add New" button on the dashboard

2. **Fill in Expense Details**
   ```
   Title: Coffee at Starbucks
   Amount: 350.00
   Category: Food
   Date: Today's date (auto-filled)
   Description: Morning coffee with colleagues
   ```

3. **Save the Expense**
   - Click "Add Expense" button
   - You'll see a success message
   - The expense appears on your dashboard

### Setting Up Budgets

1. **Go to Budgets Page**
   - Click "Budgets" in navigation

2. **Create a Budget**
   ```
   Category: Food
   Budget Amount: 5000.00
   Month: Current month
   Year: Current year
   ```

3. **Track Your Budget**
   - View budget status on Analytics page
   - Green = Under budget
   - Yellow = 80-100% used
   - Red = Over budget

### Creating Recurring Expenses

1. **Access Recurring Expenses**
   - Click "Recurring" in navigation

2. **Set Up Recurring Payment**
   ```
   Title: Monthly Rent
   Amount: 15000.00
   Category: Bills
   Frequency: Monthly
   Next Date: 1st of next month
   Description: Apartment rent payment
   ```

3. **Process Due Expenses**
   - Click "Process Due Expenses" button
   - System creates expenses for all due items
   - Updates next occurrence dates

### Filtering and Searching

1. **Use the Filter Panel**
   - Search by title/description
   - Filter by category
   - Set date ranges
   - Click "Filter" to apply

2. **Export Filtered Data**
   - Apply your filters first
   - Click "Export" button
   - Download CSV file with filtered results

---

## 💡 Pro Tips

### Budget Management
- **Start with realistic budgets** based on your spending history
- **Review monthly** to adjust budgets as needed
- **Use the 80% rule** - aim to stay under 80% of your budget

### Expense Tracking
- **Be consistent** - record expenses as soon as possible
- **Use detailed descriptions** for better categorization
- **Categorize properly** for accurate analytics

### Recurring Expenses
- **Set up all regular bills** (rent, utilities, subscriptions)
- **Process weekly** to avoid missing payments
- **Review quarterly** to update amounts if needed

### Analytics Usage
- **Check monthly** to identify spending patterns
- **Look for trends** in category spending
- **Use insights** to adjust budgets and habits

---

## 🎯 Common Use Cases

### Monthly Budget Planning
1. Review last month's spending in Analytics
2. Set realistic budgets for each category
3. Track progress throughout the month
4. Adjust habits based on budget status

### Bill Management
1. Add all recurring bills to Recurring Expenses
2. Process due expenses at the start of each month
3. Monitor budget impact in Analytics
4. Never miss a payment deadline

### Spending Analysis
1. Export data monthly for detailed analysis
2. Use filters to examine specific categories
3. Identify areas where you can cut costs
4. Track progress toward financial goals

---

## 🛠️ Advanced Features

### CSV Export
- **Full data export**: All expense details with timestamps
- **Filtered export**: Only the data you're currently viewing
- **Compatible with Excel**: Open directly in spreadsheet software

### Date Range Analysis
- **Custom periods**: Filter any date range you need
- **Monthly comparisons**: Compare spending across months
- **Trend identification**: Spot spending patterns over time

### Category Management
- **Pre-defined categories**: Food, Transport, Shopping, etc.
- **Flexible usage**: Add detailed descriptions for sub-categories
- **Analytics integration**: Categories drive all reporting

---

## 🔧 Troubleshooting

### Common Issues

**Q: Budget status isn't updating**
- A: Make sure you've set budgets for the current month
- A: Check that expenses have the correct dates

**Q: Recurring expenses not showing**
- A: Ensure the "next date" is today or in the past
- A: Click "Process Due Expenses" to create the actual expenses

**Q: Export not working**
- A: Make sure you have expenses to export
- A: Try clearing filters and exporting all data

**Q: Charts not displaying**
- A: Check browser console for errors
- A: Ensure you have expenses with data to display

### Data Management

**Backup Your Data**
- Regularly export CSV files
- Save the `expenses.db` file
- Keep copies of important financial records

**Reset Application**
- Delete `expenses.db` file to start fresh
- All data will be lost - export first!
- Application will recreate database on next run

---

## 📱 Mobile Usage

### Browser Compatibility
- Works on all modern browsers
- Mobile-responsive design
- Touch-friendly interface

### Mobile Tips
- **Bookmark the page** for quick access
- **Use landscape mode** for better chart viewing
- **Export data** for offline analysis

---

## 🎉 Best Practices

### Daily Habits
1. **Record expenses immediately** after purchase
2. **Check budget status** weekly
3. **Process recurring expenses** monthly
4. **Review analytics** at month-end

### Monthly Routine
1. **Export last month's data**
2. **Review spending patterns**
3. **Adjust budgets** if needed
4. **Set up new recurring expenses**

### Financial Planning
1. **Use analytics** to identify saving opportunities
2. **Set realistic budgets** based on history
3. **Track progress** toward financial goals
4. **Maintain consistent records** for accurate insights

---

## 🆘 Need Help?

### Quick Reference
- **Add Expense**: Navigation → Add Expense
- **View Budgets**: Navigation → Budgets  
- **Set Recurring**: Navigation → Recurring
- **See Analytics**: Navigation → Analytics
- **Export Data**: Dashboard → Export button

### Support
- Check this guide first for common issues
- Review the troubleshooting section
- All features work offline once loaded

---

## 🎉 Congratulations!

You now have **FinanceFlow** - a powerful expense tracking system that helps you:
- ✅ Track every expense effortlessly
- ✅ Stay within budget limits
- ✅ Automate recurring payments
- ✅ Analyze spending patterns
- ✅ Export data for further analysis

Happy tracking! 🚀
