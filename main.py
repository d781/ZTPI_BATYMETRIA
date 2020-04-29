from funkcje import *
import datetime
import komunikaty as kt
import os
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    #Dane wejsciowe
    par_scie = ['dane', 'dane_wyjsciowe', 'dane/model.xlsx', 'dane/przek.txt', 'PKT', 'SUMA', 'profil']
    par_tech = [50, 10, 3, 2, 5, 2]
    par_wyni = ['t', 't', 't', 't', 't', 't']

    par_scie, par_tech, par_wyni = kt.okno_glowne(par_scie,par_tech,par_wyni)

    katalog = par_scie[0]
    katalog_wyjsciowy = par_scie[1]
    sciezka_modelu = par_scie[2]
    sciezka_przek = par_scie[3]
    przed_poj = par_scie[4]
    nazwa_all = par_scie[5]
    przed_profil = par_scie[6]
    skok_zapisu = par_tech[0]
    skok_przetwarzanie = par_tech[1]
    ilosc_pkt_inte = par_tech[2]
    stopien_wagi = par_tech[3]
    skok_wars = par_tech[4]
    odleglosc_na_profilu = par_tech[5]
    tworzyc_warstwice = par_wyni[0]
    tworzyc_hipso = par_wyni[1]
    tworzyc_akso = par_wyni[2]
    tworzyc_dane_pofil = par_wyni[3]
    zapis_wszyst_pkt = par_wyni[4]
    zapis_poszczegolny_plik = par_wyni[5]

    os.system("cls")

    #Wyznaczenie sciezek plikow
    sciezka = sciezki_plikow(katalog)

    #Integracja danych GNSS z pomiarem batymetrycznym
    t1 = datetime.datetime.now()
    punkty_all = []
    pkt = []
    for i in sciezka:
        for j in i[0]:
            punkty ,punkty2 = laczenie_czasow(j, i[1] , i[2], i[3], sciezka_modelu,skok_przetwarzanie,
                                              skok_zapisu,przed_poj,katalog_wyjsciowy,zapis_poszczegolny_plik)
            punkty_all += punkty
            pkt += punkty2
    print('Liczba punktów: ',len(punkty))

    if zapis_wszyst_pkt == 't':
        save_excel(katalog_wyjsciowy + '/' +  nazwa_all + '.xlsx', punkty)


   #Parametry map
    pktt = np.array(pkt)
    x = pktt[:, 0]
    y = pktt[:, 1]
    h = pktt[:, 2]
    z = [i[2] - int(min(pktt[:,2])) for i in pkt]


    if tworzyc_warstwice == 't' :
        kt.mapa_warstwicowa(x,y,h,skok_wars)

    if tworzyc_hipso == 't':
        kt.mapa_hipsometryczna(x,y,h,skok_wars)

    if tworzyc_akso == 't':
        kt.rzut_aksonometryczny(x,y,z)

    if tworzyc_dane_pofil == 't':
        przekroj, tytul = interpolacja_profilu(sciezka_przek,pktt,odleglosc_na_profilu, ilosc_pkt_inte,stopien_wagi)
        for i, ind in enumerate(przekroj):
            save_profil( katalog_wyjsciowy + '/' + przed_profil + tytul[i] + '.xlsx' , ind )



    s1 = t1.minute * 60 + t1.second + t1.microsecond / (10 ** 6)
    t2 = datetime.datetime.now()
    s2 = t2.minute * 60 + t2.second + t2.microsecond / (10 ** 6)
    print("Czas pracy programu: {:.1f}\n".format(s2-s1))
    kt.stopka()
    c = input('Aby zakończyć wciśnij dowolny klawisz')

