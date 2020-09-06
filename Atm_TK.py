import os
import time
import fileinput
import tkinter as tk
from tkinter import filedialog, Text
clear = lambda: os.system('cls')
mesaj_intampinare = True

try:
    # verificam daca fisierul "Accounts.txt exista"
    f = open("Accounts.txt","r")
    f.close()
    # daca acest fiesier nu exista atunci cream unul
except FileNotFoundError:
    f = open("Accounts.txt", "w")
    f.close()




def create_account(lista_conturi):

    name = input("Nume: ").upper()
    pin = input("PIN: ")
    pin_confirm = input("Confirmati PIN-ul:")
    balance = 100

    if pin_confirm != pin:
        while True :
            print("Asigurati-va ca pinurile sunt indentice !")
            pin_confirm = input("Reconfirmati PIN-ul:")
            if pin_confirm == pin:
                break
    else:
            
            f = open("Accounts.txt","a")
            data =  name +" "+ pin +" "+ str(balance)
            f.write(data + '\n')
            print("Va rugam sa asteptati pana se creaza contul.")
            f.close()
            time.sleep(2)
            return lista_conturi
            
def update_user_data(lista_conturi, this_user_list):
    lista_conturi = read_file("Accounts.txt")
    for users in lista_conturi:
        if this_user_list[0]  == users[0] and this_user_list[1] == users[1]:
            this_user_list[2] = users[2]

    return this_user_list


def log_in(lista_conturi, nume_en, pin_en):
    lista_conturi = read_file('Accounts.txt') #updateaza lista de conturi cu noul coninut din "Accounts.txt" 
    #                                          (in cazul in care se creaza un user nou)
    print("Pentru a va conecta introduceti datele contului dumneavoastra.")
    user_name =nume_en.get().upper() #input("Nume utilizator>> ").upper() 
    user_pin = pin_en.get().upper()  #input("PIN>> ") 

    autentificare = False
    for list in lista_conturi:
        if (user_name == list[0] and user_pin == list[1]):
            print("Autentificare reusita\n\nWelcome {}!".format(user_name.capitalize()))
            logged_in_menu(list)
            #print(lista_conturi[1][0])
            autentificare = True
            break
        else:
            continue

    if not autentificare:
        clear()
        print("Nume utilizator sau PIN gresit!\n Va rugam sa reincercati.")
        time.sleep(2)
        
    

def read_file (file):
    opened_file = open(file, 'r')
    lines_list = []
    for line in opened_file:
        line = line.split()
        lines_list.append(line)
    return lines_list


def logged_in_menu (this_user_list):    #list cu datele utilizaotrului care a trecut de logg in
    update_user_data(lista_conturi,this_user_list)
    time.sleep(2)
    clear()
    logged_choice = int(input("[1]Interogare sold\n[2]Retragere numerar\n" +
        "[3]Depozitare numerar\n[4]Transfer intre conturi\n[5]Exit\n\nchoice>> "))
    
    if logged_choice == 1:
        print("Sold curent: {}".format(this_user_list[2]))
        logged_in_menu(this_user_list)

    elif logged_choice == 2:
        withdraw(this_user_list)

    elif logged_choice == 3:
        deposit(this_user_list)

    elif logged_choice == 4:
        transfer(this_user_list)

    elif logged_choice == 5:
        exit
        # logout or smt
    else:
        print("Ne pare rau, nu va putem ajuta. Incercati o optiune din lista afisata!")
        time.sleep(2)
        clear()
        logged_in_menu(this_user_list)


def withdraw(tul_withdraw):
    amount_to_withraw = int(input("Va rugam sa introduceti suma pe care doriti sa o retrageti.\nAmount>> "))
    choice = int(input("Suma pe care doriti sa o retrageti este: {} \nSuma este corecta?\n[1] DA\t[2] NU\n\nchoice>> ".format(amount_to_withraw)))
    if choice == 1:
        user_balance = int(tul_withdraw[2])
        if amount_to_withraw > user_balance:
            print("Fonduri insuficiente!")
            logged_in_menu(tul_withdraw)
        else:
            user_init_balance = tul_withdraw[2]
            user_balance -= amount_to_withraw
            print("New balance: {}".format(user_balance))
            with fileinput.FileInput("Accounts.txt", inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace(str(" "+ user_init_balance +"\n"),str(" "+ str(user_balance) +"\n")), end='')
            logged_in_menu(tul_withdraw)
        
    elif choice == 2:
        withdraw(tul_withdraw)
    else:
        print("Ne pare rau, nu va putem ajuta. Incercati o optiune din lista afisata!")
        withdraw(tul_withdraw)
    return tul_withdraw


def deposit(tul_deposit):
    user_balance = int(tul_deposit[2])
    amount_to_deposit = int(input("Introduceti suma pe care doriti sa o depozitati: "))
    choice = int(input("Doriti sa depozitati suma de {} coco\n[1] DA\n[2] NU\nchoice>> ".format(amount_to_deposit)))
    if choice == 1:
        user_balance += amount_to_deposit
        print("New balance {}".format(user_balance))
        user_init_balance = tul_deposit[2]

        with fileinput.FileInput("Accounts.txt", inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(str(" "+ user_init_balance +"\n"),str(" "+ str(user_balance) +"\n")), end='')
        logged_in_menu(tul_deposit)

    elif choice == 2:
        ch = int(input("[1] Alta suma\n[2] Catre meniul principal\nchoice>> "))
        if ch == 1:
            deposit(tul_deposit)
        elif ch == 2:
            logged_in_menu(tul_deposit)

    else:
        print("Ne pare rau, nu va putem ajuta. Incercati o optiune din lista afisata!")
        deposit(tul_deposit)
    return tul_deposit

def transfer(tul_transfer):
    recipient = input("Introduceti numele destinatarului>> ").upper()
    amount_to_transfer = int(input("Introduceti suma pe care doriti sa o virati destinatarului>> "))
    choice = int(input("Doriti sa trimiteti suma de {} coco catre {}?\n[1] DA\t[2] NU\nchoice>> ".format(amount_to_transfer, recipient.capitalize())))
    if choice == 1:
        user_pin = input("Introduceti pinul>> ")
        if user_pin == tul_transfer[1]:
            if amount_to_transfer > int(tul_transfer[2]):
                print("Fonduri insuficiente !")
                time.sleep(2)
                logged_in_menu(tul_transfer)
            else:
                lista_utilizatori = read_file('Accounts.txt')

                user_found = False
                for list in lista_utilizatori:
                    if recipient == list[0]:
                        recipient_data = list
                        user_found = True
                        break
                    else:
                        continue

                if user_found:
                    recipient_balance = int(recipient_data[2])
                    recipient_balance += amount_to_transfer
                    print("Tranzactia a avut succes!\nNew balance {}".format(int(tul_transfer[2]) - amount_to_transfer))
                    
                    #inlocuire date this_user
                    user_init_balance = tul_transfer[2]
                    user_new_balance = int(tul_transfer[2]) - amount_to_transfer
                    
                    with fileinput.FileInput("Accounts.txt", inplace=True, backup='.bak') as file:
                        for line in file:
                            print(line.replace(str(" "+ user_init_balance +"\n"),str(" "+ str(user_new_balance) +"\n")), end='')
                    
                    #inlocuire date recipient
                    recipient_init_balance = recipient_data[2]

                    with fileinput.FileInput("Accounts.txt", inplace=True, backup='.bak') as file:
                        for line in file:
                            print(line.replace(str(" "+ recipient_init_balance +"\n"),str(" "+ str(recipient_balance) +"\n")), end='')
                    
                    recipient_data[2] = str(recipient_balance)
                    time.sleep(2)
                    logged_in_menu(tul_transfer)

                if not user_found:
                    print("Something went wrong, please verify recipient data and try again!")
                    ch = int(input("[1] Schimba destinatar \n[2] Catre meniul principal\nchoice>> "))
                    if ch == 1:
                        transfer(tul_transfer)
                    else:
                        logged_in_menu(tul_transfer)
                    
                    time.sleep(2)
                    



        else:
            print("PIN incorect !")
            time.sleep(2)
            transfer(tul_transfer)
    
    return tul_transfer

def exit_message():
    print(">>>>>>>>>>>>>>> La revedere! <<<<<<<<<<<<<<<")


lista_conturi = read_file('Accounts.txt')
print(">>>>>>>>>>>>>>> Bine ati venit! <<<<<<<<<<<<<<<")
count = True






root = tk.Tk()
#canvas = tk.Canvas(root,height= 100, width = 100, bg = "#263D42")
#canvas.pack()
root.mainloop


def tk_logIn ():
    child = tk.Tk()
    child.mainloop
    canvas = tk.Canvas(child,height= 300, width = 300, bg = "#263D42")
    canvas.pack()  
    frame = tk.Frame(child, bg="grey")
    frame.place(relwidth = 0.8, relheight = 0.4, relx = 0.1, rely = 0.1)

    tk.Label(frame, text="Nume", bg="grey").grid(row=0)
    tk.Label(frame, text="PIN", bg="grey").grid(row=1)

    
    nume_en = tk.Entry(frame)
    pin_en = tk.Entry(frame)

    nume_en.grid(row=0, column=1)
    pin_en.grid(row=1, column=1)

    child_login = tk.Button(child, text="LogIn", padx=15, pady=10, fg="white", 
    bg="#263D42", command=lambda: log_in(lista_conturi, nume_en, pin_en)) #, command=lambda: log_in(lista_conturi)
    child_login.pack(fill=tk.X)





logIn = tk.Button(root, text="LogIn", padx=75, pady=10, fg="white", 
bg="#263D42", command= tk_logIn) #, command=lambda: log_in(lista_conturi)
logIn.pack(fill=tk.X)

newAccount = tk.Button(root, text="Cont nou", padx=75, pady=10, fg="white", bg="#263D42")
newAccount.pack(fill=tk.X)

exit_bt = tk.Button(root, text="Exit", padx=75, pady=10, fg="white", bg="#263D42")
exit_bt.pack(fill=tk.X)



#def tk_log_in():
#tk.Label(frame, text="Nume", bg="grey").grid(row=0)
#tk.Label(frame, text="PIN", bg="grey").grid(row=1)

#nume_en = tk.Entry(frame)
#pin_en = tk.Entry(frame)

#nume_en.grid(row=0, column=1)
#pin_en.grid(row=1, column=1)









while count:
    choice = int(input("\n [1] LogIn\n [2] Creaza cont nou\n [3] Exit\n\nchoice>> "))

    if(choice == 1):
        #log_in(lista_conturi)
        clear()
    elif(choice == 2):
        create_account(lista_conturi)
        clear()
    elif(choice == 3):
        clear()
        exit_message()
        time.sleep(2)
        clear()
        break
    else:
        print("Ne pare rau, nu va putem ajuta. Incercati o optiune din lista afisata!")