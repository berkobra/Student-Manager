# -*- coding: utf-8 -*-
from __future__ import print_function
import easygui as eg
import sys
import csv
from collections import OrderedDict


BLANK_LIST_ERROR = 'Program logic error - no choices were specified.'
PROPERTIES = ("Ad","Soyad","Universite","OSYM Puani",
              "Yili","CBUTF Taban Puani","Not Ortalamasi")

class Student(object):
    def calc_puan(self):
        if self.osym_puani != '' and self.cbutf_puani != '' and self.not_ortalamasi != '':
            self.puan = '{:.3f}'.format((float(self.osym_puani)/float(self.cbutf_puani))*100 + float(self.not_ortalamasi))
        else:
            self.puan = ''

    def __init__(self, name, surname, university,
                 osym_puani, year, cbutf_puani, not_ortalamasi):
        self.name = name
        self.surname = surname
        self.university = university
        self.year = year
        self.osym_puani = osym_puani
        self.cbutf_puani = cbutf_puani
        self.not_ortalamasi = not_ortalamasi
        self.calc_puan()  

    def __repr__(self):
        return '{} {}'.format(self.name,self.surname)

    def __eq__(self, other):
        if isinstance(other, str):
            return repr(self) == other

    def remove(self):
        student_l.remove(self)

    def get_info(self):
        return OrderedDict([('name', self.name),
                            ('surname', self.surname),
                            ('university', self.university),
                            ('osym_puani', self.osym_puani),
                            ('year', self.year),
                            ('cbutf_puani',self.cbutf_puani),
                            ('not_ortalamasi',self.not_ortalamasi),
                            ('puan',self.puan)])

    def edit(self, values):
        self.name,self.surname,self.university,self.osym_puani,self.year,self.cbutf_puani,self.not_ortalamasi = values
        self.calc_puan()

    def export_for_csv(self):
        return self.get_info().values()

def txt_to_ascii(text):
    mapping = {'ı':'i','ğ':'g','ö':'o',
               'ü':'u','ş':'s','ç':'c'}

    return ''.join( mapping[c] if c in 'ışğöçü' else c for c in text)

def str_to_student(chosen_student,student_list):
    for student in student_list:
        if student == chosen_student:
            return student

def add_student(student_list):
    values = eg.multenterbox(msg='Ogrenci bilgilerini giriniz:',
                            title='Ogrenci bilgisi', 
                            fields=PROPERTIES, values=())

    if values:

    #    new_student = Student(*map(txt_to_ascii, values))
        new_student = Student(*values)
        student_list.append(new_student)

def edit_student(chosen_student):
    updated_values = eg.multenterbox(msg='Ogrenci bilgilerini giriniz:',
                                    title='Ogrenci bilgisi', fields=PROPERTIES,
                                    values=chosen_student.get_info().values())
    if updated_values:
    #    chosen_student.edit(map(txt_to_ascii, updated_values))
        chosen_student.edit(updated_values)

def sort_students(student_list):
    return sorted(student_list,key=lambda x: x.osym_puani)

def quit_prompt(student_list):
    if eg.ynbox("Cikmak istediginize emin misiniz?",choices=('Evet','Hayir')):
        with open('ogrenciler.csv','wb') as f:
            writer = csv.writer(f,delimiter=';')
            writer.writerow(['AD','SOYAD','UNIVERSITE','OSYM PUANI','YILI','CBUTF TABAN PUANI','NOT ORTALAMASI','PUAN'])
            student_list = sort_students(student_list)
            for student in student_list:
                writer.writerow(student.export_for_csv())
        sys.exit(0)

try:
    with open('ogrenciler.csv','rb') as f:
        reader = csv.reader(f,delimiter=';')
        reader.next() #This skips the header line
        student_l = [Student(*row_values[:-1]) for row_values in reader]
        map(lambda x: print(x.get_info()),student_l)
except IOError:
    student_l = []

eg.msgbox("Ogrenci kayit programina hosgeldiniz","Hosgeldiniz")


###########################
#        MAIN LOOP        #
###########################
while True:
    title = "Ogrenci Kaydi"
    msg = "Lutfen hakkinda islem yapmak istediginiz ogrenciyi seciniz."
    print(student_l)
    student_list_modified = ['     -     '.join(student.get_info().values()) for student in student_l]
    chosen_student =  eg.choicebox(msg,title,student_list_modified)


    if chosen_student != BLANK_LIST_ERROR and chosen_student != None:
        chosen_student = student_l[student_list_modified.index(chosen_student)]
    

    if chosen_student:
        action = eg.buttonbox("Ne yapmak istiyorsunuz?",
                              choices=('Kaldir','Degistir','Ekle','Iptal'))
        if action == 'Kaldir':
            chosen_student.remove()
        elif action == 'Degistir':
            edit_student(chosen_student)
        elif action == 'Ekle':
            add_student(student_l)
    else:
        quit_prompt(student_l)

    



    
