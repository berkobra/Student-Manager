# -*- coding: latin1 -*-

import unittest
import student as std

global testStud
testStud = std.Student('Berk','Özkutuk','',322,'',300,90,'','','','','')


class Tests(unittest.TestCase):

    def test_student_name(self):
        self.assertEqual(repr(testStud),'Berk Özkutuk')

    def test_student_eq(self):
        self.assertEqual(testStud,'Berk Özkutuk')

    def test_calc(self):
        self.assertEqual(testStud.puan, '197.333')

    def test_find(self):
        std_list = [testStud]
        self.assertIn(repr(testStud), std_list)

    def test_sort1(self):
        Stud1 = std.Student('Şadiye','Suku','','','','','','','','','','')
        Stud2 = std.Student('Çimen','Suku','','','','','','','','','','')
        std_list = [Stud1, Stud2]
        self.assertEqual(std.sort_students(std_list), [Stud2, Stud1])

    def test_sort2(self):
        Stud1 = std.Student('Şadiye','Suku','İ uni','','','','','','','','','')
        Stud2 = std.Student('Çimen','Suku','Ü uni','','','','','','','','','')
        std_list = [Stud1, Stud2]
        self.assertEqual(std.sort_students(std_list, attr='university'), [Stud1, Stud2])


if __name__ == '__main__':
    unittest.main()


