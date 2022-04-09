# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:48:00 2021

@author: KAIZEN
"""

import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS course (
                        id INTEGER PRIMARY KEY, 
                        course_name text, 
                        student text,
                        gender text,
                        test_1 integer,
                        test_2 integer,
                        project integer,
                        exam integer,
                        total_score real, 
                        position integer)"""),
        self.conn.commit()
        
        
    def fetch(self):
        self.cur.execute("SELECT * FROM course")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, course_name, student, gender, test_1, test_2, project, exam, total_score, position):
        self.cur.execute("INSERT INTO course VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (course_name, student, gender, test_1, test_2, project, exam, total_score, position))
        self.conn.commit()
        
    def remove(self, id):
        self.cur.execute("DELETE FROM course WHERE id=?", (id,))
        self.conn.commit()
        
    def update(self, id, course_name, student, gender, test_1, test_2, project, exam, total_score, position):
        self.cur.execute("UPDATE course SET course_name = ?, student = ?, gender = ?, test_1 = ?, test_2 = ?, project = ?, exam = ?, total_score = ?, position = ? WHERE id = ?", (course_name, student, gender, test_1, test_2, project, exam, total_score, position, id))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()
        
db = Database('school.db')   


db.insert("Computer Appreciation", "Asake Ibrahim", "Female", "12", "11", "10", "45", "0", "0")
db.insert("Computer Appreciation", "Folake Ogunsanya", "Female", "12", "9", "10", "45", "0", "0")
db.insert("Computer Appreciation", "Dada Cletus", "Male", "11", "11", "10", "45", "0", "0")
db.insert("Computer Appreciation", "Brem Wilson", "Female", "6", "11", "7", "52", "0", "0")
db.insert("Computer Appreciation", "Obus Tony", "Male", "8", "11", "8", "32", "0", "0")
