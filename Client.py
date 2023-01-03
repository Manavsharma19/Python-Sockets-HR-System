"""
Name - Manav Sharma
Student ID - R00183839

"""


import socket

class Client : 
    def __init__(self, ip, port) : 
        self.ip = ip
        self.port = port
        self.running = True

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            self.s.connect((self.ip, self.port))
        except :
            print('please enter the correct ip address and port no of the server...\nExiting')
            exit()
        print('[+] connected ')
        self.session()

    def session(self) :
        while self.running :
            employee_id = str(input('What is the employee id? '))
            self.s.send(employee_id.encode())
            res = eval(self.s.recv(1024).decode())
            if res == True : 
                while self.running :
                    cmd = str(input('Salary (S) or Annual Leave (L) Query? ')).upper()
                    self.s.send(cmd.encode())
                    res =self.s.recv(1024).decode()
                    if res == 'True' :
                        while self.running : 
                            p_cmd = self.s.recv(1024).decode()
                            cmd = str(input(p_cmd))
                            # exception here
                            self.s.send(cmd.encode())
                            res = self.s.recv(1024).decode()
                            if res == 'True' :
                                result = self.s.recv(1024).decode()
                                if result == 'year' : 
                                    while True : 
                                        year = str(input('What year? '))
                                        self.s.send(year.encode())
                                        res = self.s.recv(1024).decode()
                                        if res == 'True' : 
                                            result = self.s.recv(1024).decode()
                                            print(result)
                                            self.exit_fn(self.s)
                                            self.session()
                                            break
                                        elif res == 'False'  : 
                                            print('[-] Invalid Year')
                                            continue
                                        else  :
                                            continue
                                else :
                                    print(result)
                                    self.exit_fn(self.s)
                                    break
                            elif res == 'False' :
                                print('[-] invalid command')
                                continue
                        break
                    else  : 
                        print('[-] Invalid Command ')
            else :
                print('[-] Invalid ID ')
                                


    def exit_fn(self, conn) :
        cmd = str(input('Would you like to continue (C) or exit (X)? '))          
        if cmd.lower() == 'x' : 
            conn.send('quit'.encode()) 
            msg = conn.recv(1024).decode()
            exit(0)
        elif cmd.lower() == 'c' :
            conn.send('cont'.encode())
            pass


if __name__ == '__main__'  :
    client = Client(ip='192.168.100.8', port=8081)