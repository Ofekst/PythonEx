import socket
import sys

HOST = '127.0.0.1'
PORT = 33010
BUFSIZ = 1024
ADDR = (HOST, PORT)

class ATM:
    """
    Constructor of class ATM
    """
    def __init__(self):
        self.my_socket = socket.socket()
        self.account=0
        self.connection()
        self.bank_actions()
    """
    Function responsible for connection between server and client
    """
    def connection(self):
        try:
            self.my_socket.connect((HOST, PORT))
        except:
            print("The server is not availible")
            self.my_socket.close()
            sys.exit()

        start_message = self.my_socket.recv(BUFSIZ)
        start_message = start_message.decode()
        print(start_message)
        message = input("")

        while message != "7":
            self.my_socket.send(message.encode())
            if message == '1':
                while True:
                    try:
                        accNo = int(input("Enter the account number : "))
                        if accNo <= 0:
                            print("Incorrect account number. ")
                        else:
                            break
                    except:
                        print("Incorrect account number. ")
                accNo=str(accNo)
                self.my_socket.send(bytes(accNo.encode('utf-8')))
                name = input("Enter the account holder name : ")
                self.my_socket.send(bytes(name.encode('utf-8')))
                while True:
                    pinCode = input("Enter PIN number (must be 4 digit) : ")
                    if len(pinCode) != 4:
                        print("Incorrect PIN number. ")
                    else:
                        try:
                            int_pin = int(pinCode)
                            if int_pin <= 0:
                                print("Incorrect PIN number. ")
                            else:
                                break
                        except:
                            print("Incorrect PIN number. ")
                self.my_socket.send(bytes(pinCode.encode('utf-8')))
                moneyInBank = int(input("Enter your starting amount of money: "))
                moneyInBank=str(moneyInBank)
                self.my_socket.send(bytes(moneyInBank.encode('utf-8')))
                answer = self.my_socket.recv(BUFSIZ)
                answer = answer.decode('utf-8')
                print(answer)
                break
            elif message == '2':
                account_number=input("Enter the account number : ")
                self.my_socket.send(bytes(account_number.encode('utf-8')))
                answer = self.my_socket.recv(BUFSIZ)
                answer = answer.decode('utf-8')
                print(answer)
                break
            message = input("Enter new request:")

        if message=='7':
            print("bye bye")
            self.my_socket.close()
            sys.exit()
    """
    Function responsible for the ATM's actions 
    """
    def bank_actions(self):
       # print("here")
        start_message = self.my_socket.recv(BUFSIZ)
        start_message = start_message.decode()
        print(start_message)
        message = input("")
        while message != "7":
            self.my_socket.send(message.encode())
            if message == '4':
                while True:
                    pin = int(input("Enter your PIN number "))
                    pin = str(pin)

                    if len(pin) != 4:
                        print("Incorrect PIN number.")
                    else:
                        try:
                            int_pin = int(pin)
                            if (int_pin <= 0):
                                print("Incorrect PIN number.")
                            else:
                                break

                        except:
                            print("Incorrect PIN number.")

                self.my_socket.send(bytes(pin.encode('utf-8')))
                money_to_dep = self.my_socket.recv(BUFSIZ)
                money_to_dep = money_to_dep.decode('utf-8')

                print(money_to_dep)

                how_much_money = input("")
                self.my_socket.send(bytes(how_much_money.encode('utf-8')))
                total_money = self.my_socket.recv(BUFSIZ)
                total_money = total_money.decode('utf-8')
                print(total_money)

            elif message == '5':
                while True:
                    pin = int(input("Enter your PIN number "))
                    pin = str(pin)

                    if len(pin) != 4:
                        print("Incorrect PIN number.")
                    else:
                        try:
                            int_pin = int(pin)
                            if (int_pin <= 0):
                                print("Incorrect PIN number.")
                            else:
                                break
                        except:
                            print("Incorrect PIN number.")

                self.my_socket.send(bytes(pin.encode('utf-8')))
                money_to_wid = self.my_socket.recv(BUFSIZ)
                money_to_wid = money_to_wid.decode('utf-8')
                print(money_to_wid)
                how_much_money = input("")
                self.my_socket.send(bytes(how_much_money.encode('utf-8')))
                total_money = self.my_socket.recv(BUFSIZ)
                total_money = total_money.decode('utf-8')
                print(total_money)

            elif message == '6':
                path = 'balance'
                self.my_socket.send(bytes(path.encode('utf-8')))
                total_money = self.my_socket.recv(BUFSIZ)
                total_money = total_money.decode('utf-8')
                print(total_money)
            message = input("Enter new request:")
        print("bye bye")
        self.my_socket.close()
        sys.exit()
def main():
    ATM()

if __name__ == '__main__':
    main()
