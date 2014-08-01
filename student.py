# A little GUI program to handle student data and import/export them as CSV.
#     Copyright (C) 2014  Berk Ozkutuk
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     I can be reached at: berkozkutuk@gmail.com

import easygui as eg
import sys
import csv
from collections import OrderedDict
from operator import attrgetter

PROPERTIES = ("Ad", "Soyad", "Universite", "OSYM Puani",
              "Yili", "CBUTF Taban Puani", "Not Ortalamasi",
              "Sinif", "Egitim", "Disiplin Cezasi", "Telefon", "Uygunluk")
BLANK_LIST_ERROR = 'Program logic error - no choices were specified.'
ALIGN_WIDTH = 25

class Student(object):
    """Class representing a student.
       Holds all the information related to the student.
    """
    def calc_puan(self):
        """Calculates the final score based on the other scores.
           If any of the other scores is empty, returns an empty string.
        """
        if all((self.osym_puani, self.cbutf_puani, self.not_ortalamasi)):
            self.puan = '{:.3f}'.format(
            (float(self.osym_puani)/float(self.cbutf_puani))*100 + float(self.not_ortalamasi)
            )
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
        return '{} {}'.format(self.name, self.surname)

    def __eq__(self, other):
        """Allows comparing Student objects with strings.
           Used for finding Student objects with fullnames.
        """
        if isinstance(other, str):
            return repr(self) == other

    def get_info(self):
        """Returns student info as an OrderedDict.
           Order matters because the output values 
           are passed into the student editing form 
           as default values.
        """
        return OrderedDict([('name', self.name),
                            ('surname', self.surname),
                            ('university', self.university),
                            ('osym_puani', self.osym_puani),
                            ('year', self.year),
                            ('cbutf_puani', self.cbutf_puani),
                            ('not_ortalamasi', self.not_ortalamasi),
                            ('sinif', self.sinif),
                            ('egitim', self.egitim),
                            ('disiplin', self.disiplin),
                            ('telefon', self.telefon),
                            ('uygunluk', self.uygunluk),
                            ('puan', self.puan)])

    def edit(self, values):
        """Updates student info with given tuple.
           Final score is calculated again with new values.
        """
        (self.name, self.surname, self.university, self.osym_puani,
         self.year, self.cbutf_puani, self.not_ortalamasi, self.sinif,
         self.egitim, self.disiplin, self.telefon, self.uygunluk) = values
        self.calc_puan()

    def export_for_csv(self):
        return self.get_info().values()

def add_student(student_list):
    """Adds student with given values to the Student objects' list.
    """
    values = eg.multenterbox(msg='Ogrenci bilgilerini giriniz:',
                            title='Ogrenci bilgisi',
                            fields=PROPERTIES, values=())

    if values:
        new_student = Student(*values)
        student_list.append(new_student)


def edit_student(chosen_student):
    """Edits the student with given values.
       The student's current info is filled in the form.
    """
    updated_values = eg.multenterbox(msg='Ogrenci bilgilerini giriniz:',
                                    title='Ogrenci bilgisi', fields=PROPERTIES,
                                    values=chosen_student.get_info().values())
    if updated_values:
        chosen_student.edit(updated_values)


def find_student(student_list):
    """Searchs for the Student object with given fullname in student_list.
       If found, opens up the Student's form, otherwise displays a message.
    """
    fullname = eg.enterbox(msg='Aramak istediginiz ogrencinin tam adini giriniz', title='Ogrenci Ara')
    for student in student_list:
        if student == fullname:  # Student object's __eq__ returns fullname so this code is okay.
            edit_student(student)
            break
    else:
        eg.msgbox(msg='Aradiginiz ogrenci bulunamadi!', title='Hata')


def sort_students(student_list,attr='osym_puani',reverse=False):
    """
    Returns a sorted copy of the student_list sorted by the given attr.
    If given attr is 'name', sorting is done as: 'name' 'surname'
    Else, sorting is done as: 'attr' 'name' 'surname'
    reverse parameter is directly passed into sorted() functions.
    """
    if attr != 'name':
        return sorted(student_list,key=attrgetter(attr,'name','surname'),reverse=reverse)
    else:
        return sorted(student_list,key=attrgetter('name','surname'),reverse=reverse)


def sort_param_getter(choice):
    """
    Returns a tuple of sorting criteria and reverse parameter.
    choice is what user sees in the actual program.
    value returned from paramdict based on choice is the related
    class attribute of Student object.
    reverse parameter is True for scores, otherwise False.
    """
    paramdict = {'Ad soyad':'name',
                 'Universite':'university',
                 'OSYM Puani':'osym_puani',
                 'Yili':'year',
                 'CBUTF Taban Puani':'cbutf_puani',
                 'Not Ortalamasi':'not_ortalamasi',
                 'Sinif':'sinif',
                 'Egitim':'egitim',
                 'Disiplin Cezasi':'disiplin',
                 'Telefon':'telefon',
                 'Uygunluk':'uygunluk',
                 'Puan':'puan'}

    if choice in ('OSYM Puani','CBUTF Taban Puani','Not Ortalamasi','Puan'):
        reverse = True
    else:
        reverse = False
    return paramdict[choice],reverse


def quit_prompt(student_list):
    """Asks if the user wants to quit or not.
       If yes, saves the student_list as a CSV file.
    """
    if eg.ynbox("Cikmak istediginize emin misiniz?", choices=('Evet', 'Hayir')):
        csv_file = eg.filesavebox(title='Tabloyu kaydet',filetypes=['*.csv'])

        #Adds .csv extension if user did not already.
        if csv_file:
            if csv_file[-4:] != '.csv':
                csv_file += '.csv'

            with open(csv_file, 'wb') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['AD', 'SOYAD', 'UNIVERSITE', 'OSYM PUANI', 'YILI',
                                 'CBUTF TABAN PUANI', 'NOT ORTALAMASI', 'SINIF',
                                 'EGITIM', 'DISIPLIN CEZASI', 'TELEFON', 'UYGUNLUK', 'PUAN'])
                student_list = sort_students(student_list)
                for student in student_list:
                    writer.writerow(student.export_for_csv())
            sys.exit(0)
        else:
            choice = eg.buttonbox(msg='Kaydetmeden cikmak istediginize emin misiniz?',
                                  title='Kaydetmeden cikis',choices=('Evet','Hayir'))
            if choice:
                sys.exit(0)


def align_output(values):
    """aligns the output of a Student object.
       result will be displayed in the listbox.
    """
    #TODO improve this method
    output = ''
    for item in values:
        pad = ALIGN_WIDTH - len(item)
        txt = item + pad*' '
        output += txt
    return output