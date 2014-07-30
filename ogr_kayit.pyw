import easygui as eg
import sys
import csv
from collections import OrderedDict

BLANK_LIST_ERROR = 'Program logic error - no choices were specified.'
PROPERTIES = ("Ad","Soyad","Universite","OSYM Puani",
              "Yili","CBUTF Taban Puani","Not Ortalamasi",
              "Sinif","Egitim","Disiplin Cezasi","Telefon","Uygunluk")
ALIGN_WIDTH = 25


class Student(object):
    def calc_puan(self):
        if self.osym_puani != '' and self.cbutf_puani != '' and self.not_ortalamasi != '':
            self.puan = '{:.3f}'.format((float(self.osym_puani)/float(self.cbutf_puani))*100 + float(self.not_ortalamasi))
        else:
            self.puan = ''

    def __init__(self, name, surname, university,
                 osym_puani, year, cbutf_puani, not_ortalamasi,
                 sinif, egitim, disiplin, telefon, uygunluk):
        self.name = name
        self.surname = surname
        self.university = university
        self.year = year
        self.osym_puani = osym_puani
        self.cbutf_puani = cbutf_puani
        self.not_ortalamasi = not_ortalamasi
        self.sinif = sinif
        self.egitim = egitim
        self.disiplin = disiplin
        self.telefon = telefon
        self.uygunluk = uygunluk
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
                            ('sinif',self.sinif),
                            ('egitim',self.egitim),
                            ('disiplin',self.disiplin),
                            ('telefon',self.telefon),
                            ('uygunluk',self.uygunluk),
                            ('puan',self.puan)])

    def edit(self, values):
        (self.name,self.surname,self.university,self.osym_puani,
         self.year,self.cbutf_puani,self.not_ortalamasi,self.sinif,
         self.egitim,self.disiplin,self.telefon,self.uygunluk) = values
        self.calc_puan()

    def export_for_csv(self):
        return self.get_info().values()

def str_to_student(chosen_student,student_list):
    for student in student_list:
        if student == chosen_student:
            return student

def add_student(student_list):
    values = eg.multenterbox(msg='Ogrenci bilgilerini giriniz:',
                            title='Ogrenci bilgisi', 
                            fields=PROPERTIES, values=())

    if values:
        new_student = Student(*values)
        student_list.append(new_student)

def edit_student(chosen_student):
    updated_values = eg.multenterbox(msg='Ogrenci bilgilerini giriniz:',
                                    title='Ogrenci bilgisi', fields=PROPERTIES,
                                    values=chosen_student.get_info().values())
    if updated_values:
        chosen_student.edit(updated_values)

def find_student(student_l):
    #TO BE IMPLEMENTED
    pass


def sort_students(student_list):
    return sorted(student_list,key=lambda x: x.osym_puani)

def quit_prompt(student_list):
    if eg.ynbox("Cikmak istediginize emin misiniz?",choices=('Evet','Hayir')):
        with open('ogrenciler.csv','wb') as f:
            writer = csv.writer(f,delimiter=';')
            writer.writerow(['AD','SOYAD','UNIVERSITE','OSYM PUANI','YILI',
                             'CBUTF TABAN PUANI','NOT ORTALAMASI','SINIF',
                             'EGITIM','DISIPLIN CEZASI','TELEFON','UYGUNLUK','PUAN'])
            student_list = sort_students(student_list)
            for student in student_list:
                writer.writerow(student.export_for_csv())
        sys.exit(0)

def align_output(values):
    output = ''
    for item in values:
        pad = ALIGN_WIDTH - len(item)
        txt = item + pad*' '
        output += txt
    return output


try:
    with open('ogrenciler.csv','rb') as f:
        reader = csv.reader(f,delimiter=';')
        reader.next() #This skips the header line
        #Read all values but 'puan', it is not an argument of 'Student'
        student_l = [Student(*row_values[:-1]) for row_values in reader] 

except IOError:
    student_l = []

eg.msgbox("Ogrenci kayit programina hosgeldiniz","Hosgeldiniz")


###########################
#        MAIN LOOP        #
###########################
while True:
    title = "Ogrenci Kaydi"
    msg = "Lutfen hakkinda islem yapmak istediginiz ogrenciyi seciniz."

    #Sort the 'Student' objects' list everytime the loop runs.

    student_l.sort(key=lambda x: x.puan,reverse=True)
    student_list_modified = []

    #Add the index of the item at the beginning of its representing string.
    #It maintains the sorted order.

    for i,v in enumerate(student_l, 1):
        values = v.get_info().values()[:]
        values.insert(0,str(i))
        #student_list_modified.append('     -     '.join(values))
        student_list_modified.append(align_output(values))
    
    chosen_student =  eg.choicebox(msg,title,student_list_modified)

    if chosen_student != BLANK_LIST_ERROR and chosen_student is not None:
        chosen_student = student_l[student_list_modified.index(chosen_student)]

    if chosen_student:
        action = eg.buttonbox("Ne yapmak istiyorsunuz?",
                              choices=('Kaldir','Degistir','Ekle','Ara','Iptal'))
        if action == 'Kaldir':
            chosen_student.remove()
        elif action == 'Degistir':
            edit_student(chosen_student)
        elif action == 'Ekle':
            add_student(student_l)
        elif action == 'Ara':
            find_student(student_l)
    else:
        quit_prompt(student_l)

    



    
