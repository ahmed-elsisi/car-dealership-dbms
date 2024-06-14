import csv
from tkinter import *
from tkinter import ttk
import pymysql
from pymysql import cursors
import random
import datetime
import time


def database_operation(query):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='28o12o2002',
        db='car_dealership',
    )

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return cursor.fetchall()


def main_operations():
    global root
    root.destroy()

    def filter_operation():
        global root
        root.destroy()

        def search_cars():
            for item in tree.get_children():
                tree.delete(item)

            brand = brand_entry_field.get()
            model = model_entry_field.get()
            year = year_entry_field.get()
            min_price = min_price_entry_field.get()
            max_price = max_price_entry_field.get()

            query = 'SELECT * FROM `car` WHERE'
            if brand != '':
                query = f'{query} `brand`="{brand}" AND'

            if model != '':
                if 'AND' in query:
                    query = f'{query} `model`="{model}" AND'
                elif 'AND' not in query:
                    query = f'{query} AND `model`="{model}" AND'

            if year != '':
                if 'AND' in query:
                    query = f'{query} `year`={year} AND'
                elif 'AND' not in query:
                    query = f'{query} AND `year`={year} AND'

            if min_price != '':
                if 'AND' in query:
                    query = f'{query} `price`>{int(min_price)} AND'
                elif 'AND' not in query:
                    query = f'{query} AND `price`>{int(min_price)} AND'

            if max_price != '':
                if 'AND' in query:
                    query = f'{query} `price`<{int(max_price)} AND'
                elif 'AND' not in query:
                    query = f'{query} AND `price`<{int(max_price)} AND'

            query = query.strip(' AND').replace('WHERE AND', 'WHERE')

            query_label = Label(root, text=f'Current Query: {query}')
            query_label.place(x=200, y=570)
            root.update()
            results = database_operation(query)

            for result in results:
                tree.insert('', 'end', values=result)

        root = Tk()
        root.geometry('1000x700')
        root.title('Dealership Selection System')

        brand_label = Label(root, text='Brand')
        brand_entry_field = Entry(root)

        model_label = Label(root, text='Model')
        model_entry_field = Entry(root)

        year_label = Label(root, text='Year')
        year_entry_field = Entry(root)

        price_label = Label(root, text='Price')
        to_label = Label(root, text='->')
        min_price_entry_field = Entry(root)
        max_price_entry_field = Entry(root)

        search_button = Button(root, text='Search', command=lambda: search_cars())

        columns = ('id', 'brand', 'model', 'year', 'price')
        tree = ttk.Treeview(root, column=columns, show='headings')
        tree.column("id", width=75, anchor=CENTER)
        tree.heading("id", text="ID")
        tree.column("brand", width=150, anchor=CENTER)
        tree.heading("brand", text="Brand")
        tree.column("model", width=150, anchor=CENTER)
        tree.heading("model", text="Model")
        tree.column("year", width=75, anchor=CENTER)
        tree.heading("year", text="Year")
        tree.column("price", width=150, anchor=CENTER)
        tree.heading("price", text="Price")

        tree.place(x=330, y=50, height=500)

        brand_label.place(x=25, y=98)
        brand_entry_field.place(x=70, y=100)

        model_label.place(x=24, y=98 + 50)
        model_entry_field.place(x=70, y=100 + 50)

        year_label.place(x=23, y=98 + 100)
        year_entry_field.place(x=70, y=100 + 100)

        price_label.place(x=24, y=98 + 150)
        to_label.place(x=150, y=98 + 150)
        min_price_entry_field.place(x=70, y=100 + 150, width=75)
        max_price_entry_field.place(x=175, y=100 + 150, width=75)
        search_button.place(x=70, y=100 + 225, width=180, height=40)

    def sell_operation():
        global root

        root.destroy()

        root = Tk()
        root.geometry('575x400')
        root.title('Dealership Sale Operation')

        def confirm_sale():
            sale_status = False

            car_id_sale = car_id_entry.get()

            customer_name_sale = customer_name_entry.get()
            customer_phone_sale = customer_phone_entry.get()

            salesperson_id_sale = salesperson_id_entry.get()

            model_sale = database_operation(f'SELECT `car`.`model` FROM `car` WHERE `id` = "{car_id_sale}"')

            price_sale = database_operation(f'SELECT `car`.`price` FROM `car` WHERE `id` = "{car_id_sale}"')

            car_model.config(state='normal')
            car_model.delete(0, END)

            final_price_amount.config(state='normal')
            final_price_amount.delete(0, END)

            try:
                car_model.insert(0, model_sale[0][0])
                final_price_amount.insert(0, f"{str(round(int(price_sale[0][0]) * 1.14))}")
                car_model.config(state='disabled')
                final_price_amount.config(state='disabled')
            except IndexError:
                car_model.insert(0, 'False ID')
                final_price_amount.insert(0, 'False ID')
                car_model.config(state='disabled')
                final_price_amount.config(state='disabled')
                return

            today = datetime.date.today()
            formatted_date = today.strftime('%Y-%m-%d')

            while True:
                current_ids = []
                customer_id = str(random.randint(300000, 400000))
                ids_query = database_operation('SELECT `id` FROM `customer`')
                for id_query in ids_query:
                    current_ids.append(id_query)

                if customer_id in current_ids:
                    continue

                else:
                    break

            sale_id = f"{car_id_sale[-2]}{customer_id[-2]}{salesperson_id_sale[-2]}"

            sale_status = True

            if sale_status:
                database_operation(f'INSERT INTO `customer` VALUES '
                                   f'("{customer_id}", "{customer_name_sale}", "{customer_phone_sale}");')

                time.sleep(1)

                database_operation(f'INSERT INTO `sale` VALUES '
                                   f'("{sale_id}", "{car_id_sale}", "{salesperson_id_sale}", "{customer_id}", '
                                   f'{final_price_amount.get()}, {formatted_date});')

                root.update()

                popup = Toplevel(root)

                root.geometry('25x50')

                sale_confirmed_label = Label(popup, text='Sale Confirmed!')

                def destroy_gui():
                    popup.destroy()

                ok_button = Button(popup, text='Ok', command=lambda: destroy_gui())

                sale_confirmed_label.pack()
                ok_button.pack()

        car_label_frame = LabelFrame(root, text='Car')
        customer_label_frame = LabelFrame(root, text='Customer')
        salesperson_label_frame = LabelFrame(root, text='Salesperson')
        sale_label_frame = LabelFrame(root, text='Sale')

        customer_name_label = Label(customer_label_frame, text='Name')
        customer_phone_label = Label(customer_label_frame, text='Phone')

        car_id_label = Label(car_label_frame, text='ID')

        salesperson_id_label = Label(salesperson_label_frame, text='ID')

        car_model_label = Label(sale_label_frame, text='Model')
        car_model = Entry(sale_label_frame, justify='center')
        car_model.config(state='disabled')

        final_price_label = Label(sale_label_frame, text='Final Price')
        final_price_amount = Entry(sale_label_frame, justify='center')
        final_price_amount.config(state='disabled')

        number_of_payment_label = Label(sale_label_frame, text='No. of Payments')
        number_of_payments = Entry(sale_label_frame, justify='center')

        car_id_entry = Entry(car_label_frame)
        salesperson_id_entry = Entry(salesperson_label_frame)

        customer_name_entry = Entry(customer_label_frame)
        customer_phone_entry = Entry(customer_label_frame)

        confirm_button = Button(root, text='Confirm', width=10, height=2, command=lambda: confirm_sale())

        car_label_frame.grid(row=0, column=0, padx=20, pady=30)
        car_id_label.grid(row=1, column=0, padx=5, pady=20)
        car_id_entry.grid(row=1, column=2, padx=10, pady=20)

        salesperson_label_frame.grid(row=0, column=3, padx=20, pady=30)
        salesperson_id_label.grid(row=1, column=3, padx=5, pady=20)
        salesperson_id_entry.grid(row=1, column=5, padx=10, pady=20)

        customer_label_frame.grid(row=2, column=0, padx=30, pady=30)
        customer_name_label.grid(row=3, column=0, padx=5, pady=20)
        customer_name_entry.grid(row=3, column=2, padx=10, pady=20)
        customer_phone_label.grid(row=4, column=0, padx=5, pady=20)
        customer_phone_entry.grid(row=4, column=2, padx=10, pady=20)

        sale_label_frame.grid(row=2, column=3, padx=30, pady=30)
        car_model_label.grid(row=3, column=3, padx=5, pady=10)
        car_model.grid(row=3, column=5, padx=5, pady=10)
        final_price_label.grid(row=4, column=3, padx=5, pady=10)
        final_price_amount.grid(row=4, column=5, padx=10, pady=10)
        number_of_payment_label.grid(row=5, column=3, padx=5, pady=10)
        number_of_payments.grid(row=5, column=5, padx=10, pady=10)

        confirm_button.grid(row=6, column=3)

    def payment_analysis_operation():
        global root
        root.destroy()

        def get_payments(interval):
            for result in tree.get_children():
                tree.delete(result)

            results = None
            today = datetime.date.today()
            formatted_date = today.strftime('%Y-%m-%d')

            if interval == 'today':
                results = database_operation(f'''
                                                SELECT * FROM payment
                                                WHERE STR_TO_DATE(duedate, '%Y-%m-%d') 
                                                BETWEEN STR_TO_DATE('{formatted_date}', '%Y-%m-%d') 
                                                AND DATE_ADD(STR_TO_DATE('{formatted_date}', '%Y-%m-%d'), 
                                                INTERVAL 1 DAY);
                                            ''')

            elif interval == 'week':
                results = database_operation(f'''
                                                SELECT * FROM payment
                                                WHERE STR_TO_DATE(duedate, '%Y-%m-%d') 
                                                BETWEEN STR_TO_DATE('{formatted_date}', '%Y-%m-%d') 
                                                AND DATE_ADD(STR_TO_DATE('{formatted_date}', '%Y-%m-%d'), 
                                                INTERVAL 7 DAY);
                                            ''')

            elif interval == 'month':
                results = database_operation(f'''
                                                SELECT * FROM payment
                                                WHERE STR_TO_DATE(duedate, '%Y-%m-%d') 
                                                BETWEEN STR_TO_DATE('{formatted_date}', '%Y-%m-%d') 
                                                AND DATE_ADD(STR_TO_DATE('{formatted_date}', '%Y-%m-%d'), 
                                                INTERVAL 30 DAY);
                                            ''')

            for result in results:
                tree.insert('', 'end', values=result)

        root = Tk()

        root.geometry('1000x300')
        root.title('Due Payments System')

        day_range = Button(root, text='Today', command=lambda: get_payments('today'))
        week_range = Button(root, text='This Week', command=lambda: get_payments('week'))
        month_range = Button(root, text='This Month', command=lambda: get_payments('month'))

        columns = ('id', 'amount', 'method', 'date', 'due_date')

        tree = ttk.Treeview(root, column=columns, show='headings')
        tree.column("id", width=75, anchor=CENTER)
        tree.heading("id", text="ID")
        tree.column("amount", width=150, anchor=CENTER)
        tree.heading("amount", text="Amount")
        tree.column("method", width=150, anchor=CENTER)
        tree.heading("method", text="Method")
        tree.column("date", width=75, anchor=CENTER)
        tree.heading("date", text="Date")
        tree.column("due_date", width=150, anchor=CENTER)
        tree.heading("due_date", text="Due Date")

        day_range.place(x=70, y=50, width=180, height=40)
        week_range.place(x=70, y=50 + 70, width=180, height=40)
        month_range.place(x=70, y=50 + 140, width=180, height=40)

        tree.place(x=330, y=50, height=180)
    root = Tk()
    root.geometry('300x325')
    root.title('Dealership Main Operations')

    filter_system_button = Button(root, text='Filtration', command= lambda: filter_operation())

    sale_system_button = Button(root, text='Sale Generation', command= lambda: sell_operation())

    due_payment_system_button = Button(root, text='Due Payments', command= lambda: payment_analysis_operation())

    filter_system_button.place(x=20, y=50, width=250, height=50)
    sale_system_button.place(x=20, y=125, width=250, height=50)
    due_payment_system_button.place(x=20, y=200, width=250, height=50)


def display_operation():
    global root
    root.destroy()

    cols = list()
    records = tuple()
    tree = None

    def display_table():
        nonlocal cols, records, tree

        try:
            tree["columns"] = ()
            tree.delete(*tree.get_children())

        except TypeError:
            pass

        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='28o12o2002',
            db='car_dealership',
        )
        with connection:
            with connection.cursor() as cursor:
                get_columns_query = f"SHOW COLUMNS FROM car_dealership.{table_var.get()}"
                cursor.execute(get_columns_query)
                table_cols_tuples = cursor.fetchall()
                cols = [x[0] for x in table_cols_tuples]

                get_table_data_query = f"SELECT * FROM `{table_var.get()}`"
                cursor.execute(get_table_data_query)
                records = cursor.fetchall()

                tree = ttk.Treeview(root, column=cols, show='headings')

                for result in records:
                    tree.insert('', 'end', values=result)

                for col in cols:
                    tree.column(f"{col}", width=100, anchor=CENTER)
                    tree.heading(f"{col}", text=f"{col.upper()}")

                tree.place(x=330, y=50, height=500)

    root = Tk()
    root.geometry('1000x700')
    root.title('Dealership Display System')

    table_var = StringVar(root, "car")

    welcome_label = Label(root, text=f'Welcome {salesperson_name}!')

    car_radio = Radiobutton(root, text='Car Table', value='car', variable=table_var)

    customer_radio = Radiobutton(root, text='Customer Table', value='customer', variable=table_var)

    salesperson_radio = Radiobutton(root, text='Salesperson Table', value='salesperson', variable=table_var)

    sale_radio = Radiobutton(root, text='Sale Table', value='sale', variable=table_var)

    payment_radio = Radiobutton(root, text='Payment Table', value='payment', variable=table_var)

    display_table_button = Button(root, text='Display', command=lambda: display_table())

    welcome_label.place(x=880, y=670)

    car_radio.place(x=25, y=98)

    customer_radio.place(x=24, y=98 + 40)

    salesperson_radio.place(x=23, y=98 + 80)

    sale_radio.place(x=24, y=98 + 120)

    payment_radio.place(x=24, y=98 + 160)

    display_table_button.place(x=70, y=100 + 225, width=180, height=40)


def update_operation():
    global root

    root.destroy()
    car_id_entry = None
    car_brand_entry = None
    car_model_entry = None
    car_price_entry = None
    car_year_entry = None
    customer_id_entry = None
    customer_name_entry = None
    customer_phone_entry = None
    salesperson_id_entry = None
    salesperson_name_entry = None
    salesperson_password_entry = None
    sale_id_entry = None
    date_entry = None
    final_price_entry = None
    payment_id_entry = None
    payment_amount_entry = None
    payment_method_entry = None
    payment_due_date_entry = None
    payment_date_entry = None

    def update_func(table_insert):
        data_tuple = tuple()
        if table_insert == 'car':
            data_tuple = (car_id_entry.get(), car_brand_entry.get(), car_model_entry.get(), car_year_entry.get(),
                          car_price_entry.get())

            database_operation(f"UPDATE {table_insert} SET `brand`='{data_tuple[1]}',"
                               f"`model`='{data_tuple[2]}', `year`='{data_tuple[3]}',`price`= {data_tuple[4]} "
                               f"WHERE `id`='{data_tuple[0]}';")

        if table_insert == 'customer':
            data_tuple = (customer_id_entry.get(), customer_name_entry.get(), customer_phone_entry.get())
            database_operation(f"UPDATE {table_insert} SET `name`='{data_tuple[1]}',"
                               f"`phone`='{data_tuple[2]}' "
                               f"WHERE `id`='{data_tuple[0]}';")

        if table_insert == 'salesperson':
            data_tuple = (salesperson_id_entry.get(), salesperson_name_entry.get(), salesperson_password_entry.get())
            database_operation(f"UPDATE {table_insert} SET `name`='{data_tuple[1]}',"
                               f"`password`='{data_tuple[2]}' "
                               f"WHERE `id`='{data_tuple[0]}';")

        if table_insert == 'sale':
            data_tuple = (sale_id_entry.get(), final_price_entry.get(), date_entry.get())
            database_operation(f"UPDATE {table_insert} SET `finalprice`={data_tuple[1]},"
                               f"`date`='{data_tuple[2]}' "
                               f"WHERE `id`='{data_tuple[0]}';")

        elif table_insert == 'sale':
            data_tuple = (payment_id_entry.get(), payment_amount_entry.get(), payment_method_entry.get(),
                          payment_date_entry.get(), payment_due_date_entry.get())

            database_operation(f"UPDATE {table_insert} SET `amount`={data_tuple[1]},"
                               f"`method`='{data_tuple[2]}', `paymentdate`='{data_tuple[3]}',`duedate`= '{data_tuple[4]}' "
                               f"WHERE `id`='{data_tuple[0]}';")

    def car_update():
        nonlocal car_id_entry, car_brand_entry, car_model_entry, car_year_entry, car_price_entry

        global root
        root.destroy()

        root = Tk()
        root.geometry('550x100')

        root.title('Car Insertion')

        car_id_label = Label(root, text='ID')
        car_id_entry = Entry(root)

        car_brand_label = Label(root, text='Brand')
        car_brand_entry = Entry(root)

        car_model_label = Label(root, text='Model')
        car_model_entry = Entry(root)

        car_year_label = Label(root, text='Year')
        car_year_entry = Entry(root)

        car_price_label = Label(root, text='Price')
        car_price_entry = Entry()

        insert_record_button = Button(root, text='Insert', command=lambda: update_func('car'))

        car_id_label.place(x=20, y=10)
        car_id_entry.place(x=20, y=30, width=70)

        car_brand_label.place(x=110, y=10)
        car_brand_entry.place(x=110, y=30, width=100)

        car_model_label.place(x=230, y=10)
        car_model_entry.place(x=230, y=30, width=85)

        car_year_label.place(x=330, y=10)
        car_year_entry.place(x=330, y=30, width=50)

        car_price_label.place(x=400, y=10)
        car_price_entry.place(x=400, y=30, width=70)

        insert_record_button.place(x=480, y=60, width=50, height=30)

        root.mainloop()

    def customer_update():
        nonlocal customer_id_entry, customer_name_entry, customer_phone_entry
        global root
        root.destroy()

        root = Tk()
        root.geometry('400x100')

        root.title('Customer Insertion')

        customer_id_label = Label(root, text='ID')
        customer_id_entry = Entry(root)

        customer_name_label = Label(root, text='Name')
        customer_name_entry = Entry(root)

        customer_phone_label = Label(root, text='Phone')
        customer_phone_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: update_func('customer'))

        customer_id_label.place(x=20, y=10)
        customer_id_entry.place(x=20, y=30, width=70)

        customer_name_label.place(x=110, y=10)
        customer_name_entry.place(x=110, y=30, width=100)

        customer_phone_label.place(x=230, y=10)
        customer_phone_entry.place(x=230, y=30, width=85)

        insert_record_button.place(x=325, y=60, width=50, height=30)

        root.mainloop()

    def salesperson_update():
        global root
        nonlocal salesperson_id_entry, salesperson_name_entry, salesperson_password_entry
        root.destroy()

        root = Tk()
        root.geometry('400x100')

        root.title('Salesperson Insertion')

        salesperson_id_label = Label(root, text='ID')
        salesperson_id_entry = Entry(root)

        salesperson_name_label = Label(root, text='Name')
        salesperson_name_entry = Entry(root)

        salesperson_password_label = Label(root, text='Password')
        salesperson_password_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: update_func('salesperson'))

        salesperson_id_label.place(x=20, y=10)
        salesperson_id_entry.place(x=20, y=30, width=70)

        salesperson_name_label.place(x=110, y=10)
        salesperson_name_entry.place(x=110, y=30, width=100)

        salesperson_password_label.place(x=230, y=10)
        salesperson_password_entry.place(x=230, y=30, width=85)

        insert_record_button.place(x=325, y=60, width=50, height=30)

        root.mainloop()

    def sale_update():
        nonlocal sale_id_entry, final_price_entry, date_entry

        global root
        root.destroy()

        root = Tk()
        root.geometry('320x100')

        sale_id_label = Label(root, text='ID')
        sale_id_entry = Entry(root)

        root.title('Sale Insertion')

        final_price_label = Label(root, text='Final Price')
        final_price_entry = Entry(root)

        date_label = Label(root, text='Date')
        date_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: update_func('sale'))

        sale_id_label.place(x=20, y=10)
        sale_id_entry.place(x=20, y=30, width=70)

        final_price_label.place(x=110, y=10)
        final_price_entry.place(x=110, y=30, width=85)

        date_label.place(x=210, y=10)
        date_entry.place(x=210, y=30, width=85)

        insert_record_button.place(x=205, y=60, width=50, height=30)

        root.mainloop()

    def payment_update():
        nonlocal payment_id_entry, payment_amount_entry, payment_method_entry, payment_date_entry, payment_due_date_entry
        global root
        root.destroy()

        root = Tk()
        root.geometry('575x100')

        root.title('Payment Insertion')

        payment_id_label = Label(root, text='ID')
        payment_id_entry = Entry(root)

        payment_amount_label = Label(root, text='Amount')
        payment_amount_entry = Entry(root)

        payment_method_label = Label(root, text='Method')
        payment_method_entry = Entry(root)

        payment_date_label = Label(root, text='Date')
        payment_date_entry = Entry(root)

        payment_due_date_label = Label(root, text='Due Date')
        payment_due_date_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: update_func('payment'))

        payment_id_label.place(x=20, y=10)
        payment_id_entry.place(x=20, y=30, width=70)

        payment_amount_label.place(x=110, y=10)
        payment_amount_entry.place(x=110, y=30, width=100)

        payment_method_label.place(x=230, y=10)
        payment_method_entry.place(x=230, y=30, width=100)

        payment_date_label.place(x=350, y=10)
        payment_date_entry.place(x=350, y=30, width=85)

        payment_due_date_label.place(x=455, y=10)
        payment_due_date_entry.place(x=455, y=30, width=85)

        insert_record_button.place(x=430, y=60, width=50, height=30)

    root = Tk()
    root.geometry('300x450')

    root.title('Table Update System')

    car_button = Button(root, text='Car Table', command=lambda: car_update())

    customer_button = Button(root, text='Customer Table', command=lambda: customer_update())

    salesperson_button = Button(root, text='Salesperson Table', command=lambda: salesperson_update())

    sale_button = Button(root, text='Sale Table', command=lambda: sale_update())

    payment_button = Button(root, text='Payment Table', command=lambda: payment_update())

    car_button.place(x=20, y=50, width=250, height=50)
    customer_button.place(x=20, y=125, width=250, height=50)
    salesperson_button.place(x=20, y=200, width=250, height=50)
    sale_button.place(x=20, y=275, width=250, height=50)
    payment_button.place(x=20, y=350, width=250, height=50)


def delete_operation():
    global root
    root.destroy()

    def delete_func(table_name):
        def destroy_gui():
            popup.destroy()

        database_operation('SET FOREIGN_KEY_CHECKS=0;')

        id_to_delete = id_entry.get()
        database_operation(f'DELETE FROM `{table_name}` WHERE `id`="{id_to_delete}"')

        popup = Toplevel(root)

        popup.geometry('25x50')

        confirm_label = Label(popup, text='Deleted!')
        ok_button = Button(popup, text='OK', command=lambda: destroy_gui())

        confirm_label.grid(row=0, column=2)
        ok_button.grid(row=1, column=2)

        database_operation('SET FOREIGN_KEY_CHECKS=1;')

    root = Tk()
    root.geometry('300x250')
    root.title('Dealership Deletion System')

    table_var = StringVar(root, "car")

    car_radio = Radiobutton(root, text='Car Table', value='car', variable=table_var)
    customer_radio = Radiobutton(root, text='Customer Table', value='customer', variable=table_var)
    salesperson_radio = Radiobutton(root, text='Salesperson Table', value='salesperson', variable=table_var)
    sale_radio = Radiobutton(root, text='Sale Table', value='sale', variable=table_var)

    id_label = Label(root, text='ID')
    id_entry = Entry(root)

    delete_record_button = Button(root, text='Delete', command=lambda: delete_func(table_var.get()))

    car_radio.place(x=20, y=20)
    customer_radio.place(x=20, y=50)
    salesperson_radio.place(x=20, y=80)
    sale_radio.place(x=20, y=110)

    id_label.place(x=60, y=159)
    id_entry.place(x=90, y=159)

    delete_record_button.place(x=115, y=200, width=65, height=30)


def insert_operation():
    global root
    root.destroy()

    car_id_entry                           = None
    car_brand_entry                        = None
    car_model_entry                        = None
    car_price_entry                        = None
    car_year_entry                         = None
    customer_id_entry                      = None
    customer_name_entry                    = None
    customer_phone_entry                   = None
    salesperson_id_entry                   = None
    salesperson_name_entry                 = None
    salesperson_password_entry             = None
    sale_id_entry                          = None
    date_entry                             = None
    final_price_entry                      = None
    payment_id_entry                       = None
    payment_amount_entry                   = None
    payment_method_entry                   = None
    payment_due_date_entry                 = None
    payment_date_entry                     = None

    def car_insert():
        nonlocal car_id_entry, car_brand_entry, car_model_entry, car_year_entry, car_price_entry

        global root
        root.destroy()

        root = Tk()
        root.geometry('550x100')

        root.title('Car Insertion')

        car_id_label = Label(root, text='ID')
        car_id_entry = Entry(root)

        car_brand_label = Label(root, text='Brand')
        car_brand_entry = Entry(root)

        car_model_label = Label(root, text='Model')
        car_model_entry = Entry(root)

        car_year_label = Label(root, text='Year')
        car_year_entry = Entry(root)

        car_price_label = Label(root, text='Price')
        car_price_entry = Entry()

        insert_record_button = Button(root, text='Insert', command=lambda: insert_func('car'))

        car_id_label.place(x=20, y=10)
        car_id_entry.place(x=20, y=30, width=70)

        car_brand_label.place(x=110, y=10)
        car_brand_entry.place(x=110, y=30, width=100)

        car_model_label.place(x=230, y=10)
        car_model_entry.place(x=230, y=30, width=85)

        car_year_label.place(x=330, y=10)
        car_year_entry.place(x=330, y=30, width=50)

        car_price_label.place(x=400, y=10)
        car_price_entry.place(x=400, y=30, width=70)

        insert_record_button.place(x=480, y=60, width=50, height=30)

        root.mainloop()

    def customer_insert():
        nonlocal customer_id_entry, customer_name_entry, customer_phone_entry
        global root
        root.destroy()

        root = Tk()
        root.geometry('400x100')

        root.title('Customer Insertion')

        customer_id_label = Label(root, text='ID')
        customer_id_entry = Entry(root)

        customer_name_label = Label(root, text='Name')
        customer_name_entry = Entry(root)

        customer_phone_label = Label(root, text='Phone')
        customer_phone_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: insert_func('customer'))

        customer_id_label.place(x=20, y=10)
        customer_id_entry.place(x=20, y=30, width=70)

        customer_name_label.place(x=110, y=10)
        customer_name_entry.place(x=110, y=30, width=100)

        customer_phone_label.place(x=230, y=10)
        customer_phone_entry.place(x=230, y=30, width=85)

        insert_record_button.place(x=325, y=60, width=50, height=30)

        root.mainloop()

    def salesperson_insert():
        global root
        nonlocal salesperson_id_entry, salesperson_name_entry, salesperson_password_entry
        root.destroy()

        root = Tk()
        root.geometry('400x100')

        root.title('Salesperson Insertion')

        salesperson_id_label = Label(root, text='ID')
        salesperson_id_entry = Entry(root)

        salesperson_name_label = Label(root, text='Name')
        salesperson_name_entry = Entry(root)

        salesperson_password_label = Label(root, text='Password')
        salesperson_password_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: insert_func('salesperson'))

        salesperson_id_label.place(x=20, y=10)
        salesperson_id_entry.place(x=20, y=30, width=70)

        salesperson_name_label.place(x=110, y=10)
        salesperson_name_entry.place(x=110, y=30, width=100)

        salesperson_password_label.place(x=230, y=10)
        salesperson_password_entry.place(x=230, y=30, width=85)

        insert_record_button.place(x=325, y=60, width=50, height=30)

        root.mainloop()

    def sale_insert():
        nonlocal sale_id_entry, final_price_entry, date_entry

        global root
        root.destroy()

        root = Tk()
        root.geometry('320x100')

        sale_id_label = Label(root, text='ID')
        sale_id_entry = Entry(root)

        root.title('Sale Insertion')

        final_price_label = Label(root, text='Final Price')
        final_price_entry = Entry(root)

        date_label = Label(root, text='Date')
        date_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: insert_func('sale'))

        sale_id_label.place(x=20, y=10)
        sale_id_entry.place(x=20, y=30, width=70)

        final_price_label.place(x=110, y=10)
        final_price_entry.place(x=110, y=30, width=85)

        date_label.place(x=210, y=10)
        date_entry.place(x=210, y=30, width=85)

        insert_record_button.place(x=205, y=60, width=50, height=30)

        root.mainloop()

    def payment_insert():
        nonlocal payment_id_entry, payment_amount_entry, payment_method_entry, payment_date_entry, payment_due_date_entry
        global root
        root.destroy()

        root = Tk()
        root.geometry('575x100')

        root.title('Payment Insertion')

        payment_id_label = Label(root, text='ID')
        payment_id_entry = Entry(root)

        payment_amount_label = Label(root, text='Amount')
        payment_amount_entry = Entry(root)

        payment_method_label = Label(root, text='Method')
        payment_method_entry = Entry(root)

        payment_date_label = Label(root, text='Date')
        payment_date_entry = Entry(root)

        payment_due_date_label = Label(root, text='Due Date')
        payment_due_date_entry = Entry(root)

        insert_record_button = Button(root, text='Insert', command=lambda: insert_func('payment'))

        payment_id_label.place(x=20, y=10)
        payment_id_entry.place(x=20, y=30, width=70)

        payment_amount_label.place(x=110, y=10)
        payment_amount_entry.place(x=110, y=30, width=100)

        payment_method_label.place(x=230, y=10)
        payment_method_entry.place(x=230, y=30, width=100)

        payment_date_label.place(x=350, y=10)
        payment_date_entry.place(x=350, y=30, width=85)

        payment_due_date_label.place(x=455, y=10)
        payment_due_date_entry.place(x=455, y=30, width=85)

        insert_record_button.place(x=430, y=60, width=50, height=30)

    def insert_func(table_insert):
        data_tuple = tuple()
        if table_insert == 'car':
            data_tuple = (car_id_entry.get(), car_brand_entry.get(), car_model_entry.get(), car_year_entry.get(),
                          car_price_entry.get())

            database_operation(f"INSERT INTO {table_insert} VALUES ('{data_tuple[0]}', '{data_tuple[1]}',"
                               f"'{data_tuple[2]}', '{data_tuple[3]}', {data_tuple[4]});")

        if table_insert == 'customer':
            data_tuple = (customer_id_entry.get(), customer_name_entry.get(), customer_phone_entry.get())
            database_operation(f"INSERT INTO {table_insert} VALUES ('{data_tuple[0]}', '{data_tuple[1]}',"
                               f"'{data_tuple[2]}');")

        if table_insert == 'salesperson':
            data_tuple = (salesperson_id_entry.get(), salesperson_name_entry.get(), salesperson_password_entry.get())
            database_operation(f"INSERT INTO {table_insert} VALUES ('{data_tuple[0]}', '{data_tuple[1]}',"
                               f"'{data_tuple[2]}');")

        if table_insert == 'sale':
            data_tuple = (sale_id_entry.get(), final_price_entry.get(), date_entry.get())
            database_operation(f"INSERT INTO {table_insert} VALUES ('{data_tuple[0]}', {data_tuple[1]},"
                               f"'{data_tuple[2]}');")

        elif table_insert == 'sale':
            data_tuple = (payment_id_entry.get(), payment_amount_entry.get(), payment_method_entry.get(),
                          payment_date_entry.get(),  payment_due_date_entry.get())
            database_operation(f"INSERT INTO {table_insert} VALUES ('{data_tuple[0]}', {data_tuple[1]},"
                               f"'{data_tuple[2]}', '{data_tuple[3]}', '{data_tuple[4]}');")

    root = Tk()
    root.geometry('300x450')

    root.title('Table Insertion System')

    car_button = Button(root, text='Car Table', command=lambda: car_insert())

    customer_button = Button(root, text='Customer Table', command=lambda: customer_insert())

    salesperson_button = Button(root, text='Salesperson Table', command=lambda: salesperson_insert())

    sale_button = Button(root, text='Sale Table', command=lambda: sale_insert())

    payment_button = Button(root, text='Payment Table', command=lambda: payment_insert())

    car_button.place(x=20, y=50, width=250, height=50)
    customer_button.place(x=20, y=125, width=250, height=50)
    salesperson_button.place(x=20, y=200, width=250, height=50)
    sale_button.place(x=20, y=275, width=250, height=50)
    payment_button.place(x=20, y=350, width=250, height=50)


def show_queries():
    global root
    root.destroy()

    root = Tk()
    root.geometry('1050x350')
    root.title('Queries Showcase')

    results = None

    def request_from_database(num):
        nonlocal results

        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='28o12o2002',
            db='car_dealership',
        )

        with connection:
            with connection.cursor() as cursor:
                if num == 1:
                    cursor.execute('''
                        SELECT c.name, c.phone, car.brand, car.model, s.finalprice
                        FROM car_dealership.customer c
                        JOIN car_dealership.sale s ON c.id = s.customerid
                        JOIN car_dealership.car car ON s.carid = car.id
                        JOIN car_dealership.payment p ON s.id = p.saleid
                        WHERE s.finalprice > 500000;
                    ''')

                elif num == 2:
                    cursor.execute('''
                        SELECT s.name AS salesperson_name, COUNT(*) AS total_cars_sold
                        FROM car_dealership.sale sale
                        JOIN car_dealership.salesperson s ON s.id = sale.salespersonid
                        JOIN car_dealership.car c ON c.id = sale.carid
                        WHERE c.brand = 'Skoda'
                        GROUP BY sale.salespersonid;
                    ''')

                elif num == 3:
                    cursor.execute('''
                        SELECT salesperson.name, COUNT(*) AS num_sales
                        FROM sale
                        JOIN salesperson ON sale.salespersonid = salesperson.id
                        WHERE salesperson.name = 'Ahmed'
                        GROUP BY salesperson.name;
                    ''')

                elif num == 4:
                    cursor.execute('''
                        SELECT SUM(revenue) AS total_revenue
                        FROM (
                          SELECT s.salespersonid, SUM(s.finalprice) AS revenue
                          FROM sale s
                          JOIN payment p ON s.id = p.saleid
                          JOIN car c ON s.carid = c.id
                          GROUP BY s.salespersonid
                        ) AS salesperson_profits;
                    ''')

                elif num == 5:
                    cursor.execute('''
                        SELECT * FROM car
                        WHERE year = 2018;
                    ''')

                elif num == 6:
                    cursor.execute('''
                        SELECT c.id AS car_id, c.model AS car_model,
                        cust.name AS customer_name
                        FROM car_dealership.car c
                        JOIN car_dealership.sale s ON c.id = s.carid
                        JOIN car_dealership.customer cust ON
                        s.customerid = cust.id
                        GROUP BY c.model, cust.name;
                    ''')

                elif num == 7:
                    cursor.execute('''
                        SELECT c.model, c.id, s.id AS
                        salesperson_id
                        FROM car_dealership.sale sa
                        JOIN car_dealership.salesperson s ON
                        sa.salespersonid = s.id
                        JOIN car_dealership.car c ON sa.carid =
                        c.id
                        JOIN car_dealership.payment p ON sa.id
                        = p.id
                        WHERE p.finalprice > 500000
                        GROUP BY c.model, c.id, s.id;
                    ''')

                elif num == 8:
                    cursor.execute('''
                        SELECT c.name, c.phone 
                        FROM customer c 
                        JOIN sale s ON c.id = s.customerid 
                        JOIN payment p ON p.saleid = s.id
                        JOIN car car ON s.carid = car.id 
                        WHERE s.finalprice > 500000 OR car.brand = 'Toyota';
                    ''')

                elif num == 9:
                    cursor.execute('''
                        SELECT customer.name
                        FROM customer
                        LEFT JOIN sale ON customer.id = sale.customerid
                        WHERE sale.customerid IS NULL;
                    ''')

                elif num == 10:
                    cursor.execute('''
                        SELECT name
                        FROM customer
                        WHERE id IN (
                          SELECT customerid
                          FROM sale
                          WHERE salespersonid = '202001'
                        );
                    ''')

                elif num == 11:
                    cursor.execute('''
                        CREATE DEFINER=CURRENT_USER TRIGGER `sale_AFTER_INSERT` AFTER INSERT ON `sale` FOR EACH ROW BEGIN
                          IF NEW.finalprice < 30000 THEN
                         
                            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Final price is less than 30,000';
                          END IF;
                        END
                    ''')

                results = cursor.fetchall()
                popup = Toplevel(root)

                popup.geometry('850x150')
                popup.title('Query Execution')

                Label(popup, text=str(results), font=('Calibri 13 bold')).pack()

    require_from_2_table_frame = LabelFrame(root, text='Require Data from 1+ Tables Queries')
    require_from_2_table_1 = Button(require_from_2_table_frame, text='Customer of Sale > 500,000',
                                    command=lambda: request_from_database(1))
    require_from_2_table_2 = Button(require_from_2_table_frame, text='Count Skoda Sales -> Salesperson Name',
                                    command=lambda: request_from_database(2))

    calculate_frame = LabelFrame(root, text='Calculating Queries')
    calculate_query_1 = Button(calculate_frame, text='Count of Sales by Ahmed',
                               command=lambda: request_from_database(3))
    calculate_query_2 = Button(calculate_frame, text='Total Revenue',
                               command=lambda: request_from_database(4))

    pattern_frame = LabelFrame(root, text='Pattern Query')
    pattern_search = Button(pattern_frame, text='Cars Year == 2018',
                            command=lambda: request_from_database(5))

    aggregate_frame = LabelFrame(root, text='Aggregating Queries')
    aggregating_1 = Button(aggregate_frame, text='Sales Count for Brand & Model',
                           command=lambda: request_from_database(6))
    aggregating_2 = Button(aggregate_frame, text='Salesperson of Sale > 500,000',
                           command=lambda: request_from_database(7))

    union_frame = LabelFrame(root, text='Union Queries')
    union_query = Button(union_frame, text='Customers Bought Toyota OR Sale > 500,000',
                         command=lambda: request_from_database(8))

    data_unavailability_frame = LabelFrame(root, text='Data Unavailability Query')
    data_unavailability = Button(data_unavailability_frame, text='Data Unavailability',
                                 command=lambda: request_from_database(9))

    nested_frame = LabelFrame(root, text='Nested Query')
    nested = Button(nested_frame, text='Nested',
                    command=lambda: request_from_database(10))

    trigger_frame = LabelFrame(root, text='Trigger Query')
    trigger = Button(trigger_frame, text='Trigger',
                     command=lambda: request_from_database(11))

    require_from_2_table_frame.grid(row=0, column=0, padx=30, pady=10)
    require_from_2_table_1.grid(row=1, column=1, padx=10, pady=10, ipadx=30)
    require_from_2_table_2.grid(row=1, column=2, padx=10, pady=10, ipadx=30)

    pattern_frame.grid(row=0, column=3, padx=15, pady=10)
    pattern_search.grid(row=1, column=4, padx=10, pady=10, ipadx=30)

    calculate_frame.grid(row=1, column=0, padx=15, pady=10)
    calculate_query_1.grid(row=2, column=1, padx=10, pady=10, ipadx=30)
    calculate_query_2.grid(row=2, column=2, padx=10, pady=10, ipadx=30)

    aggregate_frame.grid(row=2, column=0, padx=15, pady=10)
    aggregating_1.grid(row=3, column=1, padx=10, pady=10, ipadx=30)
    aggregating_2.grid(row=3, column=2, padx=10, pady=10, ipadx=30)

    union_frame.grid(row=1, column=3, padx=15, pady=10)
    union_query.grid(row=2, column=4, padx=10, pady=10, ipadx=30)

    data_unavailability_frame.grid(row=2, column=3, padx=15, pady=10)
    data_unavailability.grid(row=3, column=4, padx=10, pady=10, ipadx=30)

    nested_frame.grid(row=3, column=0, padx=15, pady=10)
    nested.grid(row=4, column=1, padx=10, pady=10, ipadx=30)

    trigger_frame.grid(row=3, column=3, padx=15, pady=10)
    trigger.grid(row=4, column=4, padx=10, pady=10, ipadx=30)


root = Tk()
root.geometry('450x250')
root.title('Dealership Database Management System')

main_page_label = Label(root, text='Main Page', font=14)
insert_button = Button(root, text='Insert Record', command=lambda: insert_operation())
display_button = Button(root, text='Display Tables', command=lambda: display_operation())
update_button = Button(root, text='Update Record', command=lambda: update_operation())
delete_button = Button(root, text='Delete Record', command=lambda: delete_operation())
main_button = Button(root, text='Main', command=lambda: main_operations())
query_button = Button(root, text='Queries', command=lambda: show_queries())


main_page_label.place(x=185, y=10)
insert_button.place(x=250, y=50, width=180, height=40)
update_button.place(x=20, y=110, width=180, height=40)
display_button.place(x=250, y=110, width=180, height=40)
delete_button.place(x=20, y=170, width=180, height=40)
main_button.place(x=20, y=50, width=180, height=40)
query_button.place(x=250, y=170, width=180, height=40)

root.mainloop()
