import tkinter as tk
from tkinter import simpledialog, messagebox

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget App")
        self.geometry("500x500")

        # Initialize categories and totals
        self.categories = ['Gas', 'Food', 'Entertainment', 'Clothing', 'Bills']
        self.reset_totals()

        # Category management section
        self.manage_categories_frame = tk.LabelFrame(self, text="Manage Categories", padx=10, pady=10)
        self.manage_categories_frame.pack(padx=10, pady=5, fill="x")

        self.category_listbox = tk.Listbox(self.manage_categories_frame)
        self.category_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        self.update_category_listbox()

        self.add_category_button = tk.Button(self.manage_categories_frame, text="Add Category", command=self.add_category)
        self.add_category_button.pack(side=tk.LEFT, padx=5)

        self.remove_category_button = tk.Button(self.manage_categories_frame, text="Remove Category", command=self.remove_category)
        self.remove_category_button.pack(side=tk.LEFT)

        # Purchase entry section
        self.purchase_frame = tk.LabelFrame(self, text="Add Purchase", padx=10, pady=10)
        self.purchase_frame.pack(padx=10, pady=5, fill="x")

        self.cost_label = tk.Label(self.purchase_frame, text="Cost:")
        self.cost_label.pack(side=tk.LEFT)
        self.cost_entry = tk.Entry(self.purchase_frame, width=10)
        self.cost_entry.pack(side=tk.LEFT, padx=5)

        self.category_label = tk.Label(self.purchase_frame, text="Category:")
        self.category_label.pack(side=tk.LEFT)
        self.category_var = tk.StringVar(self)
        self.category_optionmenu = tk.OptionMenu(self.purchase_frame, self.category_var, *self.categories)
        self.category_optionmenu.pack(side=tk.LEFT, padx=5)

        self.add_purchase_button = tk.Button(self.purchase_frame, text="Add Purchase", command=self.add_purchase)
        self.add_purchase_button.pack(side=tk.LEFT, padx=5)

        # Summary and control section
        self.summary_frame = tk.LabelFrame(self, text="Controls and Summary", padx=10, pady=10)
        self.summary_frame.pack(padx=10, pady=5, fill="x")

        self.total_cost_button = tk.Button(self.summary_frame, text="Calculate Total Cost", command=self.show_summary)
        self.total_cost_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.summary_frame, text="Clear/Reset", command=self.reset_data)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.summary_text = tk.Text(self.summary_frame, height=10, width=50)
        self.summary_text.pack()

    def update_category_listbox(self):
        self.category_listbox.delete(0, tk.END)
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

    def add_category(self):
        new_category = simpledialog.askstring("Add Category", "Category name:")
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.totals[new_category] = 0  # Initialize new category total
            self.update_category_listbox()
            self.category_var.set(new_category)
            self.update_optionmenu()

    def remove_category(self):
        if self.category_listbox.curselection():
            index = self.category_listbox.curselection()[0]
            category = self.category_listbox.get(index)
            del self.totals[category]  # Remove category from totals
            self.categories.remove(category)
            self.update_category_listbox()
            if self.categories:
                self.category_var.set(self.categories[0])
            self.update_optionmenu()

    def update_optionmenu(self):
        menu = self.category_optionmenu["menu"]
        menu.delete(0, "end")
        for category in self.categories:
            menu.add_command(label=category, command=lambda value=category: self.category_var.set(value))

    def add_purchase(self):
        try:
            cost = float(self.cost_entry.get())
            category = self.category_var.get()
            if category and category in self.totals:
                self.totals[category] += cost
                self.total_spent += cost
                messagebox.showinfo("Purchase Added", f"Added ${cost} to {category}")
                self.cost_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid cost. Please enter a number.")

    def show_summary(self):
        self.summary_text.delete('1.0', tk.END)  # Clear existing text
        if self.total_spent > 0:
            summary_message = f"Total Spent: ${self.total_spent:.2f}\n"
            for category, total in self.totals.items():
                percentage = (total / self.total_spent) * 100 if self.total_spent else 0
                summary_message += f"{category}: ${total:.2f} ({percentage:.2f}%)\n"
            self.summary_text.insert(tk.END, summary_message)
        else:
            self.summary_text.insert(tk.END, "No purchases recorded.")

    def reset_totals(self):
        self.totals = {category: 0 for category in self.categories}
        self.total_spent = 0

    def reset_data(self):
        self.reset_totals()
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert(tk.END, "Data has been reset. Please add new purchases.")

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
