import sqlite3
import socket
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

IP = '0.0.0.0'
PORT = 33010
BUFSIZ = 1024

server_name="Ofek's server"

class Bank:
    """
    Constructor of class Bank
    """
    def __init__(self):
        self.moneyInBank = 0
        self.name = ""
        self.pinCode = ""
        self.accNo = 0
        self.connection()
        self.bank_action()
    """
    Function responsible for connection between server and client
    """
    def connection(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(1)
        start = "Welcome to Ofekst's bank! \n" \
                  "please choose your requested action\n" \
                  "1- for creating new account\n" \
                  "2- for entering your account\n" \
                  "7- for exit\n"
        self.client_socket, self.address = self.server_socket.accept()
        self.client_socket.send(bytes((start).encode('utf-8')))
        data = self.client_socket.recv(BUFSIZ)
        data=data.decode(('utf-8'))
        while data != '7':
            if data == '1':
                self.accNo = self.client_socket.recv(BUFSIZ)
                self.accNo = self.accNo.decode('utf-8')
                self.accNo=int (self.accNo)

                self.name = self.client_socket.recv(BUFSIZ)
                self.name = self.name.decode('utf-8')

                self.pinCode = self.client_socket.recv(BUFSIZ)
                self.pinCode = self.pinCode.decode('utf-8')

                self.moneyInBank = self.client_socket.recv(BUFSIZ)
                self.moneyInBank = self.moneyInBank.decode('utf-8')
                self.moneyInBank=int(self.moneyInBank)
                self.createAccount()
                break
            elif data == '2':
                self.accNo = self.client_socket.recv(BUFSIZ)
                self.accNo = self.accNo.decode('utf-8')
                self.accNo= int(self.accNo)
                self.sign_in()
                break
            data = self.client_socket.recv(BUFSIZ)
            data = data.decode(('utf-8'))
        if data == '7':
            self.client_socket.close()
            self.server_socket.close()
    """
    Function responsible for the bank's actions 
    """
    def bank_action(self):
        request = "Welcome to Ofekst's bank! \n" \
                  "please choose your requested action\n" \
                  "4- for deposit money\n" \
                  "5- for withdraw money\n" \
                  "6- for check your balance\n" \
                  "7- for exit\n"
        self.client_socket.send(bytes((request).encode('utf-8')))
        data = self.client_socket.recv(BUFSIZ)
        data=data.decode(('utf-8'))
        data = data.lower()
        while data != '7':
            if data == '4':
                pin = self.client_socket.recv(BUFSIZ)
                pin = pin.decode('utf-8')
                self.deposit(pin)
            elif data == '5':
                pin = self.client_socket.recv(BUFSIZ)
                pin = pin.decode('utf-8')
                self.withdraw(pin)
            elif data == '6':
                msg = self.client_socket.recv(BUFSIZ)
                msg = msg.decode('utf-8')
                self.bankBalance()
            data = self.client_socket.recv(BUFSIZ)
            data = data.decode(('utf-8'))
        self.client_socket.close()
        self.server_socket.close()
    """
    Function creates new account
    """
    def createAccount(self):
        cursor.execute("SELECT * FROM account WHERE accountNum = ?", (self.accNo,))
        data1 = cursor.fetchall()
        if len(data1) == 0:
            cursor.execute("INSERT INTO account (accountNum,name,pinCode,money) VALUES(?,?,?,?)"
                           , (self.accNo, self.name, self.pinCode, self.moneyInBank))
            self.client_socket.send(bytes(("\n\n\nAccount Created").encode('utf-8')))
        else:
            self.client_socket.send(bytes(("\n\n\nyou are already signed up").encode('utf-8')))

        conn.commit()
        rows = cursor.execute("SELECT * FROM account").fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print('nothing')
    """
    Function responsible for signing in into existing account
    """
    def sign_in(self):
        cursor.execute("SELECT * FROM account WHERE accountNum = ?", (self.accNo,))
        data1 = cursor.fetchall()
        if len(data1) == 0:
            print("Your account number is incorrect")
            self.client_socket.send(bytes(("Your account number is incorrect").encode('utf-8')))

        else:
            self.client_socket.send(bytes(("Welcome to your account").encode('utf-8')))

            rows = cursor.execute("SELECT * FROM account").fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print('nothing')

    """
    Function responsible for deposit money into existing account
    """
    def deposit(self,pin):
        cursor.execute("SELECT pinCode FROM account WHERE accountNum = ?", (self.accNo,))
        cur_pin = cursor.fetchall()
        for r in cur_pin:
            self.pinCode = r[0]
        if pin == self.pinCode:
            mes="How much money do you want to deposit?"
            self.client_socket.send(bytes(mes.encode('utf-8')))
            dep = self.client_socket.recv(BUFSIZ)
            dep = dep.decode('utf-8')
            dep = int(dep)


            cursor.execute("SELECT money FROM account WHERE accountNum = ?", (self.accNo,))
            cur_money = cursor.fetchall()
            for r in cur_money:
                money = r[0]

            self.moneyInBank = money
            self.moneyInBank = money + dep
            print("deposit completed\ntotal money in Bank is:{} ".format(self.moneyInBank))
            self.client_socket.send(bytes(("deposit completed\ntotal money in Bank is:{} ".format(self.moneyInBank)).encode('utf-8')))

            sentence = "UPDATE account SET money= :new_money WHERE accountNum= :accNum "
            cursor.execute(sentence, {"accNum": self.accNo, "new_money": self.moneyInBank}, )
            conn.commit()
        else:
            print("Incorrect PIN number")
            self.client_socket.send(bytes(("Incorrect PIN number.").encode('utf-8')))

        rows = cursor.execute("SELECT * FROM account").fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print('nothing')

    """
    Function responsible for withdraw money from existing account
    """
    def withdraw(self,pin):

        cursor.execute("SELECT pinCode FROM account WHERE accountNum = ?", (self.accNo,))
        cur_pin = cursor.fetchall()
        for r in cur_pin:
            self.pinCode = r[0]
        if pin == self.pinCode:
            cursor.execute("SELECT money FROM account WHERE accountNum = ?", (self.accNo,))
            cur_money = cursor.fetchall()
            for r in cur_money:
                money = r[0]
            self.moneyInBank = money

            mes="How much money do you want to withdraw?"
            self.client_socket.send(bytes(mes.encode('utf-8')))
            wid = self.client_socket.recv(BUFSIZ)
            wid = wid.decode('utf-8')
            wid = int(wid)
            if wid > self.moneyInBank:
                print("You don't have enough money in bank")
                self.client_socket.send(bytes(("You don't have enough money in bank").encode('utf-8')))
            else:
                self.moneyInBank = self.moneyInBank - wid
                print("withdraw completed\ntotal money in Bank is:{} ".format(self.moneyInBank))
                self.client_socket.send(bytes(("withdraw completed\ntotal money in Bank is:{} "
                                               .format(self.moneyInBank)).encode('utf-8')))

                sentence = "UPDATE account SET money= :new_money WHERE accountNum= :accNum "
                cursor.execute(sentence, {"accNum": self.accNo, "new_money": self.moneyInBank}, )
                conn.commit()
        else:
            self.client_socket.send(bytes(("Incorrect PIN number.").encode('utf-8')))
        rows = cursor.execute("SELECT * FROM account").fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print('nothing')

    """
    Function returns the balance of existing account
    """
    def bankBalance(self):
        if self.accNo==0:
            self.client_socket.send(bytes(("You must enter your account first").encode('utf-8')))
        else:
            cursor.execute("SELECT money FROM account WHERE accountNum = ?", (self.accNo,))
            id_row = cursor.fetchall()
            for r in id_row:
                id = r[0]
            self.moneyInBank = id
            print("Your balance at this current time is:{} ".format(self.moneyInBank))
            self.client_socket.send(bytes(("Your balance at this current time is:{} "
                                           .format(self.moneyInBank)).encode('utf-8')))

def main():
    Bank()

if __name__ == '__main__':
    main()
