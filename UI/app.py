import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

APP_TITLE = "Lumière Boutique — Tailoring & Order Management"

# ------------------------------------------------------------
# Database layer
# ------------------------------------------------------------
class DB:
    def connect(self):
        return mysql.connector.connect(**DB_CONFIG)

    def fetchall(self, sql, params=()):
        con = self.connect()
        try:
            cur = con.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            con.close()

    def execute(self, sql, params=()):
        con = self.connect()
        try:
            cur = con.cursor()
            cur.execute(sql, params)
            con.commit()
            return cur.lastrowid
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()


db = DB()


def safe_call(action):
    try:
        return action()
    except Error as e:
        messagebox.showerror("Database error", str(e), parent=APP_INSTANCE)
    except Exception as e:
        messagebox.showerror("Something went wrong", str(e), parent=APP_INSTANCE)


def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)


def fill_tree(tree, rows):
    clear_tree(tree)
    for row in rows:
        tree.insert("", "end", values=row)


# ------------------------------------------------------------
# Application
# ------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1360x820")
        self.minsize(1180, 720)
        self.configure(bg="#FFF8FB")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.colors = {
            "bg": "#FFF8FB",
            "white": "#FFFFFF",
            "sidebar": "#FFF0F5",
            "pink": "#D96D91",
            "pink_dark": "#B95378",
            "pink_soft": "#F6D9E3",
            "pink_pale": "#FCEEF3",
            "text": "#3B3034",
            "muted": "#7F7177",
            "border": "#EEDDE4",
            "success": "#4F8A68",
            "warning": "#B9793D",
            "danger": "#B85A67",
        }

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self._configure_styles()

        self.pages = {}
        self.nav_buttons = {}
        self._build_shell()
        self._build_pages()
        self.show_page("Dashboard")
        self.refresh_dashboard()

    # ------------------------- styling -------------------------
    def _configure_styles(self):
        c = self.colors
        s = self.style
        s.configure("App.TFrame", background=c["bg"])
        s.configure("Card.TFrame", background=c["white"])
        s.configure("Sidebar.TFrame", background=c["sidebar"])
        s.configure("Top.TFrame", background=c["white"])
        s.configure("Title.TLabel", background=c["bg"], foreground=c["text"],
                    font=("Segoe UI", 24, "bold"))
        s.configure("PageTitle.TLabel", background=c["bg"], foreground=c["text"],
                    font=("Segoe UI", 18, "bold"))
        s.configure("Subtitle.TLabel", background=c["bg"], foreground=c["muted"],
                    font=("Segoe UI", 10))
        s.configure("CardValue.TLabel", background=c["white"], foreground=c["text"],
                    font=("Segoe UI", 21, "bold"))
        s.configure("CardLabel.TLabel", background=c["white"], foreground=c["muted"],
                    font=("Segoe UI", 9, "bold"))
        s.configure("Section.TLabel", background=c["white"], foreground=c["text"],
                    font=("Segoe UI", 12, "bold"))
        s.configure("Muted.TLabel", background=c["white"], foreground=c["muted"],
                    font=("Segoe UI", 9))
        s.configure("Body.TLabel", background=c["white"], foreground=c["text"],
                    font=("Segoe UI", 10))
        s.configure("Primary.TButton", background=c["pink"], foreground="white",
                    borderwidth=0, font=("Segoe UI", 10, "bold"), padding=(13, 9))
        s.map("Primary.TButton", background=[("active", c["pink_dark"]), ("pressed", c["pink_dark"])])
        s.configure("Soft.TButton", background=c["pink_pale"], foreground=c["pink_dark"],
                    borderwidth=0, font=("Segoe UI", 9, "bold"), padding=(11, 8))
        s.map("Soft.TButton", background=[("active", c["pink_soft"]), ("pressed", c["pink_soft"])])
        s.configure("Danger.TButton", background="#FAE9ED", foreground=c["danger"],
                    borderwidth=0, font=("Segoe UI", 9, "bold"), padding=(11, 8))
        s.configure("Clean.TButton", background=c["white"], foreground=c["text"],
                    borderwidth=1, relief="solid", font=("Segoe UI", 9, "bold"), padding=(11, 8))
        s.configure("Sidebar.TButton", background=c["sidebar"], foreground=c["text"],
                    borderwidth=0, anchor="w", font=("Segoe UI", 10), padding=(14, 11))
        s.map("Sidebar.TButton", background=[("active", c["pink_soft"])], foreground=[("active", c["pink_dark"])])
        s.configure("Treeview", background=c["white"], fieldbackground=c["white"],
                    foreground=c["text"], rowheight=32, font=("Segoe UI", 9), borderwidth=0)
        s.configure("Treeview.Heading", background=c["pink_pale"], foreground=c["pink_dark"],
                    font=("Segoe UI", 9, "bold"), padding=(6, 8), relief="flat")
        s.map("Treeview", background=[("selected", c["pink_soft"])], foreground=[("selected", c["text"])])
        s.configure("TEntry", fieldbackground="#FFFDFE", foreground=c["text"],
                    bordercolor=c["border"], lightcolor=c["border"], darkcolor=c["border"], padding=7)
        s.configure("TCombobox", fieldbackground="#FFFDFE", foreground=c["text"],
                    bordercolor=c["border"], lightcolor=c["border"], darkcolor=c["border"], padding=7)
        s.configure("TCheckbutton", background=c["white"], foreground=c["text"], font=("Segoe UI", 9))

    # ------------------------- shell -------------------------
    def _build_shell(self):
        shell = ttk.Frame(self, style="App.TFrame")
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(shell, width=225, style="Sidebar.TFrame")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # Sidebar brand
        brand = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding=(20, 22, 14, 18))
        brand.pack(fill="x")
        tk.Label(brand, text="✿", bg=self.colors["sidebar"], fg=self.colors["pink"],
                 font=("Segoe UI Symbol", 23)).pack(side="left")
        brand_text = ttk.Frame(brand, style="Sidebar.TFrame")
        brand_text.pack(side="left", padx=(8, 0))
        tk.Label(brand_text, text="LUMIÈRE", bg=self.colors["sidebar"], fg=self.colors["text"],
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(brand_text, text="TAILORING & BOUTIQUE", bg=self.colors["sidebar"], fg=self.colors["muted"],
                 font=("Segoe UI", 7, "bold")).pack(anchor="w")

        nav = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        nav.pack(fill="both", expand=True, padx=10)

        items = [
            ("⌂", "Dashboard"),
            ("♡", "Customers"),
            ("⌁", "Measurements"),
            ("◇", "Garments"),
            ("✦", "Designs"),
            ("◈", "Fabrics & Stock"),
            ("▣", "Orders"),
            ("✂", "Tailors"),
            ("◷", "Trials"),
            ("✧", "Alterations"),
            ("▤", "Billing & Payments"),
            ("▥", "Reports"),
        ]
        for icon, name in items:
            btn = ttk.Button(nav, text=f"  {icon}   {name}", style="Sidebar.TButton",
                             command=lambda n=name: self.show_page(n))
            btn.pack(fill="x", pady=2)
            self.nav_buttons[name] = btn

        bottom = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding=(15, 12, 15, 18))
        bottom.pack(fill="x")
        tk.Label(bottom, text="Database", bg=self.colors["sidebar"], fg=self.colors["muted"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.sidebar_status = tk.Label(bottom, text="● Checking connection…", bg=self.colors["sidebar"],
                                       fg=self.colors["muted"], font=("Segoe UI", 9))
        self.sidebar_status.pack(anchor="w", pady=(3, 9))
        ttk.Button(bottom, text="Test Connection", style="Soft.TButton",
                   command=lambda: safe_call(self.test_connection)).pack(fill="x")

        content = ttk.Frame(shell, style="App.TFrame")
        content.grid(row=0, column=1, sticky="nsew")
        content.rowconfigure(1, weight=1)
        content.columnconfigure(0, weight=1)
        self.content = content

        top = ttk.Frame(content, style="Top.TFrame", padding=(28, 18, 28, 17))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(0, weight=1)
        self.top_title = tk.Label(top, text="Dashboard", bg=self.colors["white"], fg=self.colors["text"],
                                  font=("Segoe UI", 17, "bold"))
        self.top_title.grid(row=0, column=0, sticky="w")
        self.top_sub = tk.Label(top, text="A calm workspace for every stitch, order and delivery.",
                                bg=self.colors["white"], fg=self.colors["muted"], font=("Segoe UI", 9))
        self.top_sub.grid(row=1, column=0, sticky="w", pady=(3, 0))

        self.date_label = tk.Label(top, text=date.today().strftime("%A, %d %B %Y"),
                                   bg=self.colors["white"], fg=self.colors["muted"], font=("Segoe UI", 9))
        self.date_label.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 0))

        self.page_area = ttk.Frame(content, style="App.TFrame", padding=(28, 2, 28, 26))
        self.page_area.grid(row=1, column=0, sticky="nsew")
        self.page_area.rowconfigure(0, weight=1)
        self.page_area.columnconfigure(0, weight=1)

    # ------------------------- helpers -------------------------
    def _page(self, name):
        frame = ttk.Frame(self.page_area, style="App.TFrame")
        frame.grid(row=0, column=0, sticky="nsew")
        self.pages[name] = frame
        return frame

    def _page_header(self, parent, title, subtitle=None):
        box = ttk.Frame(parent, style="App.TFrame")
        box.pack(fill="x", pady=(0, 15))
        ttk.Label(box, text=title, style="PageTitle.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(box, text=subtitle, style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))

    def _card(self, parent, padx=18, pady=16):
        outer = tk.Frame(parent, bg=self.colors["white"], highlightbackground=self.colors["border"],
                         highlightthickness=1, bd=0)
        inner = tk.Frame(outer, bg=self.colors["white"], padx=padx, pady=pady)
        inner.pack(fill="both", expand=True)
        return outer, inner

    def _tree_card(self, parent, columns, widths=None, height=14):
        outer, inner = self._card(parent, padx=10, pady=10)
        tree = ttk.Treeview(inner, columns=columns, show="headings", height=height)
        if widths is None:
            widths = [120] * len(columns)
        for i, col in enumerate(columns):
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=widths[i], minwidth=80, anchor="center")
        scroll = ttk.Scrollbar(inner, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return outer, tree

    def _button_row(self, parent):
        bar = ttk.Frame(parent, style="Card.TFrame")
        bar.pack(fill="x", pady=(0, 10))
        return bar

    def _entry(self, parent, label, variable, row, column, width=20, combo_values=None):
        wrap = tk.Frame(parent, bg=self.colors["white"])
        wrap.grid(row=row, column=column, sticky="ew", padx=7, pady=7)
        tk.Label(wrap, text=label, bg=self.colors["white"], fg=self.colors["muted"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(0, 4))
        if combo_values is not None:
            entry = ttk.Combobox(wrap, textvariable=variable, values=combo_values, width=width, state="readonly")
        else:
            entry = ttk.Entry(wrap, textvariable=variable, width=width)
        entry.pack(fill="x")
        return entry

    def _stat_card(self, parent, title, value_var, icon, col):
        outer, inner = self._card(parent, padx=15, pady=14)
        tk.Label(inner, text=icon, bg=self.colors["pink_pale"], fg=self.colors["pink_dark"],
                 font=("Segoe UI Symbol", 13), width=3, height=1).pack(anchor="w")
        ttk.Label(inner, textvariable=value_var, style="CardValue.TLabel").pack(anchor="w", pady=(9, 0))
        ttk.Label(inner, text=title.upper(), style="CardLabel.TLabel").pack(anchor="w", pady=(1, 0))
        outer.grid(row=0, column=col, sticky="nsew", padx=5)
        return outer

    def _set_status(self, text, ok=True):
        self.sidebar_status.configure(text=text, fg=self.colors["success"] if ok else self.colors["danger"])

    def show_page(self, name):
        for frame in self.pages.values():
            frame.grid_remove()
        self.pages[name].grid()
        self.top_title.configure(text=name)
        subtitles = {
            "Dashboard": "A calm workspace for every stitch, order and delivery.",
            "Customers": "Keep every client profile organised and ready for the next fitting.",
            "Measurements": "Store precise tailoring measurements in one place.",
            "Garments": "Manage your boutique's garment categories and base prices.",
            "Designs": "Keep custom design ideas structured and easy to find.",
            "Fabrics & Stock": "Track fabrics, colours, pricing and remaining stock.",
            "Orders": "Follow every custom order from placement to delivery.",
            "Tailors": "Manage your tailoring team and specialties.",
            "Trials": "Schedule and track fitting appointments.",
            "Alterations": "Keep alterations visible from first note to completion.",
            "Billing & Payments": "Create invoices and keep payment balances clear.",
            "Reports": "Turn your database into useful business insights.",
        }
        self.top_sub.configure(text=subtitles.get(name, "Boutique management workspace."))
        for n, btn in self.nav_buttons.items():
            btn.configure(style="Soft.TButton" if n == name else "Sidebar.TButton")
        refreshers = {
            "Dashboard": self.refresh_dashboard,
            "Customers": self.load_customers,
            "Measurements": self.load_measurements,
            "Garments": self.load_garments,
            "Designs": self.load_designs,
            "Fabrics & Stock": self.load_fabrics,
            "Orders": self.load_orders,
            "Tailors": self.load_tailors,
            "Trials": self.load_trials,
            "Alterations": self.load_alterations,
            "Billing & Payments": self.load_billing,
        }
        if name in refreshers:
            safe_call(refreshers[name])

    # ------------------------- pages -------------------------
    def _build_pages(self):
        self.dashboard_page()
        self.customer_page()
        self.measurement_page()
        self.garment_page()
        self.design_page()
        self.fabric_page()
        self.order_page()
        self.tailor_page()
        self.trial_page()
        self.alteration_page()
        self.billing_page()
        self.report_page()

    # ------------------------- dashboard -------------------------
    def dashboard_page(self):
        p = self._page("Dashboard")
        self._page_header(p, "Welcome back, Aarya ♡", "Your boutique at a glance — customers, orders, stock and revenue.")

        cards = tk.Frame(p, bg=self.colors["bg"])
        cards.pack(fill="x", pady=(0, 15))
        for i in range(5):
            cards.columnconfigure(i, weight=1)
        self.d_customer = tk.StringVar(value="—")
        self.d_orders = tk.StringVar(value="—")
        self.d_pending = tk.StringVar(value="—")
        self.d_tailors = tk.StringVar(value="—")
        self.d_revenue = tk.StringVar(value="—")
        self._stat_card(cards, "Customers", self.d_customer, "♡", 0)
        self._stat_card(cards, "Orders", self.d_orders, "▣", 1)
        self._stat_card(cards, "Pending Orders", self.d_pending, "◷", 2)
        self._stat_card(cards, "Active Tailors", self.d_tailors, "✂", 3)
        self._stat_card(cards, "Revenue", self.d_revenue, "₹", 4)

        grid = tk.Frame(p, bg=self.colors["bg"])
        grid.pack(fill="both", expand=True)
        grid.columnconfigure(0, weight=3)
        grid.columnconfigure(1, weight=2)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)

        outer1, inner1 = self._card(grid, padx=16, pady=15)
        outer1.grid(row=0, column=0, sticky="nsew", padx=(0, 7), pady=(0, 7))
        ttk.Label(inner1, text="Recent Orders", style="Section.TLabel").pack(anchor="w")
        ttk.Label(inner1, text="Latest boutique work entering the system.", style="Muted.TLabel").pack(anchor="w", pady=(2, 10))
        self.dtree = ttk.Treeview(inner1, columns=("order", "customer", "date", "status"), show="headings", height=7)
        for c, w in (("order",110),("customer",180),("date",100),("status",115)):
            self.dtree.heading(c, text=c.title())
            self.dtree.column(c, width=w, anchor="center")
        self.dtree.pack(fill="both", expand=True)

        outer2, inner2 = self._card(grid, padx=16, pady=15)
        outer2.grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=(0, 7))
        ttk.Label(inner2, text="Upcoming Deliveries", style="Section.TLabel").pack(anchor="w")
        ttk.Label(inner2, text="Orders that need attention soon.", style="Muted.TLabel").pack(anchor="w", pady=(2, 10))
        self.delivery_box = tk.Listbox(inner2, borderwidth=0, highlightthickness=0, bg=self.colors["white"],
                                       fg=self.colors["text"], font=("Segoe UI", 9), activestyle="none")
        self.delivery_box.pack(fill="both", expand=True)

        outer3, inner3 = self._card(grid, padx=16, pady=15)
        outer3.grid(row=1, column=0, sticky="nsew", padx=(0, 7), pady=(7, 0))
        ttk.Label(inner3, text="Low Stock Fabrics", style="Section.TLabel").pack(anchor="w")
        ttk.Label(inner3, text="Restock anything below its reorder level.", style="Muted.TLabel").pack(anchor="w", pady=(2, 10))
        self.stock_tree = ttk.Treeview(inner3, columns=("fabric", "colour", "stock", "reorder"), show="headings", height=6)
        for c, w in (("fabric",170),("colour",110),("stock",90),("reorder",90)):
            self.stock_tree.heading(c, text=c.title())
            self.stock_tree.column(c, width=w, anchor="center")
        self.stock_tree.pack(fill="both", expand=True)

        outer4, inner4 = self._card(grid, padx=16, pady=15)
        outer4.grid(row=1, column=1, sticky="nsew", padx=(7, 0), pady=(7, 0))
        ttk.Label(inner4, text="Quick Actions", style="Section.TLabel").pack(anchor="w")
        ttk.Label(inner4, text="Jump straight into the most common tasks.", style="Muted.TLabel").pack(anchor="w", pady=(2, 10))
        for text, page in (("＋  Add Customer", "Customers"), ("＋  Create Order", "Orders"),
                           ("✂  Manage Tailors", "Tailors"), ("▤  Open Billing", "Billing & Payments")):
            ttk.Button(inner4, text=text, style="Soft.TButton", command=lambda n=page: self.show_page(n)).pack(fill="x", pady=4)

    def refresh_dashboard(self):
        try:
            counts = {
                "customer": db.fetchall("SELECT COUNT(*) FROM customers")[0][0],
                "orders": db.fetchall("SELECT COUNT(*) FROM orders")[0][0],
                "pending": db.fetchall("SELECT COUNT(*) FROM orders WHERE status IN ('PLACED','IN_PROGRESS','TRIAL','ALTERATION')")[0][0],
                "tailors": db.fetchall("SELECT COUNT(*) FROM tailors WHERE status='ACTIVE'")[0][0],
                "revenue": db.fetchall("SELECT COALESCE(SUM(total_amount),0) FROM invoices")[0][0],
            }
            self.d_customer.set(str(counts["customer"]))
            self.d_orders.set(str(counts["orders"]))
            self.d_pending.set(str(counts["pending"]))
            self.d_tailors.set(str(counts["tailors"]))
            self.d_revenue.set(f"₹{float(counts['revenue']):,.0f}")

            recent = db.fetchall("""SELECT o.order_no, c.full_name, o.order_date, o.status
                                   FROM orders o JOIN customers c ON c.customer_id=o.customer_id
                                   ORDER BY o.order_id DESC LIMIT 8""")
            clear_tree(self.dtree)
            for row in recent:
                self.dtree.insert("", "end", values=row)

            upcoming = db.fetchall("""SELECT order_no, delivery_date, status
                                    FROM orders
                                    WHERE delivery_date >= CURRENT_DATE
                                      AND status <> 'DELIVERED'
                                    ORDER BY delivery_date LIMIT 6""")
            self.delivery_box.delete(0, "end")
            for order_no, delivery_date, status in upcoming:
                self.delivery_box.insert("end", f"  {order_no}   •   {delivery_date}   •   {status.replace('_',' ')}")
            if not upcoming:
                self.delivery_box.insert("end", "  No upcoming deliveries.")

            stock = db.fetchall("""SELECT f.fabric_name, f.colour, fs.quantity_meters, fs.reorder_level
                                 FROM fabric_stock fs JOIN fabrics f ON f.fabric_id=fs.fabric_id
                                 WHERE fs.quantity_meters <= fs.reorder_level
                                 ORDER BY fs.quantity_meters ASC LIMIT 8""")
            clear_tree(self.stock_tree)
            for row in stock:
                self.stock_tree.insert("", "end", values=row)
            self._set_status("● Database connected", True)
        except Exception:
            self._set_status("● Database offline", False)

    # ------------------------- customers -------------------------
    def customer_page(self):
        p = self._page("Customers")
        self._page_header(p, "Customers", "Create and maintain customer profiles for fittings, orders and history.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0, 12))
        ttk.Label(inner, text="Customer details", style="Section.TLabel").grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 5))
        self.cvars = [tk.StringVar() for _ in range(5)]
        labels = ["Customer code", "Full name", "Phone", "Email", "Address"]
        for i, (lab, var) in enumerate(zip(labels, self.cvars)):
            self._entry(inner, lab, var, 1, i, 18)
        bar = self._button_row(inner)
        bar.grid(row=2, column=0, columnspan=5, sticky="ew", pady=(9, 0))
        ttk.Button(bar, text="＋ Add Customer", style="Primary.TButton", command=lambda: safe_call(self.insert_customer)).pack(side="left", padx=(0, 6))
        ttk.Button(bar, text="Delete selected", style="Danger.TButton", command=lambda: safe_call(self.delete_customer)).pack(side="left", padx=3)
        ttk.Button(bar, text="Refresh", style="Clean.TButton", command=self.load_customers).pack(side="left", padx=3)
        ttk.Label(bar, text="Tip: select a row before deleting.", style="Muted.TLabel").pack(side="right")
        outer2, self.ctree = self._tree_card(p, ["id","code","name","phone","email","address","created_at"], [60,90,170,120,200,220,145], height=12)
        outer2.pack(fill="both", expand=True)
        self.ctree.bind("<<TreeviewSelect>>", self._customer_select)

    def _customer_select(self, _=None):
        sel = self.ctree.selection()
        if not sel:
            return
        vals = self.ctree.item(sel[0], "values")
        for var, value in zip(self.cvars, vals[1:6]):
            var.set(value)

    def load_customers(self):
        rows = db.fetchall("SELECT customer_id,customer_code,full_name,phone,email,address,created_at FROM customers ORDER BY customer_id")
        fill_tree(self.ctree, rows)

    def insert_customer(self):
        code, name, phone, email, address = [v.get().strip() for v in self.cvars]
        if not code or not name or not phone:
            raise ValueError("Customer code, full name and phone are required.")
        db.execute("INSERT INTO customers(customer_code,full_name,phone,email,address) VALUES(%s,%s,%s,%s,%s)",
                   (code, name, phone, email or None, address or None))
        for v in self.cvars:
            v.set("")
        self.load_customers()
        self.refresh_dashboard()
        messagebox.showinfo("Customer added", "The customer has been saved to MySQL.", parent=self)

    def delete_customer(self):
        sel = self.ctree.selection()
        if not sel:
            raise ValueError("Select a customer row first.")
        vals = self.ctree.item(sel[0], "values")
        if messagebox.askyesno("Delete customer", f"Delete {vals[2]}?\n\nThis will follow the database's foreign-key rules.", parent=self):
            db.execute("DELETE FROM customers WHERE customer_id=%s", (vals[0],))
            self.load_customers()
            self.refresh_dashboard()

    # ------------------------- measurements -------------------------
    def measurement_page(self):
        p = self._page("Measurements")
        self._page_header(p, "Measurements", "Precise profiles for better fitting and fewer alterations.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0, 12))
        fields = ["Customer ID", "Bust (cm)", "Waist (cm)", "Hip (cm)", "Shoulder (cm)", "Sleeve (cm)", "Length (cm)"]
        self.mvars = [tk.StringVar() for _ in fields]
        for i, (lab, var) in enumerate(zip(fields, self.mvars)):
            self._entry(inner, lab, var, 0, i, 13)
        bar = self._button_row(inner)
        bar.grid(row=1, column=0, columnspan=7, sticky="ew", pady=(8, 0))
        ttk.Button(bar, text="Save measurement", style="Primary.TButton", command=lambda: safe_call(self.save_measurement)).pack(side="left")
        ttk.Button(bar, text="Refresh", style="Clean.TButton", command=self.load_measurements).pack(side="left", padx=7)
        outer2, self.mtree = self._tree_card(p, ["measurement_id","customer_id","bust","waist","hip","shoulder","sleeve","length"], [100,100,95,95,95,100,95,95], height=13)
        outer2.pack(fill="both", expand=True)

    def save_measurement(self):
        vals = [v.get().strip() for v in self.mvars]
        if not all(vals):
            raise ValueError("Please fill every measurement field.")
        sql = """INSERT INTO measurement_profiles(customer_id,bust_cm,waist_cm,hip_cm,shoulder_cm,sleeve_cm,length_cm)
                 VALUES(%s,%s,%s,%s,%s,%s,%s)
                 ON DUPLICATE KEY UPDATE bust_cm=VALUES(bust_cm),waist_cm=VALUES(waist_cm),hip_cm=VALUES(hip_cm),
                 shoulder_cm=VALUES(shoulder_cm),sleeve_cm=VALUES(sleeve_cm),length_cm=VALUES(length_cm)"""
        db.execute(sql, tuple(vals))
        self.load_measurements()

    def load_measurements(self):
        fill_tree(self.mtree, db.fetchall("SELECT measurement_id,customer_id,bust_cm,waist_cm,hip_cm,shoulder_cm,sleeve_cm,length_cm FROM measurement_profiles ORDER BY measurement_id"))

    # ------------------------- garments -------------------------
    def garment_page(self):
        p = self._page("Garments")
        self._page_header(p, "Garments", "A clean catalogue of the boutique's garment categories.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0, 12))
        self.gvars = [tk.StringVar() for _ in range(3)]
        labels = ["Garment name", "Description", "Base price"]
        for i, (lab, var) in enumerate(zip(labels, self.gvars)):
            self._entry(inner, lab, var, 0, i, 24)
        ttk.Button(inner, text="Add garment", style="Primary.TButton", command=lambda: safe_call(self.add_garment)).grid(row=0, column=3, padx=8, pady=7, sticky="s")
        self.gtree_card, self.gtree = self._tree_card(p, ["id","name","description","price"], [90,170,480,140], height=14)
        self.gtree_card.pack(fill="both", expand=True)

    def add_garment(self):
        name, desc, price = [v.get().strip() for v in self.gvars]
        if not name:
            raise ValueError("Garment name is required.")
        db.execute("INSERT INTO garment_types(garment_name,description,base_price) VALUES(%s,%s,%s)", (name, desc or None, price or 0))
        for v in self.gvars: v.set("")
        self.load_garments()

    def load_garments(self):
        fill_tree(self.gtree, db.fetchall("SELECT garment_type_id,garment_name,description,base_price FROM garment_types ORDER BY garment_type_id"))

    # ------------------------- designs -------------------------
    def design_page(self):
        p = self._page("Designs")
        self._page_header(p, "Designs", "Keep custom styles organised across garment categories.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0, 12))
        self.dvars = [tk.StringVar() for _ in range(4)]
        labels = ["Design code", "Design name", "Garment type ID", "Description"]
        for i, (lab, var) in enumerate(zip(labels, self.dvars)):
            self._entry(inner, lab, var, 0, i, 21)
        ttk.Button(inner, text="Add design", style="Primary.TButton", command=lambda: safe_call(self.add_design)).grid(row=0, column=4, padx=8, pady=7, sticky="s")
        self.design_card, self.designtree = self._tree_card(p, ["id","code","name","garment_type_id","description"], [80,110,180,120,460], height=14)
        self.design_card.pack(fill="both", expand=True)

    def add_design(self):
        code, name, gid, desc = [v.get().strip() for v in self.dvars]
        if not code or not name or not gid:
            raise ValueError("Design code, name and garment type ID are required.")
        db.execute("INSERT INTO designs(design_code,design_name,garment_type_id,description) VALUES(%s,%s,%s,%s)", (code, name, gid, desc or None))
        for v in self.dvars: v.set("")
        self.load_designs()

    def load_designs(self):
        fill_tree(self.designtree, db.fetchall("SELECT design_id,design_code,design_name,garment_type_id,description FROM designs ORDER BY design_id"))

    # ------------------------- fabrics -------------------------
    def fabric_page(self):
        p = self._page("Fabrics & Stock")
        self._page_header(p, "Fabrics & Stock", "Track fabric pricing, colours and inventory before the next cut.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0, 12))
        self.fvars2 = [tk.StringVar() for _ in range(6)]
        labels = ["Fabric code", "Fabric name", "Type", "Colour", "Price / meter", "Opening stock"]
        for i, (lab, var) in enumerate(zip(labels, self.fvars2)):
            self._entry(inner, lab, var, 0, i, 15)
        ttk.Button(inner, text="Add fabric", style="Primary.TButton", command=lambda: safe_call(self.add_fabric)).grid(row=1, column=5, padx=8, pady=7, sticky="e")
        self.fabric_card, self.ftree2 = self._tree_card(p, ["id","code","name","type","colour","price","stock","reorder","status"], [70,95,160,110,100,95,95,95,110], height=13)
        self.fabric_card.pack(fill="both", expand=True)

    def add_fabric(self):
        code, name, typ, colour, price, stock = [v.get().strip() for v in self.fvars2]
        if not code or not name or not typ:
            raise ValueError("Fabric code, name and type are required.")
        fabric_id = db.execute("INSERT INTO fabrics(fabric_code,fabric_name,fabric_type,colour,price_per_meter) VALUES(%s,%s,%s,%s,%s)",
                               (code, name, typ, colour or None, price or 0))
        db.execute("INSERT INTO fabric_stock(fabric_id,quantity_meters,reorder_level) VALUES(%s,%s,%s)", (fabric_id, stock or 0, 5))
        for v in self.fvars2: v.set("")
        self.load_fabrics()
        self.refresh_dashboard()

    def load_fabrics(self):
        rows = db.fetchall("""SELECT f.fabric_id,f.fabric_code,f.fabric_name,f.fabric_type,f.colour,f.price_per_meter,
                            fs.quantity_meters,fs.reorder_level,
                            CASE WHEN fs.quantity_meters <= fs.reorder_level THEN 'LOW STOCK' ELSE 'IN STOCK' END
                            FROM fabrics f LEFT JOIN fabric_stock fs ON fs.fabric_id=f.fabric_id
                            ORDER BY f.fabric_id""")
        fill_tree(self.ftree2, rows)

    # ------------------------- orders -------------------------
    def order_page(self):
        p = self._page("Orders")
        self._page_header(p, "Orders", "Follow every custom order from placement to final delivery.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0, 12))
        self.ovars = {x: tk.StringVar() for x in ["order_no","customer_id","delivery_date","status","instructions"]}
        self.ovars["delivery_date"].set(date.today().isoformat())
        self.ovars["status"].set("PLACED")
        self._entry(inner, "Order no.", self.ovars["order_no"], 0, 0, 18)
        self._entry(inner, "Customer ID", self.ovars["customer_id"], 0, 1, 15)
        self._entry(inner, "Delivery date (YYYY-MM-DD)", self.ovars["delivery_date"], 0, 2, 18)
        self._entry(inner, "Status", self.ovars["status"], 0, 3, 15,
                   ["PLACED","IN_PROGRESS","TRIAL","ALTERATION","READY","DELIVERED","CANCELLED"])
        self._entry(inner, "Special instructions", self.ovars["instructions"], 0, 4, 26)
        bar = self._button_row(inner)
        bar.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(8,0))
        ttk.Button(bar, text="＋ Create order", style="Primary.TButton", command=lambda: safe_call(self.create_order)).pack(side="left")
        ttk.Button(bar, text="Refresh", style="Clean.TButton", command=self.load_orders).pack(side="left", padx=7)
        self.order_card, self.otree = self._tree_card(p, ["id","order_no","customer_id","order_date","delivery_date","status","instructions"], [60,105,95,105,105,120,350], height=12)
        self.order_card.pack(fill="both", expand=True)

    def create_order(self):
        v = self.ovars
        vals = [v[x].get().strip() for x in ["order_no","customer_id","delivery_date","status","instructions"]]
        if not vals[0] or not vals[1] or not vals[2]:
            raise ValueError("Order number, customer ID and delivery date are required.")
        db.execute("INSERT INTO orders(order_no,customer_id,delivery_date,status,special_instructions) VALUES(%s,%s,%s,%s,%s)",
                   (vals[0], vals[1], vals[2], vals[3], vals[4] or None))
        self.load_orders()
        self.refresh_dashboard()

    def load_orders(self):
        fill_tree(self.otree, db.fetchall("SELECT order_id,order_no,customer_id,order_date,delivery_date,status,special_instructions FROM orders ORDER BY order_id DESC"))

    # ------------------------- tailors -------------------------
    def tailor_page(self):
        p = self._page("Tailors")
        self._page_header(p, "Tailors", "Manage your tailoring team, specialisations and active availability.")
        outer, inner = self._card(p)
        outer.pack(fill="x", pady=(0,12))
        self.tlvars = [tk.StringVar() for _ in range(5)]
        labels = ["Tailor code","Name","Specialization","Phone","Status"]
        for i, (lab,var) in enumerate(zip(labels,self.tlvars)):
            vals = ["ACTIVE","INACTIVE"] if lab == "Status" else None
            self._entry(inner, lab, var, 0, i, 18, vals)
        self.tlvars[-1].set("ACTIVE")
        ttk.Button(inner, text="Add tailor", style="Primary.TButton", command=lambda: safe_call(self.add_tailor)).grid(row=0,column=5,padx=8,pady=7,sticky="s")
        self.tlcard, self.tltree = self._tree_card(p,["id","code","name","specialization","phone","status"],[70,100,180,180,120,100],height=14)
        self.tlcard.pack(fill="both",expand=True)

    def add_tailor(self):
        vals=[v.get().strip() for v in self.tlvars]
        if not vals[0] or not vals[1]:
            raise ValueError("Tailor code and name are required.")
        db.execute("INSERT INTO tailors(tailor_code,tailor_name,specialization,phone,status) VALUES(%s,%s,%s,%s,%s)",tuple(vals))
        for v in self.tlvars: v.set("")
        self.tlvars[-1].set("ACTIVE")
        self.load_tailors(); self.refresh_dashboard()

    def load_tailors(self):
        fill_tree(self.tltree, db.fetchall("SELECT tailor_id,tailor_code,tailor_name,specialization,phone,status FROM tailors ORDER BY tailor_id"))

    # ------------------------- trials -------------------------
    def trial_page(self):
        p = self._page("Trials")
        self._page_header(p, "Trials", "Keep fitting appointments visible and conflict-free.")
        outer, inner = self._card(p); outer.pack(fill="x",pady=(0,12))
        self.tvars = {x:tk.StringVar() for x in ["order_id","tailor_id","datetime","notes"]}
        labels=["Order ID","Tailor ID","Date & time","Notes"]
        for i,(lab,x) in enumerate(zip(labels,self.tvars)):
            self._entry(inner,lab,self.tvars[x],0,i,22)
        ttk.Button(inner,text="Schedule trial",style="Primary.TButton",command=lambda:safe_call(self.schedule_trial)).grid(row=0,column=4,padx=8,pady=7,sticky="s")
        self.trial_card,self.ttree=self._tree_card(p,["trial_id","order_id","tailor_id","trial_datetime","status","notes"],[80,100,100,160,120,380],height=14)
        self.trial_card.pack(fill="both",expand=True)

    def schedule_trial(self):
        v=self.tvars
        vals=[v[x].get().strip() for x in ["order_id","tailor_id","datetime","notes"]]
        if not vals[0] or not vals[1] or not vals[2]: raise ValueError("Order, tailor and date/time are required.")
        db.execute("INSERT INTO trials(order_id,tailor_id,trial_datetime,notes) VALUES(%s,%s,%s,%s)",(vals[0],vals[1],vals[2],vals[3] or None))
        self.load_trials()

    def load_trials(self):
        fill_tree(self.ttree,db.fetchall("SELECT trial_id,order_id,tailor_id,trial_datetime,trial_status,notes FROM trials ORDER BY trial_datetime"))

    # ------------------------- alterations -------------------------
    def alteration_page(self):
        p=self._page("Alterations")
        self._page_header(p,"Alterations","Track fitting changes, costs and completion status.")
        outer,inner=self._card(p); outer.pack(fill="x",pady=(0,12))
        self.alvars=[tk.StringVar() for _ in range(4)]
        labels=["Order ID","Trial ID","Alteration details","Cost"]
        for i,(lab,var) in enumerate(zip(labels,self.alvars)):
            self._entry(inner,lab,var,0,i,25)
        ttk.Button(inner,text="Add alteration",style="Primary.TButton",command=lambda:safe_call(self.add_alteration)).grid(row=0,column=4,padx=8,pady=7,sticky="s")
        self.altcard,self.altree=self._tree_card(p,["id","order_id","trial_id","date","details","cost","status"],[70,95,90,110,420,100,120],height=13)
        self.altcard.pack(fill="both",expand=True)

    def add_alteration(self):
        vals=[v.get().strip() for v in self.alvars]
        if not vals[0] or not vals[2]: raise ValueError("Order ID and alteration details are required.")
        db.execute("INSERT INTO alterations(order_id,trial_id,alteration_details,alteration_cost) VALUES(%s,%s,%s,%s)",(vals[0],vals[1] or None,vals[2],vals[3] or 0))
        self.load_alterations()

    def load_alterations(self):
        fill_tree(self.altree,db.fetchall("SELECT alteration_id,order_id,trial_id,alteration_date,alteration_details,alteration_cost,alteration_status FROM alterations ORDER BY alteration_id DESC"))

    # ------------------------- billing -------------------------
    def billing_page(self):
        p=self._page("Billing & Payments")
        self._page_header(p,"Billing & Payments","Keep invoices, received amounts and outstanding balances crystal clear.")
        outer,inner=self._card(p); outer.pack(fill="x",pady=(0,10))
        self.ivars={x:tk.StringVar() for x in ["invoice_no","order_id","subtotal","alteration_total"]}
        for i,x in enumerate(self.ivars):
            self._entry(inner,x.replace("_"," ").title(),self.ivars[x],0,i,20)
        ttk.Button(inner,text="Create invoice",style="Primary.TButton",command=lambda:safe_call(self.create_invoice)).grid(row=0,column=4,padx=8,pady=7,sticky="s")
        outer2,inner2=self._card(p); outer2.pack(fill="x",pady=(0,10))
        self.pvars={x:tk.StringVar() for x in ["invoice_id","amount","method","reference"]}
        labels=["Invoice ID","Amount","Payment method","Reference no."]
        for i,(lab,x) in enumerate(zip(labels,self.pvars)):
            vals=["CASH","UPI","CARD","BANK_TRANSFER"] if x=="method" else None
            self._entry(inner2,lab,self.pvars[x],0,i,20,vals)
        self.pvars["method"].set("UPI")
        ttk.Button(inner2,text="Add payment",style="Soft.TButton",command=lambda:safe_call(self.add_payment)).grid(row=0,column=4,padx=8,pady=7,sticky="s")
        self.billcard,self.btree=self._tree_card(p,["invoice_no","order_id","total","paid","balance"],[150,100,130,130,130],height=12)
        self.billcard.pack(fill="both",expand=True)

    def create_invoice(self):
        v=self.ivars
        subtotal=float(v["subtotal"].get())
        alt=float(v["alteration_total"].get() or 0)
        db.execute("INSERT INTO invoices(invoice_no,order_id,subtotal,alteration_total,total_amount) VALUES(%s,%s,%s,%s,%s)",(v["invoice_no"].get().strip(),v["order_id"].get().strip(),subtotal,alt,subtotal+alt))
        self.load_billing(); self.refresh_dashboard()

    def add_payment(self):
        v=self.pvars
        if not v["invoice_id"].get().strip() or not v["amount"].get().strip(): raise ValueError("Invoice ID and amount are required.")
        db.execute("INSERT INTO payments(invoice_id,amount,payment_method,reference_no) VALUES(%s,%s,%s,%s)",(v["invoice_id"].get().strip(),v["amount"].get().strip(),v["method"].get().strip(),v["reference"].get().strip() or None))
        self.load_billing(); self.refresh_dashboard()

    def load_billing(self):
        rows=db.fetchall("""SELECT i.invoice_no,i.order_id,i.total_amount,COALESCE(SUM(p.amount),0),
                           i.total_amount-COALESCE(SUM(p.amount),0)
                           FROM invoices i LEFT JOIN payments p ON p.invoice_id=i.invoice_id
                           GROUP BY i.invoice_id,i.invoice_no,i.order_id,i.total_amount""")
        fill_tree(self.btree,rows)

    # ------------------------- reports -------------------------
    def report_page(self):
        p=self._page("Reports")
        self._page_header(p,"Reports","Quick views for pending work, delivery, workload, history and revenue.")
        bar_outer,bar=self._card(p,padx=13,pady=12); bar_outer.pack(fill="x",pady=(0,12))
        buttons=[
            ("Pending orders","SELECT * FROM v_pending_orders"),
            ("Delivery due","SELECT * FROM v_delivery_due"),
            ("Tailor workload","SELECT * FROM v_tailor_workload"),
            ("Customer history","SELECT * FROM v_customer_history"),
            ("Revenue","SELECT * FROM v_revenue"),
            ("Fabric usage","SELECT f.fabric_name,SUM(fi.quantity_meters) meters_issued FROM fabrics f JOIN fabric_issues fi ON fi.fabric_id=f.fabric_id GROUP BY f.fabric_id,f.fabric_name"),
        ]
        for label,sql in buttons:
            ttk.Button(bar,text=label,style="Soft.TButton",command=lambda s=sql,l=label:self.show_report(s,l)).pack(side="left",padx=4)
        self.report_title=tk.StringVar(value="Choose a report")
        ttk.Label(p,textvariable=self.report_title,style="Section.TLabel").pack(anchor="w",pady=(0,6))
        self.rcard,self.rtree=self._tree_card(p,["result"],[800],height=16)
        self.rcard.pack(fill="both",expand=True)

    def show_report(self,sql,title):
        rows=db.fetchall(sql)
        self.report_title.set(title)
        clear_tree(self.rtree)
        if not rows:
            self.rtree.configure(columns=("result",),show="headings")
            self.rtree.heading("result",text="RESULT")
            self.rtree.insert("","end",values=("No records found.",))
            return
        cols=[f"c{i+1}" for i in range(len(rows[0]))]
        self.rtree.configure(columns=cols,show="headings")
        for i,c in enumerate(cols):
            self.rtree.heading(c,text=c.upper())
            self.rtree.column(c,width=max(140, min(240, 860//len(cols))),anchor="center")
        for row in rows:
            self.rtree.insert("","end",values=row)

    # ------------------------- shared actions -------------------------
    def test_connection(self):
        rows=db.fetchall("SELECT DATABASE(), CURRENT_USER()")
        self._set_status("● Database connected", True)
        messagebox.showinfo("Connection successful",f"Database: {rows[0][0]}\nUser: {rows[0][1]}",parent=self)


APP_INSTANCE = None

if __name__ == "__main__":
    APP_INSTANCE = App()
    APP_INSTANCE.mainloop()
