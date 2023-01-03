"""
Name - Manav Sharma
Student ID - R00183839

"""


import simplejson
import threading
import socket

class Server : 
    def __init__(self, port, data:dict) : 
        self.port = port
        self.data = data
        self.running = True
        self.logs = dict()
        self.employee_ids = [x for x in data.keys()]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("0.0.0.0", self.port))
        self.s.listen()
        print('[+] Server up and running...')
        self.initiate_conn()

    def initiate_conn(self) :
        while self.running : 
            self.conn, addr = self.s.accept()
            print(addr)
            self.logs[addr[0]] = []
            threading.Thread(target=self.session, args=(self.conn,addr[0],)).start()
    def session(self, conn, ip) -> str: 
        while self.running :
            employee_id = conn.recv(1024).decode()
            self.save_logs(ip=ip, log=employee_id)
            if employee_id in self.employee_ids :
                conn.send("True".encode())
            else :
                conn.send("False".encode())
                continue
            temp_cmd = ["S" , "L"]
            cmd = self.recv_cmd(conn=conn, cmd_list=temp_cmd)
            self.save_logs(ip, cmd)
            if cmd == "S" :
                temp_cmd = ["C", "T"]
                cmd = self.recv_cmd(conn, temp_cmd, p_cmd='Current salary (C) or total salary (T) for year? ')
                self.save_logs(ip, cmd)
                if cmd.upper() == "C"  :
                    conn.send(self.data[employee_id]['salary']['current_salary'].encode())
                    if self.exit_fn(conn) :
                        break
                    continue
                else :
                    years = [x for x in self.data[employee_id]['salary']['total_salary'].keys()]
                    year = self.recv_cmd(conn=conn, years=years, p_cmd='Current Entitlement (C) or Leave taken for year (Y)? ')
                    self.save_logs(ip, year)
                    conn.send(self.data[employee_id]['salary']['total_salary'][year].encode())

                    if self.exit_fn(conn) :
                        break
                    continue
            if cmd == "L" :
                temp_cmd = ["C","Y"]
                cmd = self.recv_cmd(conn=conn,cmd_list=temp_cmd, p_cmd='Current Entitlement (C) or Leave taken for year (Y)?')
                self.save_logs(ip, cmd)
                if cmd == 'C' : 
                    conn.send(self.data[employee_id]['Annual_Leave']['current_entitlement'].encode())
                    if self.exit_fn(conn) :
                        break
                    continue
                else :
                    years = [x for x in self.data[employee_id]['Annual_Leave']['per_year'].keys()]
                    year = int(self.recv_cmd(conn=conn, years=years, p_cmd='Current Entitlement (C) or Leave taken for year (Y)? '))
                    self.save_logs(ip, year)
                    conn.send(self.data[employee_id]['Annual_Leave']['per_year'][year].encode())

                    if self.exit_fn(conn) :
                        break
                    continue
    def recv_cmd(self, conn, cmd_list:list=None, years=None, p_cmd=None) :
        print(cmd_list)
        print(p_cmd)
        if years :
            conn.send('year'.encode())
            while True : 
                year = str(conn.recv(1024).decode())
                print('year by client', year)
                if year.isdigit() : 
                    print('is digit')
                    if int(year) in years :
                        print('is year')
                        conn.send('True'.encode())
                        return int(year)
                conn.send('False'.encode())
        while True : 
            if p_cmd : 
                conn.send(p_cmd.encode())
            cmd = conn.recv(1024).decode()
            if cmd in cmd_list : 
                conn.send('True'.encode())
                return cmd
            conn.send('False'.encode())
    def exit_fn(self, conn) : 
        cmd = conn.recv(1024).decode()
        if cmd == 'quit' : 
            conn.send('Goodbye'.encode())        
            conn.close()
            return True
        elif cmd == 'cont' :
            return False
        else :
            print(cmd)
    def save_logs(self, ip, log) :
        self.logs[ip].append(log)
        print(self.logs)
        with open('logs.txt', 'w') as f:
            data = simplejson.dumps(self.logs)
            f.write(data)
            f.close()
if __name__ == '__main__' :
     # HERE IS THE EMPLOYEE DETAILS 

    employee_details = {
        "E00123" : {
            "name" : "Sherlock", 
            "salary" : {
                "current_salary" : """
            Employee Sherlock: 
            Current basic salary: 38566""",
                "total_salary" : {
                2018 : """
                Employee Sherlock: 
                Total Salary for 2018: Basic pay, 29400; Overtime, 2587 
                """,
                2019 : 
                """
                Employee Sherlock: 
                Total Salary for 2019: Basic pay, 22500; Overtime, 3177 
                """}} ,
        "Annual_Leave" :{ 
            "current_entitlement" :
        """
        Employee Sherlock: 
        Current annual leave entitlement: 25 days 
        """,
        "per_year" :
        {
            2018 : """
            Employee Sherlock: 
            Leave taken in 2018: 22 days 
            """,
            2019 : """
            Employee Sherlock: 
            Leave taken in 2019: 20 days 
            """
        }
        }           
                },
        "E01033" : {
            "name" : "John", 
            "salary" : {
                "current_salary" : """
            Employee John: 
            Current basic salary: 53577""",
                "total_salary" : {
                2018 : """
                Employee John: 
                Total Salary for 2018: Basic pay, 40000; Overtime, 2587 
                """,
                2019 : 
                """
                Employee John: 
                Total Salary for 2019: Basic pay, 55000; Overtime, 3177 
                """}} ,
        "Annual_Leave" :{ 
            "current_entitlement" :
        """
        Employee John: 
        Current annual leave entitlement: 27 days 
        """,
        "per_year" :
        {
            2018 : """
            Employee John: 
            Leave taken in 2018: 19 days 
            """,
            2019 : """
            Employee John: 
            Leave taken in 2019: 20 days 
            """
        }
        }           
                }
            }
    server = Server(port=8081, data=employee_details)

    # E00123