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

import student as std
import easygui as eg
import csv


csv_file = eg.fileopenbox(title='Tabloyu ac',filetypes=['*.csv'])
if csv_file:
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        reader.next()  # This skips the header line
        #Read all values but 'puan', it is not an argument of 'Student'
        student_l = [std.Student(*row_values[:-1]) for row_values in reader]
else:
    student_l = []

#Intro message
#Can display the 'About' section or move on to the program
intro_choice = eg.buttonbox("Ogrenci kayit programina hosgeldiniz","Hosgeldiniz",choices=('Devam','Hakkinda'))
if intro_choice == 'Hakkinda':
    eg.msgbox("""Copyright (C) 2014  Berk Ozkutuk
    Bu program GPL lisansina sahiptir.
    Daha fazla bilgi icin LICENSE.txt dosyasina bakiniz.""")

#variables which are passed to the choicebox function.
title = "Ogrenci Kaydi"
msg = "Lutfen hakkinda islem yapmak istediginiz ogrenciyi seciniz.\n"
msg_veriler = str(std.PROPERTIES + ('Puan',))
msg += msg_veriler

#Default sorting parameters
sort_param = 'osym_puani'
reverse_param = True

while True:
    #Sort the "Student" objects' list everytime the loop runs.
    student_l = std.sort_students(student_l,sort_param, reverse=reverse_param)
    student_list_modified = []

    #Add the index of the item at the beginning of its representing string.
    #It maintains the sorted order.
    for i,v in enumerate(student_l, 1):
        values = v.get_info().values()[:]
        values.insert(0,str(i))
        student_list_modified.append(std.align_output(values))
    
    #modified list is displayed, values in original list are preserved.
    chosen_student =  eg.choicebox(msg,title,student_list_modified)

    #Ensures that chosen_student is a string representation of a Student object.
    if chosen_student != std.BLANK_LIST_ERROR and chosen_student is not None:
        chosen_student = student_l[student_list_modified.index(chosen_student)]

    if chosen_student:
        action = eg.buttonbox("Ne yapmak istiyorsunuz?",
                              choices=('Kaldir','Degistir','Ekle','Ara','Sirala','Iptal'))
        if action == 'Kaldir':
            student_l.remove(chosen_student)
        elif action == 'Degistir':
            std.edit_student(chosen_student)
        elif action == 'Ekle':
            std.add_student(student_l)
        elif action == 'Ara':
            std.find_student(student_l)
        elif action == 'Sirala':
            sort_choice = eg.buttonbox("Siralama parametresini seciniz.",
                              choices=('Ad soyad',)+std.PROPERTIES[2:]+('Puan',))
            sort_param, reverse_param = std.sort_param_getter(sort_choice)
    else:
        std.quit_prompt(student_l)

    



    
