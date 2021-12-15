import sqlite3
import os

def main():
    f = open("kw.sql", "w+")
    
    conn = sqlite3.connect("kw.sql")
    cur = conn.cursor()
    
    command = 'CREATE TABLE employee(id VARCHAR(6) PRIMARY KEY, name VARCHAR(20), lastname VARCHAR(20), position VARCHAR(20), experience INT, residence VARCHAR(30), salary FLOAT, hiring_date DATE, company_id VARCHAR(6), project_id VARCHAR(6))'
    execute(cur, command, conn)
    
    command = 'CREATE TABLE company(id VARCHAR(6), name VARCHAR(20), hq VARCHAR(30), money FLOAT)'
    execute(cur, command, conn)
    
    command = 'CREATE TABLE project(id VARCHAR(6), name VARCHAR(20), difficulty INT, return FLOAT)'
    execute(cur, command, conn)
    
    command = 'CREATE TABLE required_resources(project_id VARCHAR(6), resource_id VARCHAR(20), amount FLOAT)'
    execute(cur, command, conn)
    
    command = 'CREATE TABLE resources_owned_by_company(company_id VARCHAR(6), resource_id varchar(20), amount FLOAT)'
    execute(cur, command, conn)
    
    command = 'CREATE TABLE resource(name VARCHAR(20), price FLOAT)'
    execute(cur, command, conn)
    
    cur.close()
    conn.close()

def execute(cur, command, conn):
    cur.execute(command)
    conn.commit()

if __name__ == '__main__':
    main()


#Sql, py project - conect python GUI with sql data base
#
#Bastian Lipka -
