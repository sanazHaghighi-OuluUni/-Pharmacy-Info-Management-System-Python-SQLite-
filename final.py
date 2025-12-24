from tkinter import *
from tkinter import ttk
import jdatetime 
import datetime
import time
import sqlite3
from tkinter import messagebox

win=Tk()
win.title("Pharmacy Info")
win.geometry("610x600")

# نمایش زمان حال
lb_time=Label(win,text="0",font=("Tahoma",10))
lb_time.place(x=10,y=10)

def showtime():
    t=datetime.datetime.now().strftime("%c")
    lb_time.config(text=t)
    lb_time.after(1000,showtime)
    
showtime()

# لیبل ها

text1=Label(win,text="نام دارو",font=("B titr",12))
text1.place(x=520,y=40)

en_drug=Entry(win,font=("B titr",10),width=30)
en_drug.place(x=320,y=40)

text2=Label(win,text="دوز دارو",font=("B titr",12))
text2.place(x=520,y=80)

en_doses=Entry(win,font=("B titr",10),width=30)
en_doses.place(x=320,y=80)

text3=Label(win,text="تعداد",font=("B titr",12))
text3.place(x=520,y=120)

combo_numbers=ttk.Combobox(win,values=list(range(1,1001)),font=("B titr",10),state="readonly")
combo_numbers.place(x=320,y=120)

text4=Label(win,text="شرکت سازنده ",font=("B titr",12),justify=CENTER)
text4.place(x=520,y=160)

en_company=Entry(win,font=("B titr",10),width=30)
en_company.place(x=320,y=160)

text5=Label(win,text="تاریخ انقضا ",font=("B titr",12))
text5.place(x=520,y=200)

# قسمت تعیین تاریخ انقضا به شمسی

expire_var = StringVar()
en_expire = Entry(win, textvariable=expire_var, font=("B titr", 10), width=30, state="readonly")
en_expire.place(x=320, y=200)

def open_calendar():
    top = Toplevel(win)
    top.title("انتخاب تاریخ انقضا")
    top.geometry("250x150")

    year_var = StringVar(value="1404")
    month_var = StringVar(value="1")
    day_var = StringVar(value="1")

    ttk.Label(top, text="روز").grid(row=0, column=0)
    ttk.Combobox(top, textvariable=day_var, values=[str(i) for i in range(1, 32)], width=5).grid(row=1, column=0)

    ttk.Label(top, text="ماه").grid(row=0, column=1)
    ttk.Combobox(top, textvariable=month_var, values=[str(i) for i in range(1, 13)], width=5).grid(row=1, column=1)

    ttk.Label(top, text="سال").grid(row=0, column=2)
    ttk.Combobox(top, textvariable=year_var, values=[str(i) for i in range(1404, 1415)], width=7).grid(row=1, column=2)

    def set_date():
        try:
            d = jdatetime.date(int(year_var.get()), int(month_var.get()), int(day_var.get()))
            expire_var.set(d.strftime("%Y/%m/%d"))
            top.destroy()
        except:
            expire_var.set("تاریخ نامعتبر")

    Button(top, text="تأیید", command=set_date).grid(row=2, column=0, columnspan=3, pady=10)

en_expire.bind("<Button-1>", lambda e: open_calendar())
    
# ادامه لیبل ها

text6=Label(win,text="نسخه دار؟",font=("B titr",12))
text6.place(x=520,y=240)

var=IntVar()
r1=Radiobutton(win,font=("B titr",12),text=" با نسخه",value=0,variable=var)
r1.place(x=320,y=240)
r2=Radiobutton(win,font=("B titr",12),text=" بدون نسخه",value=1,variable=var)
r2.place(x=410,y=240)

text7=Label(win,text="قیمت ",font=("B titr",12))
text7.place(x=520,y=280)

text7=Label(win,text="(هزار تومان)",font=("B titr",10))
text7.place(x=520,y=310)

en_price=Entry(win,font=("B titr",10),width=30)
en_price.place(x=320,y=280)

text10=Label(win,text="نام مشتری",font=("B titr",12))
text10.place(x=240,y=40)

en_costumer=Entry(win,font=("B titr",10),width=30)
en_costumer.place(x=40,y=40)

# قسمت لیست باکس

def savebox():
    if en_drug.get() and en_costumer.get():
        data=(en_drug.get(),en_doses.get(),combo_numbers.get(),en_company.get(),
             expire_var.get(),var.get(),en_price.get(),en_costumer.get())
        print(data)

users_list=Listbox(win,font=("B titr",10),height=10,width=50)
users_list.place(x=10,y=80)

# خروج از برنامه

image_exit=PhotoImage(file="exit.png")
bt_exit=Button(win,font=("B titr",10),width=30,command=win.quit,image=image_exit)
bt_exit.place(x=520,y=550)

# حذف تکی 

def delete_sel():
    try:
        selected_index = users_list.curselection()
        if selected_index:
            selected_text = users_list.get(selected_index)
            print("متن انتخاب‌شده:", selected_text)  # فقط برای تست

            # استخراج id از ابتدای متن (قبل از __)
            item_id = selected_text.split("__")[0].strip()

            print("شناسه استخراج‌شده:", item_id)  # فقط برای تست

            # حذف از دیتابیس
            cur = con.cursor()
            cur.execute("DELETE FROM drugs WHERE id=?", (item_id,))
            con.commit()

            # حذف از لیست گرافیکی
            users_list.delete(selected_index)
            load_all_data()
            check_expired_drugs()

    except Exception as e:
        print("خطا در حذف موردی:", e)
        messagebox.showerror("خطا", "در حذف دارو مشکلی پیش آمد.")


bt_delete1=Button(win,text="حذف موردی",font=("B titr",10),width=8,command=delete_sel)
bt_delete1.place(x=435,y=550)

# حذف همه

def delete_all():
    try:
        con = sqlite3.connect("pharmacy.db")
        cur = con.cursor()
        cur.execute("DELETE FROM drugs")
        con.commit()
        con.close()

        users_list.delete(0, END)
        load_all_data()
    except Exception as e:
        print("خطا در حذف همه:", e)

image_delete=PhotoImage(file="delete.png")
bt_delete2=Button(win,font=("B titr",10),width=30,command=delete_all,image=image_delete)
bt_delete2.place(x=400,y=550)

# ..................................... بخش دیتابیس

con = sqlite3.connect("pharmacy.db")

con.execute('''
    CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        expire TEXT,
        prescription INTEGER,
        price REAL,
        drug_name TEXT,
        doses INTEGER,
        company TEXT,
        quantity INTEGER
    )
''')
con.commit()
 
# تابع نمایش همه داروهای موجود در دیتابیس در لیست باکس

def load_all_data():
    users_list.delete(0, END)
    cur = con.cursor()
    cur.execute("SELECT id, customer, drug_name, price, prescription, expire FROM drugs")
    rows = cur.fetchall()
    for row in rows:
        drug_id = row[0]
        customer = row[1]
        drug_name = row[2]
        price = row[3]
        prescription = "با نسخه" if row[4] == 0 else "بدون نسخه"
        expire = row[5]
       
        # رشته‌ای که در لیست‌باکس نمایش داده می‌شود:
        item_text = f"{drug_id}__{customer} - {drug_name} - {price} تومان - {prescription} - انقضا: {expire}"
        users_list.insert(END, item_text)
  
# ذخیره اطلاعات

def save_data():
    name = en_drug.get()
    dose = en_doses.get()
    price = en_price.get()
    quantity = combo_numbers.get()
    company = en_company.get()
    expire = expire_var.get()
    prescription = var.get()
    customer = en_costumer.get()
   
    if not all([name,dose,price,quantity,company,expire,customer]):
        messagebox.showwarning("خطا","لطفا همه فیلدها را تکمیل کنید")
        return  
        
    try:
        con.execute('''
        INSERT INTO drugs (drug_name, doses, price, quantity, company, expire, prescription, customer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, dose, price, quantity, company, expire, prescription, customer))
        con.commit()
        # users_list.insert(END, f"{customer}-{name}-{price} تومان")
        load_all_data()
        en_drug.delete(0, END)
        en_doses.delete(0, END)
        en_price.delete(0, END)
        combo_numbers.set('')
        en_company.delete(0, END)
        expire_var.set('')
        en_costumer.delete(0, END)
        messagebox.showinfo("ذخیره","اطلاعات با موفقیت ذخیره شد")
        check_expired_drugs()
    except Exception as e:
        messagebox.showerror("خطا",f"خطا در ذخیره اطلاعات :\n{e}")
              
bt_save=Button(win,text="ذخیره اطلاعات",font=("B titr",10),width=10,command=save_data,foreground="blue")
bt_save.place(x=300,y=550)

# جستجو

en_search_input=Entry(win,font=("B titr",10),width=20)
en_search_input.place(x=30,y=550)

def search_drug():
    keyword=en_search_input.get().strip()
    users_list.delete(0,END)
    if not keyword:
        messagebox.showwarning("جستجو","لطفا نام دارو را وارد کنید")
        return
    
    cur=con.cursor()
    cur.execute("select id,customer,drug_name,price,prescription,expire FROM drugs where drug_name like ?",('%'+keyword+'%',))
    results=cur.fetchall()
    if results:
        for row in results:
            drug_id = row[0]
            customer = row[1]
            drug_name = row[2]
            price = row[3]
            prescription = "با نسخه" if row[4] == 0 else "بدون نسخه"
            expire = row[5]

            item_text = f"{drug_id}__{customer} - {drug_name} - {price} تومان - {prescription} - انقضا: {expire}"
            users_list.insert(END, item_text)
    else:
        messagebox.showinfo("نتیجه‌ای یافت نشد", "دارویی با این نام یافت نشد")
            
            
            # users_list.insert(END,f"{row[0]}-{row[1]},{row[2]}تومان")
   
en_search=Button(win,text="جستجو بر اساس نام دارو",font=("B titr",10),foreground="green",command=search_drug)
en_search.place(x=160,y=550)

# بخش Toplevel

def aboutapp():
    about_win=Toplevel()
    about_win.title=("درباره داروخانه")
    about_win.geometry("350x90")
    
    lb_text=Label(about_win,text="داروخانه شبانه روزی دانش بطور 24 ساعته، در خدمت شماست")
    lb_text.place(x=10,y=20)
    

bt_about=Button(win,text="اطلاعات",command=aboutapp,font=("B titr",15),background="blue",foreground="white",borderwidth=4,width=9)
bt_about.place(x=320,y=320)

# بخش منو/ذخیره اطلاعات در فایل متنی

def saveTofile():
    from tkinter import filedialog
    file=filedialog.asksaveasfilename(defaultextension=".txt",
                                      filetypes=[("text files","*.txt"),("allfiles","*.*")])
    if file:
        try:
            with open(file,"w",encoding="utf_8") as f:
                for i in range (users_list.size()):
                    f.write(users_list.get(i)+"\n")
            messagebox.showinfo("ذخیره","فایل با موفقیت ذخیره شد")
        except Exception as e:
            messagebox.showerror("خطا","خطا در ذخیره فایل")

def about_dialog():
    win_about = Toplevel(win)
    win_about.title("درباره داروخانه")
    win_about.geometry("400x150")
    Label(
        win_about,
        text="داروخانه دکتر محبی\nتأسیس 1390\nبا ارائه داروهای مجاز و مشاوره رایگان 24 ساعته.\nآدرس: تهران، خیابان سلامت، پلاک 24",
        font=("B Titr", 11),
        justify="right"
    ).pack(padx=10, pady=20)
    
                       
menubar=Menu()

filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="ذخیره",command=saveTofile)
filemenu.add_separator()
filemenu.add_command(label="خروج",command=win.quit)

menubar.add_cascade(label="پوشه",menu=filemenu)
aboutmenue=Menu(menubar,tearoff=0)
aboutmenue.add_command(label="درباره برنامه",command=about_dialog)
menubar.add_cascade(label="درباره برنامه ",menu=aboutmenue)
win.config(menu=menubar)


# هشدار داروهای تاریخ انقضا

# image_warning=PhotoImage(file="warning.png")
frame_warn=LabelFrame(win,text="هشدار",font=("B titr",10),fg="red")
frame_warn.place(x=10,y=400,width=580,height=100)
# lbl_img=Label(frame_warn,image=image_warning)
# lbl_img.place(x=520,y=10)

def check_expired_drugs():
  
    for widget in frame_warn.winfo_children():
        widget.destroy()

    today = jdatetime.date.today()
    today_gregorian = today.togregorian()

    cur = con.cursor()
    cur.execute("SELECT customer, drug_name, expire FROM drugs")
    rows = cur.fetchall()

    warn_texts = []

    for row in rows:
        try:
            exp_jalali = jdatetime.datetime.strptime(row[2], "%Y/%m/%d").date()
            exp_gregorian = exp_jalali.togregorian()
            days_left = (exp_gregorian - today_gregorian).days

            if 0 <= days_left <= 14:
                warn_texts.append(f"⚠️ {row[1]} - تاریخ انقضا: {row[2]} - مشتری: {row[0]}")
        except Exception as e:
            print(f"خطا در تبدیل تاریخ: {e}")

    if warn_texts:
        full_text = "\n".join(warn_texts)
        lbl = Label(frame_warn, text=full_text, font=("B titr", 11), fg="red", bg="yellow", justify="right")
        lbl.place(x=10, y=5)
    else:
        lbl = Label(frame_warn, text="✅ داروی در حال انقضا وجود ندارد", font=("B titr", 11), fg="green")
        lbl.place(x=10, y=10)

# روی هر آیتم لیست بزنیم جزییات رو بیاره

def show_details():
    try:
        selected = users_list.get(users_list.curselection())
        # استخراج ID از ابتدای رشته
        drug_id = selected.split("__")[0].strip()

        cur = con.cursor()
        cur.execute('SELECT * FROM drugs WHERE id=?', (drug_id,))
        row = cur.fetchone()

        if row:
            detail_win = Toplevel(win)
            detail_win.title("جزئیات دارو")
            detail_win.geometry("400x300")

            labels = [
                f"مشتری: {row[1]}",
                f"تاریخ انقضا: {row[2]}",
                f"نسخه‌دار: {'بله' if row[3]==0 else 'خیر'}",
                f"قیمت: {row[4]} تومان",
                f"نام دارو: {row[5]}",
                f"دوز: {row[6]}",
                f"شرکت سازنده: {row[7]}",
                f"تعداد: {row[8]}"
            ]

            for i, txt in enumerate(labels):
                Label(detail_win, text=txt, font=("B Titr", 11), anchor="w").pack(anchor="w", padx=20, pady=5)
    except Exception as e:
        messagebox.showwarning("خطا", "لطفاً یک دارو را از لیست انتخاب کنید")

bt_details=Button(win,text="جزییات دارو",command=show_details,font=("B titr",10))
bt_details.place(x=15,y=330)

# ویرایش فیلدها

def edit_drug():
    selection = users_list.curselection()
    if not selection:
        messagebox.showwarning("خطا", "لطفاً یک دارو را از لیست انتخاب کنید")
        return

    selected = users_list.get(selection[0])
    try:
        drug_id = selected.split("__")[0].strip()

        cur = con.cursor()
        cur.execute('SELECT * FROM drugs WHERE id=?', (drug_id,))
        row = cur.fetchone()

        if row:
            edit_win = Toplevel(win)
            edit_win.title("ویرایش دارو")
            edit_win.geometry("400x500")

            # متغیرها برای فیلدهای فرم
            var_name = StringVar(value=row[5])
            var_dose = StringVar(value=row[6])
            var_quantity = StringVar(value=row[8])
            var_company = StringVar(value=row[7])
            var_expire = StringVar(value=row[2])
            var_prescription = IntVar(value=row[3])
            var_price = StringVar(value=row[4])
            var_customer = StringVar(value=row[1])

            # فرم ویرایش
            Label(edit_win, text="نام دارو").pack()
            Entry(edit_win, textvariable=var_name).pack()

            Label(edit_win, text="دوز").pack()
            Entry(edit_win, textvariable=var_dose).pack()

            Label(edit_win, text="تعداد").pack()
            Entry(edit_win, textvariable=var_quantity).pack()

            Label(edit_win, text="شرکت").pack()
            Entry(edit_win, textvariable=var_company).pack()

            Label(edit_win, text="تاریخ انقضا").pack()
            Entry(edit_win, textvariable=var_expire).pack()

            Label(edit_win, text="نسخه‌دار؟").pack()
            Radiobutton(edit_win, text="با نسخه", variable=var_prescription, value=0).pack()
            Radiobutton(edit_win, text="بدون نسخه", variable=var_prescription, value=1).pack()

            Label(edit_win, text="قیمت").pack()
            Entry(edit_win, textvariable=var_price).pack()

            Label(edit_win, text="نام مشتری").pack()
            Entry(edit_win, textvariable=var_customer).pack()

            def save_edit():
                try:
                    con.execute('''
                        UPDATE drugs SET 
                            drug_name=?, 
                            doses=?, 
                            quantity=?, 
                            company=?, 
                            expire=?, 
                            prescription=?, 
                            price=?, 
                            customer=?
                        WHERE id=?
                    ''', (
                        var_name.get(), 
                        var_dose.get(), 
                        var_quantity.get(), 
                        var_company.get(), 
                        var_expire.get(), 
                        var_prescription.get(), 
                        var_price.get(), 
                        var_customer.get(),
                        drug_id
                    ))
                    con.commit()
                    load_all_data()
                    check_expired_drugs()
                    messagebox.showinfo("ویرایش", "اطلاعات با موفقیت ویرایش شد")
                    edit_win.destroy()
                except Exception as e:
                    messagebox.showerror("خطا", f"خطا در ویرایش اطلاعات:\n{e}")

            Button(edit_win, text="ذخیره تغییرات", command=save_edit, fg="blue").pack(pady=20)

    except Exception as e:
        messagebox.showerror("خطا", f"مشکل در پردازش اطلاعات:\n{e}")


bt_edit=Button(win,text="ویرایش",command=edit_drug, font=("B titr",10))
bt_edit.place(x=100,y=330)


load_all_data()
check_expired_drugs()
mainloop()

