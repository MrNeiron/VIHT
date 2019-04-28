import sqlite3
from os.path import basename
import re

class DB:
    def __init__(self, path):
        self.name_database = basename(path)#name_database
        self.conn = sqlite3.connect(path)
        self.dataTypes = {}
        self.notNulls = {}
        self.table_names = self._get_table_names()
        self.messageNothing = "Ничего не найдено"
        for name_table in self.table_names:
            self.dataTypes[name_table] = self._get_table_types(name_table)
            self.notNulls[name_table] = self._get_table_notNulls(name_table)

        
    def Create_table(self, name_table, *fields):
        try:
            cur = self.conn.cursor()
            table_fields = ", ".join(fields)
            cur.execute(f"CREATE TABLE IF NOT EXISTS {name_table} ({table_fields})")
            
            self.table_names.append(name_table)
            self.dataTypes[name_table] = self._get_table_types(name_table)
            self.notNulls[name_table] = self._get_table_notNulls(name_table)  
            
            self.conn.commit()
        except:
            if self.conn:
                self.conn.rollback()
            print("Error table")
          
    def Add_values(self, name_table, fields, data, print_logs = False):
        try:
            message = ''
            for i,(field, new_value) in enumerate(zip(fields, data)):
                try:
                    new_value = int(new_value)
                    if self.dataTypes[name_table][field] == "text":
                        message = "Не соответствие типов: Поле типа 'text' не может быть 'integer'"
                        return message
                    elif self.dataTypes[name_table][field] == "date":
                        message = "Не соответствие типов: Поле типа 'date' не может быть 'integer'"
                        return message
                except:
                    if new_value == '' or new_value == '(Null)':
                        if self.notNulls[name_table][field] == 1:
                            message = "Значение не может быть нулевым."
                        else:
                            data[i] = '(Null)'
                    elif self.dataTypes[name_table][field] == "integer":
                        message += "Не соответствие типов: Ожидалось поле типа 'integer'"
                        return message
                    elif self.dataTypes[name_table][field] == "real":
                        try:
                            new_value = float(new_value)
                        except:
                            message += "Не соответствие типов: Ожидалось поле типа 'real'"
                            return message
                    elif self.dataTypes[name_table][field] == "date" and (not re.match(r'[0-3][0-9][..][0-1][0-9][..]\d\d\d\d', new_value) or len(new_value) != 10):
                        message = "Не соответствие типов: Ожидалось поле типа 'date'"
                        return message

            cur = self.conn.cursor()
            table_fields = self._join_fields(fields)
            table_data = self._join_data(data)
            if print_logs:
                print("table_fields = ", table_fields)
                print("table_data = ", table_data)
    
            cur.execute(f"INSERT INTO {name_table}({table_fields}) VALUES({table_data})")
            self.conn.commit()
            rowcount = cur.rowcount
            if print_logs:
                print("Row count: ", rowcount)
                print("Success")
        except:
            if self.conn:
                self.conn.rollback()
            print("Error add values")
        finally:
            return message
        
    def Get_values(self, name_table, fields = None, mode = None, print_logs = False):
        try:
            cur = self.conn.cursor()
            if mode is not None and mode == "all":
                cur.execute(f"SELECT * FROM {name_table}")
            else:
                table_fields = self._join_fields(fields)
                cur.execute(f"SELECT {table_fields} FROM {name_table}")
            values = cur.fetchall()
            rowcount = len(values)
            message = self.messageNothing if rowcount == 0 else f"Найдена {rowcount} строка" if (rowcount%100 < 11 or rowcount % 100 > 19) and rowcount % 10 == 1  else f"Найдены {rowcount} строки" if (rowcount%100 < 11 or rowcount % 100 > 19) and 1 < rowcount % 10 < 5 else f"Найдено {rowcount} строк"
            if print_logs:
                print("Values = ", values)
                print("Row count: ", rowcount)
                print("Success")
            return values,message
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
                
    def Get_values_condition(self, name_table, search_field, value, equal = '=', table_fields = None, mode = "all", print_logs = False):
        try:
            cur = self.conn.cursor()
            
            if table_fields is not None: table_fields = self._join_fields(table_fields)
                
            if mode is not None and mode == "all":
                cur.execute(f"SELECT * FROM {name_table} WHERE {search_field} {equal} '{value}'")
            else:
                cur.execute(f"SELECT {table_fields} FROM {name_table} WHERE {search_field} {equal} '{value}'")
                
            values = cur.fetchall()
            rowcount = len(values)
            message = self.messageNothing if rowcount == 0 else f"Найдена {rowcount} строка" if (rowcount%100 < 11 or rowcount % 100 > 19) and rowcount % 10 == 1  else f"Найдены {rowcount} строки" if (rowcount%100 < 11 or rowcount % 100 > 19) and 1 < rowcount % 10 < 5 else f"Найдено {rowcount} строк"          
            if print_logs:
                print("Values = ", values)
                print("Row count: ", rowcount)
                print("Success")
                
            return values,message
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
            
    def Get_values_condition_extend(self, name_table, search_fields, equals, values, and_or_equals, table_fields = None, mode= "all", print_logs = False):
        try:
            
            cur = self.conn.cursor()
            
            and_or_equals = ("AND" if and_or_equal=="И" else "OR" if and_or_equal=="ИЛИ" else '' for and_or_equal in and_or_equals)
            if table_fields is not None: table_fields = self._join_fields(table_fields)
            
            if print_logs:
                print("[log] Table_fields = ", table_fields)
                print("[log] Search_fields = ", search_fields)
            
            expressions = []
            for search_field,equal,value,and_or_equal in zip(search_fields,equals,values,and_or_equals):
                if self.dataTypes[name_table][search_field]=="integer":
                    expressions.append(search_field+equal+str(value)+' '+and_or_equal)
                else:
                    expressions.append(search_field+equal+f"'{value}' "+and_or_equal)

            expressions = ' '.join(expressions)
            if mode is not None and mode=="all":
                cmd = f"SELECT * FROM {name_table} WHERE " + expressions
            else:
                cmd = f"SELECT {table_fields} FROM {name_table} WHERE " + expressions
            cur.execute(cmd)
            values = cur.fetchall()
            rowcount = len(values)
            message = self.messageNothing if rowcount == 0 else f"Найдена {rowcount} строка" if (rowcount%100 < 11 or rowcount % 100 > 19) and rowcount % 10 == 1  else f"Найдены {rowcount} строки" if (rowcount%100 < 11 or rowcount % 100 > 19) and 1 < rowcount % 10 < 5 else f"Найдено {rowcount} строк"
            if print_logs:
                print("[LOG] Cmd = ", cmd)
                print("[LOG] Table fields = ", table_fields)
                print("[LOG] Value = ", values)
                print("[LOG] Row count: ", rowcount)
            return values, message
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
                
    def Update_row(self, name_table, update_field, new_value, search_item, print_logs = False):
        try:
            message = ''
            cur = self.conn.cursor()
            try:
                new_value = int(new_value)
                if self.dataTypes[name_table][update_field] == "text":
                    message = "Не соответствие типов: Поле типа 'text' не может быть 'integer'"
                    return message
                elif self.dataTypes[name_table][update_field] == "date":
                    message = "Не соответствие типов: Поле типа 'date' не может быть 'integer'"
                    return message
            except: 
                if new_value == '' or new_value == '(Null)':
                    if self.notNulls[name_table][update_field] == 1:
                        message = "Значение не может быть нулевым"
                        return message
                    else:
                        new_value = '(Null)'
                elif self.dataTypes[name_table][update_field] == "integer":
                    message = "Не соответствие типов: Поле типа 'integer' не может быть 'text'"
                    return message
                elif self.dataTypes[name_table][update_field] == "real":
                    try:
                        new_value = float(new_value)
                    except:
                        message += "Не соответствие типов: Ожидалось поле типа 'real'"
                        return message      
                elif self.dataTypes[name_table][update_field] == "date" and (not re.match(r'[0-3][0-9][..][0-1][0-9][..]\d\d\d\d', new_value) or len(new_value) != 10):
                    message = "Не соответствие типов: Ожидалось поле типа 'date'"
                    return message
                    
               
            cur.execute(f"UPDATE {name_table} SET {update_field} = '{new_value}' WHERE ID = '{search_item}'")
                
            self.conn.commit()
            rowcount = cur.rowcount
            
            if print_logs:
                print("Row count: ", rowcount)
                print("Success")
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
        finally:
            return message
        
        
    def Del_row(self, name_table, value, print_logs = False):
        try:
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM {name_table} WHERE ID == '{value}'")
            self.conn.commit()
            rowcount = cur.rowcount
            if print_logs: 
                print("Row count: ", rowcount)
                print("Success")
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
            
                
    def ItemsInColumn(self, name_table, field):
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT DISTINCT {field} FROM {name_table}")
            value = cur.fetchall()
            return value if len(value) <= 200 else value[:201]
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")    

                
    def _get_table_names(self):
        
        cur = self.conn.execute(f"SELECT * FROM sqlite_master WHERE type = 'table'")

        names = [desc[1] for desc in cur.fetchall()]
        return names
    
    def _get_table_types(self, name_table, print_logs = False):
        try:
            cur = self.conn.cursor()
            cur.execute(f"PRAGMA TABLE_INFO({name_table})")
            values = cur.fetchall()
            return_types = {column[1]:column[2] for column in values}
            rowcount = cur.rowcount
            if print_logs:
                print("[LOG] Return_types = ", return_types)
                print("[LOG] Row count: ", rowcount)
                print("[LOG] Success")
            return return_types
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
            
            
    def _get_table_notNulls(self, name_table, print_logs = False):
        try:
            cur = self.conn.cursor()
            cur.execute(f"PRAGMA TABLE_INFO({name_table})")
            values = cur.fetchall()
            return_notNulls = {column[1]:column[3] for column in values}
            rowcount = cur.rowcount
            if print_logs:
                print("[LOG] Return_notNulls = ", return_notNulls)
                print("[LOG] Row count: ", rowcount)
                print("[LOG] Success")
            return return_notNulls
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")     
    
    def Get_columns_names(self, name_table):
        
        cur = self.conn.execute(f"SELECT * FROM {name_table}")
        
        names = [name[0] for name in cur.description]
        return names
                
    def _join_fields(self, lst):
        lst = ['"'+l+'"' if ' ' in l else l for l in lst]
        
        return ", ".join(lst)
    
    def _join_data(self, lst):
        lst = ['"'+l+'"' if type(l) is str else str(l) for l in lst]
        
        return ", ".join(lst)
    
    def Execute(self, cmd, print_logs = False):
        try:
            cur = self.conn.cursor()
            cur.execute(cmd)
            values = cur.fetchall()
            rowcount = cur.rowcount
            if print_logs:
                print("Values = ", values)
                print("Row count: ", rowcount)
                print("Success")
            return values
        except IOError:
            if self.conn:
                self.conn.rollback()
            print("Error")
    
    def Close(self):
        self.conn.close()  

if __name__ == "__main__":
    myDB = DB("Databases/myTable.db")
    #myDB.Create_table("employeers", "ID integer PRIMARY KEY", "ID_department integer", "Name text NOT NULL", "Last_name text NOT NULL", "", "Hire_date date NOT NULL", "Salary real NOT NULL")
    
    myDB.Create_table("employeers", 
    """
    ID integer PRIMARY KEY,
    ID_department integer,
    Position text NOT NULL,
    Name text NOT NULL,
    Last_name text NOT NULL,
    Second_name text,
    Age integer NOT NULL,
    Sex text NOT NULL,
    Salary real NOT NULL,
    Hire_date date NOT NULL,
    Experience integer,
    Birth_date date NOT NULL,
    Childs integer
    """
    )
    print(    myDB.Add_values("employeers", ["ID", "ID_department", "Position", "Name", "Last_name", "Second_name", "Age", "Sex", "Salary", "Hire_date", "Experience", "Birth_date", "Childs"], [1,    1, "Lecturer", "Ivan", "Ivanov", "Ivanovich", 40, 'м', 30000, '12.03.2006', 12, "12.12.1978", 2], False))

    
    myDB.Create_table("classes", 
    """
    ID integer PRIMARY KEY,
    Name text NOT NULL,
    Duration_sem int NOT NULL,
    Last_change_date date
    """
    )   
    print(    myDB.Add_values("classes", ["ID", "Name", "Duration_sem", "Last_change_date"], [1, "История", 2, '12.12.2016'], False))

    myDB.Create_table("students", 
    """
    ID integer PRIMARY KEY,
    Name text NOT NULL,
    Last_name text NOT NULL,
    Second_name text,
    Class integer NOT NULL,
    Age integer NOT NULL,
    Sex text NOT NULL,
    Birth_date date NOT NULL,
    Study_form text NOT NULL,
    Education text NOT NULL,
    Last_visit date
    """
    )
    print(    myDB.Add_values("students", ["ID", "Name", "Last_name", "Second_name", "Class", "Age", "Sex", "Birth_date", "Study_form", "Education", "Last_visit"], [1, "Сергей", "Сергеев", "Сергеевич", 3, 20, 'м', '23.10.1999', "очная", "среднее", '12.12.2016'], False))
    
    myDB.Close()