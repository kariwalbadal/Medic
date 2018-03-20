import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from dbutils import getDiseases, init, destroy
from classifier import classifier
import os
from mail_bot import send_mail


class Main_Window(Gtk.Window):

    def __init__(self):
        #WINDOW DESCRIPTION

        Gtk.Window.__init__(self, title = "Medical App")
        self.set_border_width(10)
        self.set_default_size(850, 300)


        #MAKING BOXES

        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        self.vbox1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        self.vbox2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)



        main_menu_bar = Gtk.MenuBar()

        #FILE MENU

        file_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem("File")

        file_save = Gtk.MenuItem("Save")
        file_exit = Gtk.MenuItem("Exit")

        file_exit.connect("activate", Gtk.main_quit)
        file_save.connect("activate", self.save_file)

        file_menu_dropdown.set_submenu(file_menu)

        file_menu.append(file_save)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(file_exit)

        main_menu_bar.append(file_menu_dropdown)


        #ADDING MENU BAR IN THE BOX

        self.hbox.pack_start(main_menu_bar, True, True, 0)


        #ADDING VERTICAL BOX INSIDE THE HORIZONTAL BOX

        self.hbox.pack_start(self.vbox1, True, True, 0)
        boxseparator = Gtk.Separator(orientation = Gtk.Orientation. VERTICAL)
        self.hbox.pack_start(boxseparator, True, True, 0)
        self.hbox.pack_start(self.vbox2, True, True, 0)




        #PATIENT'S DETAILS FILL

        self.label_name = Gtk.Label("Patient's Name : ")
        self.vbox1.pack_start(self.label_name, False, True, 0)
        self.name = Gtk.Entry()
        self.vbox1.pack_start(self.name, False, True, 5)

        self.label_age = Gtk.Label("Patient's Age : ")
        self.vbox1.pack_start(self.label_age, False, True, 0)
        self.age = Gtk.Entry()
        self.vbox1.pack_start(self.age, False, True, 5)

        label_address = Gtk.Label("Patient's Address :")
        self.vbox1.pack_start(label_address, False, True, 0)
        self.address = Gtk.Entry()
        self.vbox1.pack_start(self.address, False, True, 5)

        label_number = Gtk.Label("Patient's Phone Number : ")
        self.vbox1.pack_start(label_number, False, True, 0)
        self.number = Gtk.Entry()
        self.vbox1.pack_start(self.number, False, True, 5)



        #SYMPTOMS DETAILS
        self.symptom1 = Gtk.Entry()
        self.symptom1.set_placeholder_text("(Compulsory)")
        self.symptom2 = Gtk.Entry()
        self.symptom2.set_placeholder_text("(Compulsory)")
        self.symptom3 = Gtk.Entry()
        self.symptom3.set_placeholder_text("(Optional)")
        self.symptom4 = Gtk.Entry()
        self.symptom4.set_placeholder_text("(Optional)")
        self.symptom5 = Gtk.Entry()
        self.symptom5.set_placeholder_text("(Optional)")

        label_symptom = Gtk.Label("Symptoms : ")
        self.vbox2.pack_start(label_symptom, False, True, 0)

        label_info = Gtk.Label("Please enter symptoms from the list available")
        self.vbox2.pack_start(label_info, False, True, 0)

        self.vbox2.pack_start(self.symptom1, False, True, 5)
        self.vbox2.pack_start(self.symptom2, False, True, 5)
        symptom_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox2.pack_start(symptom_separator, False, True, 0)
        self.vbox2.pack_start(self.symptom3, False, True, 5)
        self.vbox2.pack_start(self.symptom4, False, True, 5)
        self.vbox2.pack_start(self.symptom5, False, True, 5)


        #SET COMPLETION MODE IN THE SYMPTOMS

        completion1 = Gtk.EntryCompletion()
        completion2 = Gtk.EntryCompletion()
        completion3 = Gtk.EntryCompletion()
        completion4 = Gtk.EntryCompletion()
        completion5 = Gtk.EntryCompletion()
        self.liststore = Gtk.ListStore(str)
        self.problems = []
        with open("sym.txt") as filename:
            for line in filename:
                self.problems.append(line.strip('\n'))

        for text in self.problems:
            self.liststore.append([text])

        completion1.set_model(self.liststore)
        completion2.set_model(self.liststore)
        completion3.set_model(self.liststore)
        completion4.set_model(self.liststore)
        completion5.set_model(self.liststore)
        completion1.set_text_column(0)
        completion2.set_text_column(0)
        completion3.set_text_column(0)
        completion4.set_text_column(0)
        completion5.set_text_column(0)



        self.symptom1.set_completion(completion1)
        self.symptom2.set_completion(completion2)
        self.symptom3.set_completion(completion3)
        self.symptom4.set_completion(completion4)
        self.symptom5.set_completion(completion5)






        #SUBMIT BUTTON

        self.submit = Gtk.Button("Submit")
        self.submit.connect("clicked", self.submit_clicked)
        self.vbox2.pack_start(self.submit, False, True, 5)
        #ADD HORIZONTAL BOX TO THE WINDOW WHICH CONTAINS ALL THE BOXES

        self.add(self.hbox)




    def submit_clicked(self, widget):

        if len(self.name.get_text()) == 0 or len(self.age.get_text()) == 0 or len(self.address.get_text()) == 0 or len(self.number.get_text()) == 0:
            dialog_details = Details(self)
            response = dialog_details.run()

            dialog_details.destroy()
            return

        try:

            pqr=int(self.age.get_text())
            abc = int(self.number.get_text())
            if(pqr<0 or pqr>120):
                pqr = (int)("abc")
            if(len(str(abc))!=10 and abc > 0):
                abc = (int)("pqr")
        except Exception as e:
            dialog_number = Number(self)
            response = dialog_number.run()
            dialog_number.destroy()
            return

        if(len(self.symptom1.get_text()) == 0 or len(self.symptom2.get_text()) == 0):
            dialog_error = PopUp(self)
            response = dialog_error.run()

            dialog_error.destroy()
            return

        if len(self.symptom1.get_text()) != 0:
            if self.symptom1.get_text() not in self.problems:
                print(self.symptom1.get_text())
                print(self.liststore)
                dialog_entry_error = Error(self)
                response = dialog_entry_error.run()
                dialog_entry_error.destroy()
                return
        if len(self.symptom2.get_text()) != 0:
            if self.symptom2.get_text() not in self.problems:
                dialog_entry_error = Error(self)
                response = dialog_entry_error.run()
                dialog_entry_error.destroy()
                return
        if len(self.symptom3.get_text()) != 0:
            if self.symptom3.get_text() not in self.problems:
                dialog_entry_error = Error(self)
                response = dialog_entry_error.run()
                dialog_entry_error.destroy()
                return


        if len(self.symptom4.get_text()) != 0:
            if self.symptom4.get_text() not in self.problems:
                dialog_entry_error = Error(self)
                response = dialog_entry_error.run()
                dialog_entry_error.destroy()
                return

        if len(self.symptom5.get_text()) != 0:
            if self.symptom5.get_text() not in self.problems:
                dialog_entry_error = Error(self)
                response = dialog_entry_error.run()
                dialog_entry_error.destroy()
                return

        if self.symptom2.get_text() == self.symptom1.get_text() and len(self.symptom2.get_text())>0:
            dialog_same = Same(self)
            response = dialog_same.run()
            dialog_same.destroy()
            return

        if (self.symptom3.get_text() == self.symptom1.get_text() or self.symptom3.get_text() == self.symptom2.get_text()) and  len(self.symptom3.get_text())>0:
            dialog_same = Same(self)
            response = dialog_same.run()
            dialog_same.destroy()
            return

        if (self.symptom4.get_text() == self.symptom1.get_text() or self.symptom4.get_text() == self.symptom2.get_text() or self.symptom4.get_text() == self.symptom3.get_text()) and len(self.symptom4.get_text())>0:
            dialog_same = Same(self)
            response = dialog_same.run()
            dialog_same.destroy()
            return

        if (self.symptom5.get_text() == self.symptom1.get_text() or self.symptom5.get_text() == self.symptom2.get_text() or self.symptom5.get_text() == self.symptom3.get_text() or self.symptom5.get_text() == self.symptom4.get_text()) and len(self.symptom5.get_text())>0:
            dialog_same = Same(self)
            response = dialog_same.run()
            dialog_same.destroy()
            return

        list = []
        list.append(self.symptom1.get_text())
        list.append(self.symptom2.get_text())
        if(len(self.symptom3.get_text())>0):
            list.append(self.symptom3.get_text())
        if (len(self.symptom4.get_text()) > 0):
            list.append(self.symptom4.get_text())
        if (len(self.symptom5.get_text()) > 0):
            list.append(self.symptom5.get_text())

        #DISEASE SELECTION USING CLASSIFIER

        db_client = init()
        all_Diseases = getDiseases(list)
        self.disease = classifier(all_Diseases, list)

        destroy(db_client)

        dialog_answer = Answer(self, self.disease)
        response = dialog_answer.run()
        self.save_file(response)
        dialog_answer.destroy()

        time = str(datetime.datetime.now())
        time = time.split(' ')

        date = time[0].split('-')
        date = date[2] + "-" + date[1] + "-" + date[0]
        time = time[1][:len(time[1]) - 7]

        try:
            send_mail(self.name.get_text(), date, time, self.name.get_text()+"_"+date+"_"+time+".pdf")

            dialog_mail_sent = Mail(self)
            response = dialog_mail_sent.run()
            dialog_mail_sent.destroy()

        except Exception as e:

            dialog_mail_error = Mail_error(self)
            response = dialog_mail_error.run()
            dialog_mail_error.destroy()


        filep = './Reports/' + self.name.get_text()+"_"+date+"_"+time+".pdf"
        os.system('/usr/bin/xdg-open '+filep)
        self.name.set_text('')
        self.age.set_text('')
        self.address.set_text('')
        self.number.set_text('')
        self.symptom3.set_text('')
        self.symptom2.set_text('')
        self.symptom1.set_text('')
        self.symptom5.set_text('')
        self.symptom4.set_text('')


    def save_file(self, widget):
        time = str(datetime.datetime.now())
        time = time.split(' ')

        date = time[0].split('-')
        date = date[2] + "-" + date[1] + "-" + date[0]
        time = time[1][:len(time[1]) - 7]
        filepath = os.getcwd()
        if not os.path.exists(filepath + "/Reports"):
            os.mkdir(filepath + "/Reports")
        c = canvas.Canvas(filepath + "/Reports/"+self.name.get_text()+"_"+date+"_"+time+".pdf", pagesize=A4)
        c.setFont('Helvetica', 20, leading=None)
        c.drawString(240, 810, "Patient's Details")
        c.setFont('Helvetica', 18, leading=None)
        c.drawString(5, 810, date)
        c.drawString(510, 810, time)
        c.setFont('Helvetica', 16, leading = None)
        c.drawString(5, 750, "Name : ")
        c.setFont('Helvetica', 16, leading = None)
        c.drawString(90, 750, self.name.get_text())
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 710, "Age : ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(90,710, self.age.get_text())

        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 670, "Address : ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(90, 670, self.address.get_text())
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 630, "Number : ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(90, 630, self.number.get_text())


        c.setFont('Helvetica', 20, leading=None)
        c.drawString(270, 570, "Symptoms")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 530, "1. ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(20, 530, self.symptom1.get_text())
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 490, "2. ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(20, 490, self.symptom2.get_text())

        optional_symptoms = 0

        if len(self.symptom3.get_text()) > 0:
            optional_symptoms = optional_symptoms + 1
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(5, 490-optional_symptoms*40, str(2+optional_symptoms)+".")
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(20, 490-optional_symptoms*40, self.symptom3.get_text())
        if len(self.symptom4.get_text()) > 0:
            optional_symptoms = optional_symptoms + 1
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(5, 490-optional_symptoms*40, str(2+optional_symptoms)+".")
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(20, 490-optional_symptoms*40, self.symptom4.get_text())
        if len(self.symptom5.get_text()) > 0:
            optional_symptoms = optional_symptoms + 1
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(5,490-optional_symptoms*40, str(2+optional_symptoms)+".")
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(20, 490-optional_symptoms*40, self.symptom5.get_text())

        c.setFont('Helvetica', 20, leading=None)
        y = 490-60-40*optional_symptoms
        c.drawString(275, y, "Disease")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(160, y-60, "The Patient is suffering from "+self.disease)
        c.showPage()
        c.save()

class PopUp(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(100, 50)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("Atleast Two Symptoms are required."))
        self.show_all()




class Answer(Gtk.Dialog):



    def __init__(self, parent, disease):

        Gtk.Dialog.__init__(self, "Disease", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(100,50)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.disease = disease
        area = self.get_content_area()
        area.add(Gtk.Label("The Possible Disease Patient is suffering from is " + self.disease))
        self.show_all()



class Error(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(100, 50)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("You have entered one or more wrong symptoms"))
        self.show_all()


class Same(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(130, 80)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("Repeated Symptom(s)"))
        self.show_all()

class Details(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(130, 80)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("Please enter Patient's details"))
        self.show_all()

class Number(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(130, 80)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("Invalid Age or Phone number"))
        self.show_all()


class Mail(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Mail Sent", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(130, 80)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("The Mail has been sent"))
        self.show_all()


class Mail_error(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(130, 80)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        area = self.get_content_area()
        area.add(Gtk.Label("The report couldn't be mailed to the doctor"))
        self.show_all()




window = Main_Window()
window.set_position(Gtk.WindowPosition.CENTER)
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()