# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:13:39 2020

@author: surface
"""
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
from splinter import Browser
import datetime
from datetime import timedelta
from time import sleep
import _thread

Weekdict={0:'Sunday',1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday'}
Urldict={0:'https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=2c9c486e4f821a19014f82418a900004',
         1:'https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=2c9c486e4f821a19014f826f2a4f0036',
         2:'https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=8aecc6ce749544fd01749a31a04332c2',
         }
    

Timedict={'Today':0,'Tomorrow':1,'+2':2,'+3(rush mode)':3}

namedict={0:'正大',1:'北区',2:'江湾'}
browser_state_dict={0:'log in',1:'search',2:'record'}

class OOP():
    def __init__(self):
        self.win=tk.Tk()
        self.win.geometry('700x700')
        self.win.title('Python GUI')
        self.create_settings()
        self.create_login()
        self.create_query()
        self.create_records()
        self.create_menu()
        
        self.valid_sites=[]
        self.select_row=-1
        
        self.valid_td=[]
        self.select_record_row=-1
        self.browser_state='log in'
        self.today=datetime.date.today()
        self.username=''
        self.password=''
        self.mobile=''
        

        

        
    
    
    def create_menu(self):
        def msgbox():
            msg.showinfo('Info Box','This is a python GUI designed by Wenliang Zhang\n Use for fun : )')
        menu_bar=Menu(self.win)
        self.win.config(menu=menu_bar)
        
        file_menu=Menu(menu_bar,tearoff=0)
        file_menu.add_command(label='About',command=msgbox)
        menu_bar.add_cascade(label='Menu',menu=file_menu)
    
    
    
    def create_settings(self):
        settings=ttk.LabelFrame(self.win,text='Settings')
        settings.grid(row=0,column=0,sticky='w'+'e',padx=50,pady=10)

        driver_label=ttk.Label(settings, text='Driver name',width=15,anchor='center')
        driver_label.grid(row=0,column=0,padx=5,pady=5)
        
        self.driver_name=tk.StringVar()
        driver_option=ttk.Combobox(settings,textvariable=self.driver_name,width=17,state='readonly')
        driver_option['values']=('firefox','chrome')
        driver_option.current(0)
        driver_option.grid(row=0,column=1,padx=5)
        

    
    def log_in(self):
        
        try:
            driver=self.driver_name.get()
            self.browser = Browser(driver_name=driver,headless=True)
            self.browser.visit('https://elife.fudan.edu.cn/')
            self.browser.find_by_xpath("//div/input[@class='xndl']").click()
            self.browser.fill("username", self.username)
            self.browser.fill("password", self.password)
            self.browser.find_by_value(u'登录').click()
            self.note.configure(text=('Hello, '+self.browser.find_by_xpath("//div[@class='person_a']").first.text))
            self.search_button.configure(state='normal')
            self.search_button2.configure(state='normal')
            self.info_button1.configure(state='normal')
            self.info_button2.configure(state='normal')
            self.browser.cookies.all()
        except:
            self.note.configure(text='Failed, please check your input or Internet access')


        
    def search(self):
        
        self.browser_state='search'
        def select(event,row):
            self.select_row=int(row)-1
            self.avail_scr.tag_raise('tag_all')
            self.avail_scr.tag_configure('tag_all',background='white',foreground='black')
            self.avail_scr.tag_raise('tag'+row)            
            self.avail_scr.tag_configure('tag'+row,background='blue',foreground='white')
        
        
        
        self.avail_scr.configure(state='normal')
        self.avail_scr.delete('1.0','end')
        self.valid_sites=[]
        self.select_row=-1


        
        
        urlcode=self.court_var.get()
        user_start_time=int(self.start_time.get()[0:2])
        user_end_time=int(self.end_time.get()[0:2])




        
        dtime=Timedict[self.date.get()]
        reserve_date=(self.today+timedelta(dtime,0)).strftime('%Y-%m-%d')
        self.browser.visit(Urldict[urlcode]+'&currentDate='+reserve_date)        


        found_sites=self.browser.find_by_xpath("//td[@class='site_td1']/font")
        sites=[]
        for site in found_sites:
            if site.text !='':
                sites.append(site.text)
        has_reversed=self.browser.find_by_xpath("//td[@class='site_td4']/font")
        all_for_reservation=self.browser.find_by_xpath("//td[@class='site_td4']/span")
        
        
        
        
        if len(has_reversed)==0:
            self.avail_scr.insert('insert','您好，当天没有场地可以预约')
        else:
            

            for i in range(len(has_reversed)):
                site_time=int(sites[i][0:2])
                remain=int(all_for_reservation[i].text)-int(has_reversed[i].text)
                if (site_time>=user_start_time) and (site_time<=(user_end_time-1)) and remain>0:
                    self.valid_sites.append(i)


            if len(self.valid_sites)==0:
                self.avail_scr.insert('insert','该时段场地未开放或已预定完，请适当放宽筛选条件。')
            else:                    
                for valid_site_num in self.valid_sites:            
                    self.avail_scr.insert('insert',Weekdict[int((self.today+timedelta(dtime,0)).strftime('%w'))]+' '+ sites[valid_site_num]+' '+namedict[urlcode]+' \n') 
                    
                    
                self.avail_scr.tag_add('tag_all','1.0','end')
                
                self.avail_scr.tag_raise('tag_all')
                self.avail_scr.tag_configure('tag_all',background='white',foreground='black')  #刷新的时候把蓝色漂白
                
                for j in range(len(self.valid_sites)):
                    row=str(j+1)
                    self.avail_scr.tag_add('tag'+row,row+'.0',row+'.end')
                    self.avail_scr.tag_bind('tag'+str(j+1),'<Button-1>',lambda event,row=row: select(event,row))
        
            
        self.avail_scr.configure(state='disable')
        
        
    def make_appointment(self):
        dtime=Timedict[self.date.get()]
        reserve_date=(self.today+timedelta(dtime,0)).strftime('%Y-%m-%d')
        url=Urldict[self.court_var.get()]+'&currentDate='+reserve_date
        
        def wait_for_the_midnight():
            while (self.today.strftime('%d')==datetime.date.today().strftime('%d')):
                sleep(300)
            self.browser.visit(url)
            self.browser.find_by_tag('li').last.click()
            self.browser.find_by_tag('img')[self.select_row].click()
            try:
                self.browser.fill('mobile',self.mobile)
                self.browser.find_by_value(u' 预 约 ').click()
                self.note2.configure('Job done')
            except:
                self.note2.configure(text='Error, something wrong happened')
            else:
                self.note2.configure(text='Job done')
            
        
        if self.select_row==-1 or self.browser_state != 'search':
            if self.browser_state!='search':
                self.note2.configure(text='Please update the search result')
            
            if self.select_row==-1:
                self.note2.configure(text='Please choose a court first')
            
        else:
            if Timedict[self.date.get()] <=2 :
                try:
                    self.browser.find_by_tag('img')[self.valid_sites[self.select_row]].click()
                    self.browser.fill('mobile',self.mobile)
                    self.browser.find_by_value(u' 预 约 ').click()
                except:
                    self.note2.configure(text='You cannot book the court')
                else:
                    self.note2.configure(text='Job done')
            
            else:
                confirm_msg=msg.askokcancel('提示', '确定执行抢场功能吗，这可能需要一点时间。（场地晚上12点刷新，请保持程序运行）')
                if confirm_msg==True:
                    self.note2.configure(text='Job has been queued, hold on please.')
                    _thread.start_new_thread(wait_for_the_midnight,())
                    

                        



                
    def update(self):
        self.browser_state='record'
        self.record_scr.configure(state='normal')
        self.record_scr.delete('1.0','end')
        self.valid_td=[]
        self.select_record_row=-1


        
                
        def select(event,row):
            self.select_record_row=int(row)-1
            self.record_scr.tag_raise('tag_all')
            self.record_scr.tag_configure('tag_all',background='white',foreground='black')
            self.record_scr.tag_raise('tag'+row)            
            self.record_scr.tag_configure('tag'+row,background='blue',foreground='white')

        
        self.valid_td=[]
        self.browser.visit('https://elife.fudan.edu.cn/public/userbox/index.htm?userConfirm=&orderstateselect=')
        record_tr_num=len(self.browser.find_by_xpath("//table[@class='table3']/tbody/tr"))
        record_td=self.browser.find_by_xpath("//table[@class='table3']/tbody/tr/td")
        for i in range(record_tr_num):
            if record_td[5+7*i].text=='待签到':
                self.valid_td.append(i)
        
        if len(self.valid_td)!=0:
            for j in self.valid_td:
                valid_record_name=record_td[3+7*j].text+'  '+record_td[4+7*j].text+'  '+record_td[2+7*j].text+'\n'
                self.record_scr.insert('insert',valid_record_name)
                
            self.record_scr.tag_add('tag_all','1.0','end')
            
            self.record_scr.tag_raise('tag_all')
            self.record_scr.tag_configure('tag_all',background='white',foreground='black')  #刷新的时候把蓝色漂白

            for p in range(len(self.valid_td)):
                row=str(p+1)
                self.record_scr.tag_add('tag'+row,row+'.0',row+'.end')
                self.record_scr.tag_bind('tag'+row,'<Button-1>',lambda event,row=row: select(event,row))
        self.record_scr.configure(state='disable')

    
    
    
    
    
    def cancel(self):
        self.browser.visit('https://elife.fudan.edu.cn/public/userbox/index.htm?userConfirm=&orderstateselect=')
        if self.select_record_row!=-1:
            self.browser.find_by_xpath("//table[@class='table3']/tbody/tr/td")[6+(self.valid_td[self.select_record_row])*7].click()
            self.browser.get_alert().accept()
            
            self.record_scr.configure(state='normal')
            self.record_scr.tag_raise('tag_all')
            self.record_scr.tag_configure('tag_all',background='white',foreground='black')  #刷新的时候把蓝色漂白
            self.record_scr.delete('1.0','end')
            self.record_scr.insert('insert','取消预约成功，请刷新')
            self.record_scr.configure(state='disable')
        else:
            self.record_scr.configure(state='normal')
            self.record_scr.tag_raise('tag_all')
            self.record_scr.tag_configure('tag_all',background='white',foreground='black')  #刷新的时候把蓝色漂白
            self.record_scr.delete('1.0','end')
            self.record_scr.insert('insert','您未选择需要取消的预约，请刷新后重试')
            self.record_scr.configure(state='disable')
            



            


        
        
    


    

       
    def create_login(self):
        def confirm():
            login_button_1.configure(text='modify',command=modify)
            student_ID_enter.configure(state='readonly')
            mobile_enter.configure(state='readonly')
            password_enter.configure(state='readonly')
            self.username=student_ID_var.get()
            self.password=password_var.get()
            self.mobile=mobile_var.get()
 
      
        def modify():
            login_button_1.configure(text='OK',command=confirm)
            student_ID_enter.configure(state='normal')
            mobile_enter.configure(state='normal')
            password_enter.configure(state='normal')
        
            
            

        login=ttk.LabelFrame(self.win,text=' Log in')
        login.grid(row=1,column=0,padx=50,pady=10,sticky='w'+'e')
        
        student_ID_label=ttk.Label(login,text='Student ID',width=15,anchor='center')
        student_ID_label.grid(row=0,column=0,padx=5,pady=5)
        student_ID_var=tk.StringVar()
        student_ID_enter=ttk.Entry(login,textvariable=student_ID_var,width=20)
        student_ID_enter.grid(row=0,column=1,padx=5)
        
        password_label=ttk.Label(login,text='Password',width=15,anchor='center')
        password_label.grid(row=1,column=0,padx=5,pady=5)
        password_var=tk.StringVar()
        password_enter=ttk.Entry(login,textvariable=password_var)
        password_enter.grid(row=1,column=1,padx=5)

        mobile_label=ttk.Label(login,text='Mobile',width=15,anchor='center')
        mobile_label.grid(row=2,column=0,pady=5,padx=5)
        mobile_var=tk.StringVar()
        mobile_enter=ttk.Entry(login,textvariable=mobile_var)
        mobile_enter.grid(row=2,column=1,padx=5)


        img=Image.open(r"./logo.jpg")
        global tk_img
        tk_img=ImageTk.PhotoImage(img)
        logo_frame=tk.Label(login,image=tk_img)
        logo_frame.grid(row=0,column=3,rowspan=3,columnspan=5,padx=30,pady=5)
        
        
        
        login_button_1=ttk.Button(login, text='OK',command=confirm,width=10)
        login_button_1.grid(row=3,column=6,pady=10,padx=20,sticky='e')
        
        login_button_2=ttk.Button(login, text='Log in',command=self.log_in,width=10)
        login_button_2.grid(row=3,column=7,pady=10,padx=5)    
        
        self.note=ttk.Label(login,text='Please verify your identity')
        self.note.grid(row=3,column=0,padx=100,columnspan=4,sticky='w')



    def create_query(self):
        query=ttk.LabelFrame(self.win,text=' Query ')
        query.grid(row=2,column=0,padx=50,pady=10,sticky='w'+'e')
        
        court_label=ttk.Label(query,text='Court',width=14,anchor='center')
        court_label.grid(row=0,column=0,padx=5,pady=5)
        self.court_var=tk.IntVar()
        self.court_var.set(0)
        courtRad1=ttk.Radiobutton(query,text='正大',variable=self.court_var,value=0,width=8)
        courtRad1.grid(column=1,row=0,sticky='w',padx=5)
        courtRad2=ttk.Radiobutton(query,text='北区',variable=self.court_var,value=1,width=8)
        courtRad2.grid(column=2,row=0,sticky='w')
        courtRad3=ttk.Radiobutton(query,text='江湾',variable=self.court_var,value=2,width=8)
        courtRad3.grid(column=1,row=1,sticky='w',padx=5)

        
        date_label=ttk.Label(query,text='Day of Week',anchor='center')
        date_label.grid(row=2,column=0,padx=5,pady=5)
        self.date=tk.StringVar()
        date_option=ttk.Combobox(query,textvariable=self.date,width=17,state='readonly')
        date_option['values']=('Today','Tomorrow','+2','+3(rush mode)')
#        date_option.current(int((datetime.date.today()).strftime('%w')))
        date_option.current=('Tomorrow')
        date_option.grid(row=2,column=1,padx=5,columnspan=2)


        start_time_label=ttk.Label(query,text='Start time',anchor='center')
        start_time_label.grid(row=3,column=0,padx=5,pady=5)
        self.start_time=tk.StringVar()
        start_time_option=ttk.Combobox(query,textvariable=self.start_time,width=17,state='readonly')
        start_time_option['values']=('08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00')
        start_time_option.current(0)
        start_time_option.grid(row=3,column=1,padx=5,columnspan=2)
        
        end_time_label=ttk.Label(query,text='End time',anchor='center')
        end_time_label.grid(row=4,column=0,padx=5,pady=5)
        self.end_time=tk.StringVar()
        end_time_option=ttk.Combobox(query,textvariable=self.end_time,width=17,state='readonly')
        end_time_option['values']=('09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','22:00')
        end_time_option.current(12)
        end_time_option.grid(row=4,column=1,padx=5,columnspan=2)
        

        
        
        avail_label=ttk.Label(query,text='Available',width=10)
        avail_label.grid(row=0,column=3,padx=30,pady=5,sticky='w')
        
        self.avail_scr=scrolledtext.ScrolledText(query,width=33,height=7)
        self.avail_scr.grid(row=1,column=3,padx=30,pady=5,rowspan=4,columnspan=4)
        self.avail_scr.bind('<Enter>',self.avail_scr.configure(cursor='arrow'))        
        self.avail_scr.configure(state='disable')
         
        
        self.search_button=ttk.Button(query,text='Search',width=10,command=self.search,state='disable')
        self.search_button.grid(row=5,column=4,padx=15,pady=10,sticky='w')
        
        self.search_button2=ttk.Button(query,text='Reserve',command=self.make_appointment,width=10,state='disable')
        self.search_button2.grid(row=5,column=6,padx=30,pady=10,sticky='w')

        self.note2=ttk.Label(query,text='Please set your preference')
        self.note2.grid(row=5,column=0,padx=100,columnspan=4,sticky='w')
        
    def create_records(self):
        info=ttk.LabelFrame(self.win,text=' Info ')
        info.grid(row=3,column=0,padx=50,pady=10,sticky='w'+'e')
        record_label=ttk.Label(info,text='Records',width=14,anchor='center')
        record_label.grid(row=0,column=0,padx=5,pady=5,sticky='w')
        
        self.record_scr=tk.Text(info,width=50,height=3)
        self.record_scr.grid(row=1,column=0,padx=50,pady=10,rowspan=2,columnspan=2,sticky='e')
        self.record_scr.bind('<Enter>',self.avail_scr.configure(cursor='arrow'))        
        self.avail_scr.configure(state='disable')
        
        
        self.info_button1=ttk.Button(info,text='Update',width=10,command=self.update,state='disable')
        self.info_button1.grid(row=1,pady=5,padx=10,column=2)
        
        self.info_button2=ttk.Button(info,text='Cancel',width=10,command=self.cancel,state='disable')
        self.info_button2.grid(row=2,pady=5,column=2)



oop=OOP()
oop.win.mainloop()    