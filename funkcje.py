import pandas as pd
import numpy as np
import os
"""Definicje klas obiektów"""

"""Klasa czas"""
class Time():

    def __init__(self,czas = "0:0:0"):
        czas = czas.split(':')
        self.czas = float(czas[0]) * 3600 + float(czas[1]) * 60 + float(czas[2])

    def __float__(self):
        return self.czas

    def __int__(self):
        return self.czas

    def __str__(self):
        g = int(self.czas / 3600)
        m = int((self.czas - g * 3600) / 60)
        s = self.czas - g * 3600 - m * 60
        t = '{:02d}:{:02d}:{:06.3f}'.format(g, m, s)
        return t

    def dodaj(self, t):
        self.czas = t


"""Klasa punkt"""
class Point():

    def __init__(self,Nr = '', X = 0, Y = 0, Hel = 0, H = 0, dok = "", depth = 0):
        self.Nr = Nr
        self.X = X
        self.Y = Y
        self.Hel = Hel
        self.H = H
        self.dok = dok
        self.depth = depth

"""Definicje funkcji"""

"""Wczytywanie pomiarowych sondy"""
def load_sonda(nazwa):
    data = pd.read_csv(nazwa)
    depth =np.array(data['Depth'].to_list())
    time = np.array(data['TimeOffset[ms]'].to_list())
    return depth, time

"""Wczytywanie danych pomiarowych GPS"""
def load_excel(nazwa):
    data = pd.read_excel(nazwa,'Arkusz1',header=None,)
    numer = np.array(data[0].to_list())
    rozwiazanie = np.array(data[1].to_list())
    time = np.array(data[2].to_list())
    Y = np.array(data[3].to_list())
    X = np.array(data[4].to_list())
    H = np.array(data[5].to_list())
    return numer, rozwiazanie, time, X, Y, H

def load_model(nazwa):
    data = pd.read_excel(nazwa,'Arkusz1')
    Y = data['Y'].to_list()
    X = data['X'].to_list()
    N = data['N'].to_list()
    undulacja = []
    for i, un in enumerate(X):
        tmp=[]
        tmp.append(float(un))
        tmp.append(float(Y[i]))
        tmp.append(float(N[i]))
        tmp.append(0)
        undulacja.append(tmp)
    return undulacja

"""Wczytywanie parametrow pomiaru"""
def load_par(nazwa):
    with open(nazwa,'r') as plik:
        li = plik.readlines()
        h = float(li[1].rstrip().lstrip())
        t = li[3].rstrip().lstrip()
        t=Time(t)
    return t, h

"""Wczytywanie czasów wybranych soundingów"""
def load_czas(nazwa, nazwa_sondowania):
    czas = []
    tmp = False
    son = nazwa_sondowania.split('.')[0]
    with open(nazwa, 'r') as plik:
        linie = plik.readlines()
        for li in linie:
            li=li.rstrip()
            li=li.lstrip()
            if li == son:
                tmp = True
                continue
            if tmp:
                if li == '':
                    break
                else:
                    czas.append(li)
    return czas

"""Zapisanie punktów do pliku"""
def save_excel(sciezka,lista):
    x = []
    y = []
    Hel = []
    Hort = []
    dok = []
    numer = []
    for  i, li in enumerate(lista):
        numer.append(li.Nr)
        x.append(li.X)
        y.append(li.Y)
        Hel.append(li.Hel)
        Hort.append(li.H)
        dok.append(li.dok)
    pkt = {
        'Numer' : numer,
        'X' : x,
        'Y' : y,
        'H_elips' : Hel,
        'H_ort' : Hort,
        'Dokładność' : dok
    }
    df = pd.DataFrame(pkt)
    df.to_excel(sciezka)
    print("Liczba zapisanych punktów: ",len(x))


"""Obliczenie czasu zerowego na podstawie wybranego soundingu"""
def obl_czas_zerowy(zero, saund):
    zerowy = Time()
    zerowy.czas = zero[1].czas - saund[zero[0]] / 1000
    return  zerowy

"""Obliczenie czsu sredniego"""
def czas_sredni(lista):
    suma = 0
    vv = 0
    for i in lista:
        suma += i.czas
    t = Time()
    t.czas = suma / len(lista)
    for i in lista:
        vv += (i.czas - t.czas) ** 2
    m0 =Time()
    m0.czas = np.sqrt(vv/(len(lista)-1))

    return t , m0


def printt(lista):
    for i in lista:
        print(i)

"""Wyszukiwanie określonego czasu"""
def szukac_czasu(lista,czas):
    try:
        return lista.index(czas)
    except ValueError:
        return 'brak danych'



"""Wyszukiwanie indeksu okreslonego punktu"""
def szukac_index(i,time_gps):
    if (i.czas - int(i.czas)) <= 0.5:
        index = szukac_czasu(time_gps, int(i.czas))
        if index == 'brak danych':
            index = szukac_czasu(time_gps, int(i.czas) + 1)
    else:
        index = szukac_czasu(time_gps, int(i.czas) + 1)
        if index == 'brak danych':
            index = szukac_czasu(time_gps, int(i.czas))
    return  index

"""Obliczanie długości ze współrzędnych"""
def dlugosc(X1, Y1, X2, Y2):
    dl = np.sqrt((X2-X1) ** 2 + (Y2 - Y1) ** 2 )
    return dl

"""Interpolacja undulacji"""
def interpoluj(X, Y, model):
    tmp = model[:]
    for i in tmp:
        i[3] = dlugosc(X, Y, i[0], i[1])
    tmp = sorted(tmp, key=lambda x: x[3])
    suma = 0
    waga = 0
    for i in tmp[0:4]:
        suma += i[2] * ( 1 / ( i[3] ** 2))
        waga +=  1 / ( i[3] ** 2)
    return suma/waga

"""Wyświetlanie komunikatu"""
def print_czasy(nazwa,czasy,czas0,m0):
    print('_' * 50)
    print(nazwa)
    print('Czasy pierwszego soundingu:')
    for i in czasy:
        print('\t{}'.format(i))
    print('Czas średni:')
    print('\t{} +- {}'.format(czas0,m0))
    print('*' * 40)

"""Wyznaczenie sciezki plików"""
def sciezki_plikow(katalog):
    sciezki = []
    katalog1 = []
    lista = os.listdir(katalog)
    for i in lista:
        if os.path.isdir(katalog + '/' + i):
            katalog1.append(katalog + '/' + i)
    for i in katalog1:
        lista = os.listdir(i)
        tmp = []
        tmp1 = []
        for j in lista:
            naz = j.split('.')[0].split()[0].lstrip().rstrip()
            if naz == 'Chart':
                tmp.append(i + '/' + j)
            elif naz == 'czasy':
                n_cza = i + '/' + j
            elif naz == 'GPS':
                n_gps = i + '/' + j
            elif naz == 'par':
                n_par = i + '/' + j
        tmp1.append(tmp)
        tmp1.append(n_gps)
        tmp1.append(n_cza)
        tmp1.append(n_par)
        sciezki.append(tmp1)
    return sciezki

"""Wybór punktów z określonym skokiem"""
def selekcja(lista,skok):
    tmp = []
    for  i in range(0,len(lista), skok):
        tmp.append(lista[i])
    tmp.append(lista[-1])
    return tmp

"""Lączenie punktów z sondy z punktami GPS"""
def laczenie_czasow(sciezka_soun, sciezka_GPS, sciezka_czas, sciezka_para, sciezka_modelu, skok, skok_zapisu):
    #Uzyskania nazwy
    nazwa = sciezka_soun.split('/')
    nazwa1 = nazwa[-2]
    nazwa = nazwa[-1].split('.')[0]
    #Wczytane dane
    numer, rozwiazanie, t_gps, X, Y, H = load_excel(sciezka_GPS)
    depth ,t_sonda = load_sonda(sciezka_soun)
    czas = load_czas(sciezka_czas, nazwa)
    roznica, wys_tyczki = load_par(sciezka_para)
    model = load_model(sciezka_modelu)
    for j, i in enumerate(rozwiazanie):
        if i == 'Pomierzony':
            rozwiazanie[j] = 'Fix'
        elif i == 'Nawigacyjny':
            rozwiazanie[j] = 'Auto'
        elif i == 'Measured':
            rozwiazanie[j] = 'Fix'
        elif i == 'Navigated':
            rozwiazanie[j] = 'Auto'
        else:
            rozwiazanie[j] = ''
    #Czas z pomiaru gps
    time_gps = [Time(str(t).split()[-1]) for t in t_gps ]
    #Godziny i indexy wybranych soundingów
    time = []
    for t in czas:
        li = t.split()
        index = int(li[1])-1
        tmp = Time(li[2])
        tmp.czas +=  roznica.czas
        time.append([index, tmp])
    #Czas pierwszego soundingu
    czas_zerowy = [obl_czas_zerowy(t,t_sonda) for t in time]
    czas_zerowy_sredni ,m0 = czas_sredni(czas_zerowy)
    #Wyswietlenie raportu z obliczenia czasu zerowego
    print_czasy(nazwa,czas_zerowy,czas_zerowy_sredni,m0)
    #Czasy soundingów
    time_sonda = []
    for t in t_sonda:
        tmp = Time()
        tmp.czas = czas_zerowy_sredni.czas + t/1000
        time_sonda.append(tmp)
    punkty = []
    time_sonda = np.array(time_sonda)

    timee = [x.czas for x in time_gps]

    #Przypisane współrzędneych soundingom
    for ind, i in enumerate(time_sonda):
        index = szukac_index(i,timee)
        if index != 'brak danych':
            tmp = Point(Nr=numer[index],X=X[index],Y=Y[index], Hel=(H[index] - wys_tyczki - depth[ind]/3.2808), dok = rozwiazanie[index], depth=depth[ind]/3.2808)
            N = interpoluj(tmp.X, tmp.Y, model)
            tmp.H = tmp.Hel - N
            punkty.append(tmp)
    #Wyświetlenie raportu
    print('Liczba punktów z pomiaru: {}'.format(len(punkty)))
    # Zapis punktów do excela
    save_excel('dane_wyjsciowe/' + nazwa1 + '_' + nazwa + '.xlsx', selekcja(punkty,skok_zapisu))
    print('_' * 50)
    return  selekcja(punkty,skok)