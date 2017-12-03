# polskie znaki
#-*- coding: utf-8 -*-

import pymysql
from Haslo.password import Haslo

class Logowanie:
    def __init__(self):
        self.instrukcja()
        self.conn = Haslo.password()
              
        while True:
            choice = input("\n\nWciśnij C,B lub Q: ")
            if choice.upper() == "C":
                self.czytelnik()                
                                
            elif choice.upper() == "B":
                self.bibliotekarz()
                
            elif choice.upper() == "Q":
                print('''
                         ____                   _     _               _            __  
                        |  _ \  ___   __      _(_) __| |_______ _ __ (_) __ _   _  \ \ 
                        | | | |/ _ \  \ \ /\ / / |/ _` |_  / _ \ '_ \| |/ _` | (_)  | |
                        | |_| | (_) |  \ V  V /| | (_| |/ /  __/ | | | | (_| |  _   | |
                        |____/ \___/    \_/\_/ |_|\__,_/___\___|_| |_|_|\__,_| (_)  | |
                                                                                   /_/
                ''')
                break            
            else: 
                print("\nWcisnąłeś zły przycisk! \nWciśnij C - żeby zalogować się jako czytelnik \nlub B - żeby zalogować się jako Bibliotekarz, Q - wyjście")
                continue
    
    def instrukcja(self):
        print('''
                    
                     ____  _ _     _ _       _       _          
                    | __ )(_) |__ | (_) ___ | |_ ___| | ____ _  
                    |  _ \| | '_ \| | |/ _ \| __/ _ \ |/ / _` | 
                    | |_) | | |_) | | | (_) | ||  __/   < (_| | 
                    |____/|_|_.__/|_|_|\___/ \__\___|_|\_\__,_| 
                                             
        
        ''')
        print('''\t\t\tWitaj w panelu logowania Biblioteki.\n\nJeśli chcesz zalogować się jako Czytelnik wciśnij - C,
        \njeśli jako biblotekarz wciśnij - B \n\njeśli chcesz opuścić program wciśnij Q''')
   
    def czytelnik(self):
        email = input("Podaj email: ")
        haslo = input("Podaj hasło: ")
        cursor = self.conn.cursor()
        id_klienta = cursor.execute("select id_klienta from czytelnik where email='"+email+"' and password='"+haslo+"';")
        results = cursor.fetchall()
        for row in results:
            id_klienta = row[0]
            if id_klienta > 0:
                czytelnik = Czytelnik(id_klienta)
            else:   
                print('Login lub hasło błędne\nWybierz ponownie jako kto chcesz się zalogować(C,B) lub wyjdź(Q)')
                        
                       
    def bibliotekarz(self):
        login = input("Podaj login: ")
        haslo = input("Podaj hasło: ")
        cursor = self.conn.cursor()
        id_b = cursor.execute('select id_b from bibliotekarz where login=\''+login+'\' and password=\''+haslo+'\';')
        results = cursor.fetchall()
        for row in results:
            self.id_b = row[0]
            if id_b > 0:
                bibliotekarz = Bibliotekarz(id_b)
            else:   
                print('Login lub hasło błędne\nWybierz ponownie jako kto chcesz się zalogować(C,B) lub wyjdź(Q)')
            
        
'''////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''  

class Czytelnik(Logowanie):
 
    def __init__(self,id_klienta):
        self.instruction()
        self.id_klienta = id_klienta
        self.conn = Haslo.password()
        while True:
            choice = input('Wpisz cyfrę: ')
            if choice == '1':
                self.wolne_ksiazki()
            elif choice == '2':
                self.zamowienie()
                self.conn.commit()
            elif choice == '3':
                self.stan_konta()
            elif choice == '4':
                self.usuwanie_zamowienia()
                self.conn.commit()
            elif choice == '5':
                print('Wylogowano poprawnie.')
                break           
            else:
                print('!!!Wybrałeś niedostępną opcję!!!')
                print('1 - sprawdzenie książek, 2 - zamówienie, 3 - stan konta, 4 - usuwanie zamówienia, 5 - wylogowanie')
                continue
        
    def instruction(self):
        print('\nWitaj Czytelniku co chcesz zrobić?\n\nSprawdzic dostępne w tej chwili ksiazki (1),\n\nZłożyć zamówienie (2)'+
              '\n\nSprawdzic stan swojego konta (3), \n\nUsuwanie zamówienia (4),\n\nWylogowanie (5)\n' )
        
    def instruction2(self):
        print('\nWitaj spowrotem w menu głównym. Co chcesz zrobić?')
        print('\n\nSprawdzic dostępne w tej chwili ksiazki (1),\n\nZłożyć zamówienie (2)'+
              '\n\nSprawdzic stan swojego konta (3), \n\nUsuwanie zamówienia (4),\n\nWylogowanie (5)\n' )
    
    def wolne_ksiazki(self):
        cursor = self.conn.cursor()
        cursor.execute('select*from wolne_ksiazki;')
        print ('|%+10s|%-45s|%-10s|%-11s|%-10s|'%('id ksiązki','tytuł','kategoria','rok wydania', 'krótki opis'))
        for i in range(cursor.rowcount):
            rec = cursor.fetchone()
            print (('|%+10s|%-45s|%-10s|%-11s|%-10s|')%(rec[0], rec[1], rec[2], rec[3], rec[4]))       
        self.instruction2()
    
    def zamowienie(self):
        print('Dokonaj zamówienia wpisując id_książki')
        book = input('Podaj id_książki: ')
        self.cursor = self.conn.cursor()
        self.cursor.execute('insert into zamowienia (id_z, id_klienta, data_zamowienia) values (%s, %s, curdate());' , (0 , self.id_klienta))
        self.cursor.execute("select id_z from zamowienia where id_klienta = %s and data_zamowienia = curdate();", (self.id_klienta))
        results = self.cursor.fetchall()
        for row in results:
            self.id_z = row[0]
        try:    
            self.cursor.execute('insert into zamowienia_ksiazki values (%s,%s);', (self.id_z, book))
        except:
            print("Wpisałeś zły znak lub próbujesz wypożyczyć zajętą książkę sprawdź dostępne książki poprzez wybranie 3 w menu głównym")
        while True:
            
            pytanie = input("Czy chcesz dodać więcej książek do tego zamówienia? T/N")
            
            if pytanie.upper() == 'T':
                book = int(input('Podaj id_książki: '))
                self.cursor = self.conn.cursor()
                try:
                    self.cursor.execute('insert into zamowienia_ksiazki values (%s, %s);',(self.id_z, book))
                except:
                    print("Próbujesz wypożyczyć zajętą książkę sprawdź dostępne poprzez wybranie 3 w menu głównym")
                    
            elif  pytanie.upper() == 'N':
                self.instruction2()
                break
            else:
                print('!!!Wybrałeś niedostępną opcję!!!')
                print('dodanie nowej ksiazki - T, wyjscie - N ')
                continue
            
                        
    def stan_konta(self):
        cursor = self.conn.cursor()
        cursor.execute('select * from zamowienia_klienci_ksiazki where id_klienta= (%s);', self.id_klienta)
        print ('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|'%('id_książki','tytuł','id_z','id_klienta', 'Imię', 'Nazwisko', 'data_zamowienia', 'data_odbioru', 'termin_zwrotu', 'data_zwrotu'))
        for i in range(cursor.rowcount):
            rec = cursor.fetchone()
            print (('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|')%(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9]))       
        self.instruction2()
        
    def usuwanie_zamowienia(self):
        print('Jeśli zamówienie zostanie poprawnie usunięte wygenerowany zostanie komunikat w przeciwnym wypadku znajdziesz się spowrotem w menu głównym.')
        cursor = self.conn.cursor()
        id_zamowienia = input('Podaj id_zamowienia które chcesz usunąć lub wciśnij Q aby wyjść: ')
        cursor.execute('select data_odbioru from zamowienia_klienci_ksiazki where id_z= %s;', id_zamowienia)
        result = cursor.fetchall()
        for row in result:
            result = row[0]        
            if result == None:
                cursor.execute("delete from zamowienia_ksiazki where id_z= %s;", id_zamowienia)
                cursor.execute("delete from zamowienia where id_z= %s;", id_zamowienia)
                print("Zamówienie zostało usunięte.")
                input("\nWciśnij enter by przejść do menu głównego")               
            else:
                print("Próbujesz usunąć zamówienie, które zostało odebrane w dniu", result)
                input("\nWciśnij enter by przejść do menu głównego")
        self.instruction2()       
            
        
'''////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''     
        
class Bibliotekarz:
    def __init__(self, id_b):
        self.instruction()
        self.id_b = id_b;
        self.conn = Haslo.password()
        while True:
            choice = input('Wpisz cyfrę: ')
            if choice == '1':
                self.lista()
            elif choice == '2':
                self.sprawdzanie_id_z()
            elif choice == '3':
                self.odbior()
                self.conn.commit()
            elif choice == '4':
                self.rozliczanie_zamowienia()
                self.conn.commit()
            elif choice == '5':
                print('Wylogowano poprawnie')
                break           
            else:
                print('!!!Wybrałeś niedostępną opcję!!!')
                print('1 - lista zamówien, 2 - sprawdzanie id zamówienia danej książki, 3 - dodawanie daty odbioru ksiązki, 4 - usuwanie zamówienia, 5 - wylogowanie')
                continue
        
    def instruction(self):
        print('\nWitaj Bibliotekarzu co chcesz zrobić?\n\nZobaczyć listę wypożyczeń (1) \n\nSprawdzić id zamówienia danej książki (2),\n\nDodać datę odbioru książki (3),\n\nUsunąć zamówienie (4),\n\nWyjść (5)\n' )
    def instruction2(self):
        print('\nMenu główne\n-------------\nCo chcesz zrobić?\n\nZobaczyć listę wypożyczeń (1) \n\nSprawdzić id zamówienia danej książki (2),\n\nDodać datę odbioru książki (3),\n\nUsunąć zamówienie (4),\n    \nWyjść (5)\n' )
    def lista(self):
        cursor = self.conn.cursor()
        cursor.execute("select * from zamowienia_klienci_ksiazki;")
        print ('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|'%('id_książki','tytuł','id_z','id_klienta', 'Imię', 'Nazwisko', 'data_zamowienia', 'data_odbioru', 'termin_zwrotu', 'data_zwrotu'))
        for i in range(cursor.rowcount):
            rec = cursor.fetchone()
            print (('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|')%(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9]))
            
        while True:
            pytanie = input("\n\nCzy chcesz sprawdzic książki nieodebrane (1) odebrane i niezwrócone (2) lub niezwrócone w terminie (3) (Q) - wyjście do menu głównego ")
            
            if pytanie == '1':
                cursor = self.conn.cursor()
                cursor.execute("select * from zamowienia_klienci_ksiazki where data_odbioru is null;")
                print ('\n\n|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|'%('id_książki','tytuł','id_z','id_klienta', 'Imię', 'Nazwisko', 'data_zamowienia', 'data_odbioru', 'termin_zwrotu', 'data_zwrotu'))
                for i in range(cursor.rowcount):
                    rec = cursor.fetchone()
                    print (('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|')%(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9]))
                
            elif pytanie == '2':
                cursor = self.conn.cursor()
                cursor.execute("select * from zamowienia_klienci_ksiazki where data_zwrotu is null and termin_zwrotu is not null;")
                print ('\n\n|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|'%('id_książki','tytuł','id_z','id_klienta', 'Imię', 'Nazwisko', 'data_zamowienia', 'data_odbioru', 'termin_zwrotu', 'data_zwrotu'))
                for i in range(cursor.rowcount):
                    rec = cursor.fetchone()
                    print (('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|')%(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9]))
            
            elif pytanie == '3':
                cursor = self.conn.cursor()
                cursor.execute("select * from zamowienia_klienci_ksiazki where termin_zwrotu < curdate();")
                print ('\n\n|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|'%('id_książki','tytuł','id_z','id_klienta', 'Imię', 'Nazwisko', 'data_zamowienia', 'data_odbioru', 'termin_zwrotu', 'data_zwrotu'))
                for i in range(cursor.rowcount):
                    rec = cursor.fetchone()
                    print (('|%+10s|%-45s|%-5s|%-11s|%-10s|%-10s|%-15s|%-15s|%-15s|%-15s|')%(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[                9]))
                                    
            elif  pytanie.upper() == 'Q':
                self.instruction2()
                break
            else:
                print('!!!Wybrałeś niedostępną opcję!!!')
                print(' wybierz 1,2,3 lub Q wyjście ')
                continue
        
    def sprawdzanie_id_z(self):
        print("Jeśli podana ksiązka jest przedmiotem zamówienia wyświetli się komunikat.\nW przeciwnym wypadku zostaniesz przeniesiony do menu głównego.")
        cursor = self.conn.cursor()
        pytanie = input("Podaj id książki, której nr zamówienia chcesz sprawdzić? (Enter wyjście do menu głównego)")
        cursor.execute("select id_z from zamowienia_ksiazki where id_k = %s;", (pytanie))
        results = cursor.fetchall()
        for row in results:
            id_z = row[0]
            if id_z >= 0:
                print("Nr zamówienia podanej książki to: ", id_z)
                input("Jeśli chcesz przejść do menu głównego wciśnij Enter")
            else:
                print("Nie ma takiego zamówienia")
        self.instruction2()
         
    def rozliczanie_zamowienia(self):
        cursor = self.conn.cursor()
        id_zamowienia = input("Podaj nr zamówienia, które chcesz usunąć: ")
        id_ksiazki = input("Podaj id książki, którego zamowienie dotyczy: ")
        id_klienta = input("Podaj id klienta: ")
        cursor.execute("select * from zamowienia_klienci_ksiazki where id_z =%s and id_k = %s and id_klienta = %s;", (id_zamowienia, id_ksiazki, id_klienta));
        results = cursor.fetchall()  
        if len(results) > 0:
            cursor.execute("insert into historia_zamowien values (%s,%s, %s, %s)", (0, id_zamowienia, id_ksiazki, id_klienta))
            cursor.execute("delete from zamowienia_ksiazki where id_z = %s and id_k = %s;", (id_zamowienia, id_ksiazki));
            cursor.execute("select * from zamowienia_ksiazki where id_z =% s", (id_zamowienia));
            results = cursor.fetchall()
            if len(results) == 0:
                cursor.execute("UPDATE zamowienia SET data_zwrotu = curdate() WHERE id_z = %s;", (id_zamowienia))
                cursor.execute("select termin_zwrotu, data_zwrotu from zamowienia WHERE id_z = %s;", (id_zamowienia))
                results = cursor.fetchall()
                for row in results:
                    self.termin_zwrotu = row[0]  
                    self.data_zwrotu = row[1]

                    if self.termin_zwrotu >= self.data_zwrotu:
                        cursor.execute("delete from zamowienia where id_z = %s;", (id_zamowienia));
                        print("Zamówienie zostało usunięte")
                        self.instruction2()
                    else:
                        cursor.execute("insert into kary values (0, %s, (select id_klienta from zamowienia where id_z =%s), ((DATEDIFF((select data_zwrotu from zamowienia where id_z = %s), (select termin_zwrotu from zamowienia where id_z = %s)))*0.5));",(id_zamowienia, id_zamowienia,id_zamowienia, id_zamowienia))
                        cursor.execute("select kwota from kary WHERE id_z = %s;", (id_zamowienia))
                        results = cursor.fetchall()
                        for row in results:
                            kwota = row[0] 
                            print("Kwota kary ", kwota)
                            cursor.execute("delete from zamowienia where id_z = %s;", (id_zamowienia));
            
            elif len(results) > 0:
                cursor.execute("UPDATE zamowienia SET data_zwrotu = curdate() WHERE id_z = %s;", (id_zamowienia))
                cursor.execute("select termin_zwrotu, data_zwrotu from zamowienia WHERE id_z = %s;", (id_zamowienia))
                results = cursor.fetchall()
                for row in results:
                    self.termin_zwrotu = row[0]  
                    self.data_zwrotu = row[1]
                    if self.termin_zwrotu >= self.data_zwrotu:
                        cursor.execute("delete from zamowienia where id_z = %s;", (id_zamowienia));
                        print("Zamówienie zostało usunięte")
                        self.instruction2()                        
                    else:
                        cursor.execute("insert into kary values (0, %s, (select id_klienta from zamowienia where id_z =%s), ((DATEDIFF((select data_zwrotu from zamowienia where id_z = %s), (select termin_zwrotu from zamowienia where id_z = %s)))*0.5));",(id_zamowienia, id_zamowienia,id_zamowienia, id_zamowienia))
                        cursor.execute("select kwota from kary WHERE id_z = %s;", (id_zamowienia))
                        results = cursor.fetchall()
                        for row in results:
                            kwota = row[0]  
                            print("Kwota kary ", kwota)
                            cursor.execute("UPDATE zamowienia SET data_zwrotu = null WHERE id_z = %s;", (id_zamowienia));
        
            self.instruction2()
        
        else:
            print("Nie ma takiego zamówienia")
            self.instruction2()
            
    def odbior(self):
        cursor = self.conn.cursor()
        print("Jeśli chcesz dodać datę odbioru podaj nr zamówienia, jeśli chcesz wyjść kliknij Enter i N")
        print("Jeśli data odbioru zostanie poprawnie dodana wyświetli się komunikat. Data odbioru tej książki to: dzisiejsza data.\nJeżeli książka została już odebrana wcześniej wyświetli się data jej odbioru.")
        id_zamowienia = input("\nPodaj nr zamówienia do którego chcesz dodać datę odbioru: ")
        cursor.execute("UPDATE zamowienia SET data_odbioru = curdate(), termin_zwrotu = DATE_ADD(curdate(), INTERVAL 30 DAY) WHERE id_z = %s and data_odbioru is null;", id_zamowienia)
        cursor.execute("select data_odbioru from zamowienia WHERE id_z = %s;", (id_zamowienia))
        results = cursor.fetchall()
        for row in results:
            data_odbioru = row[0]
        print("Data odbioru tej książki to: ", data_odbioru)
        while True:
            pytanie = input("Czy chcesz dodać kolejne daty zamówienia (T)ak, (N)ie: ")
            if pytanie.upper() == "T":
                cursor = self.conn.cursor()
                id_zamowienia = input("Podaj nr kolejnego zamówienia do którego chcesz dodać datę odbioru: ")
                cursor.execute("UPDATE zamowienia SET data_odbioru = curdate(), termin_zwrotu = DATE_ADD(curdate(), INTERVAL 30 DAY) WHERE id_z = %s and data_odbioru is null;", id_zamowienia)                
                cursor.execute("select data_odbioru from zamowienia WHERE id_z = %s;", (id_zamowienia))
                results = cursor.fetchall()
                for row in results:
                    data_odbioru = row[0]
                print("Data odbioru tej książki to: ", data_odbioru)              
            elif pytanie.upper() == "N":
                break;
            else:
                print("Wybrałeś niedostępną opcję")
                continue
        self.instruction2()   
        
log = Logowanie()
#czyt = Czytelnik(3)
#bib = Bibliotekarz(1)


    