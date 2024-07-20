import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import csv

class ExpenseSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Sharing App")
        self.root.configure(bg='#ffffff')

        # Center the window on the screen
        window_width = 600
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        self.expenses = []

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg='#ffffff')
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Expense input frame
        input_frame = tk.LabelFrame(main_frame, text="Add New Expense", padx=10, pady=10, bg='#f5f5f5', font=('Arial', 12, 'bold'))
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(input_frame, text="Expense Description:", bg='#f5f5f5').grid(row=0, column=0, sticky="e")
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(input_frame, text="Amount:", bg='#f5f5f5').grid(row=1, column=0, sticky="e")
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(input_frame, text="Paid By:", bg='#f5f5f5').grid(row=2, column=0, sticky="e")
        self.paid_by_entry = tk.Entry(input_frame)
        self.paid_by_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(input_frame, text="Shared With (comma-separated):", bg='#f5f5f5').grid(row=3, column=0, sticky="e")
        self.shared_with_entry = tk.Entry(input_frame)
        self.shared_with_entry.grid(row=3, column=1, sticky="ew")

        tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg='#f5f5f5').grid(row=4, column=0, sticky="e")
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=4, column=1, sticky="ew")

        tk.Label(input_frame, text="Category:", bg='#f5f5f5').grid(row=5, column=0, sticky="e")
        self.category_entry = tk.Entry(input_frame)
        self.category_entry.grid(row=5, column=1, sticky="ew")

        tk.Button(input_frame, text="Add Expense", command=self.add_expense, bg='#4CAF50', fg='white').grid(row=6, column=0, columnspan=2, pady=5)

        # Expense list frame
        expense_list_frame = tk.LabelFrame(main_frame, text="Expenses", padx=10, pady=10, bg='#f5f5f5', font=('Arial', 12, 'bold'))
        expense_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.expenses_listbox = tk.Listbox(expense_list_frame, selectmode=tk.SINGLE)
        self.expenses_listbox.grid(row=0, column=0, sticky="nsew")
        self.expenses_listbox.bind('<Delete>', self.remove_expense)

        expense_buttons_frame = tk.Frame(expense_list_frame, bg='#f5f5f5')
        expense_buttons_frame.grid(row=1, column=0, pady=5, sticky="ew")

        tk.Button(expense_buttons_frame, text="Remove Selected", command=self.remove_expense, bg='#f44336', fg='white').grid(row=0, column=0, padx=5)
        tk.Button(expense_buttons_frame, text="Edit Selected", command=self.edit_expense, bg='#ff9800', fg='white').grid(row=0, column=1, padx=5)

        # Balance frame
        balance_frame = tk.LabelFrame(main_frame, text="Balances", padx=10, pady=10, bg='#f5f5f5', font=('Arial', 12, 'bold'))
        balance_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        tk.Button(balance_frame, text="Calculate Balances", command=self.calculate_balances, bg='#2196F3', fg='white').grid(row=0, column=0, pady=5)

        self.balances_listbox = tk.Listbox(balance_frame)
        self.balances_listbox.grid(row=1, column=0, sticky="nsew")

        # Export button
        tk.Button(main_frame, text="Export Expenses & Balances", command=self.export_data, bg='#9C27B0', fg='white').grid(row=3, column=0, pady=10, sticky="ew")

        # Summary
        self.summary_label = tk.Label(main_frame, text="Total Expenses: 0 | Transactions: 0", bg='#ffffff', font=('Arial', 10, 'italic'))
        self.summary_label.grid(row=4, column=0, pady=10, sticky="ew")

    def add_expense(self):
        desc = self.desc_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        paid_by = self.paid_by_entry.get().strip()
        shared_with = [name.strip() for name in self.shared_with_entry.get().split(',')]
        date = self.date_entry.get().strip()
        category = self.category_entry.get().strip()

        if not desc or not paid_by or not shared_with or not date or not category:
            messagebox.showerror("Error", "All fields are required")
            return

        if paid_by in shared_with:
            messagebox.showerror("Error", "Paid by person cannot be in shared with list")
            return

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
            return

        expense = {
            "desc": desc,
            "amount": amount,
            "paid_by": paid_by,
            "shared_with": shared_with,
            "date": date,
            "category": category
        }

        self.expenses.append(expense)
        self.update_expenses_listbox()
        self.update_summary()

        # Clear input fields
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.paid_by_entry.delete(0, tk.END)
        self.shared_with_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def update_expenses_listbox(self):
        self.expenses_listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.expenses_listbox.insert(
                tk.END, 
                f"{expense['desc']} ({expense['date']}) - {expense['category']}: {expense['amount']} paid by {expense['paid_by']} shared with {', '.join(expense['shared_with'])}"
            )

    def remove_expense(self, event=None):
        selected_idx = self.expenses_listbox.curselection()
        if not selected_idx:
            return

        idx = selected_idx[0]
        del self.expenses[idx]
        self.update_expenses_listbox()
        self.update_summary()

    def edit_expense(self):
        selected_idx = self.expenses_listbox.curselection()
        if not selected_idx:
            return

        idx = selected_idx[0]
        expense = self.expenses[idx]

        # Populate the input fields with selected expense data
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(tk.END, expense['desc'])

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(tk.END, expense['amount'])

        self.paid_by_entry.delete(0, tk.END)
        self.paid_by_entry.insert(tk.END, expense['paid_by'])

        self.shared_with_entry.delete(0, tk.END)
        self.shared_with_entry.insert(tk.END, ', '.join(expense['shared_with']))

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(tk.END, expense['date'])

        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(tk.END, expense['category'])

        # Remove the expense to allow re-adding it
        del self.expenses[idx]
        self.update_expenses_listbox()
        self.update_summary()

    def calculate_balances(self):
        balances = {}
        for expense in self.expenses:
            amount_per_person = expense['amount'] / (len(expense['shared_with']) + 1)

            if expense['paid_by'] not in balances:
                balances[expense['paid_by']] = 0
            balances[expense['paid_by']] += expense['amount'] - amount_per_person

            for person in expense['shared_with']:
                if person not in balances:
                    balances[person] = 0
                balances[person] -= amount_per_person

        self.balances_listbox.delete(0, tk.END)

        for person in balances:
            balances[person] = round(balances[person], 2)

        for person, balance in balances.items():
            if balance > 0:
                self.balances_listbox.insert(tk.END, f"{person} is owed: {balance:.2f}")
            else:
                self.balances_listbox.insert(tk.END, f"{person} owes: {-balance:.2f}")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Description", "Amount", "Paid By", "Shared With", "Date", "Category"])
                for expense in self.expenses:
                    writer.writerow([
                        expense['desc'],
                        expense['amount'],
                        expense['paid_by'],
                        ', '.join(expense['shared_with']),
                        expense['date'],
                        expense['category']
                    ])
                writer.writerow([])
                writer.writerow(["Person", "Balance"])
                balances = self.calculate_balances_dict()
                for person, balance in balances.items():
                    writer.writerow([person, balance])
            messagebox.showinfo("Export Success", "Expenses and balances exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

    def calculate_balances_dict(self):
        balances = {}
        for expense in self.expenses:
            amount_per_person = expense['amount'] / (len(expense['shared_with']) + 1)

            if expense['paid_by'] not in balances:
                balances[expense['paid_by']] = 0
            balances[expense['paid_by']] += expense['amount'] - amount_per_person

            for person in expense['shared_with']:
                if person not in balances:
                    balances[person] = 0
                balances[person] -= amount_per_person

        for person in balances:
            balances[person] = round(balances[person], 2)

        return balances

    def update_summary(self):
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        num_transactions = len(self.expenses)
        self.summary_label.config(text=f"Total Expenses: {total_expenses:.2f} | Transactions: {num_transactions}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSharingApp(root)
    root.mainloop()
