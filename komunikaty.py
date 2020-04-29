from funkcje import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter
import matplotlib.tri as tri


def mapa_warstwicowa(x,y,h,skok_wars):
    min_x = int(min(x))
    max_x = int(max(x)) + 1
    min_y = int(min(y))
    max_y = int(max(y)) + 1
    min_h = int(min(h))
    max_h = int(max(h)) + 1
    pas_h = np.arange(min_h, max_h + skok_wars, skok_wars)
    #Tworzenie mapy warstwicowej
    triang = tri.Triangulation(y, x)
    triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1),
                             y[triang.triangles].mean(axis=1))< 0.15)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 0.5+10*(max_x-min_x)/(max_y-min_y))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_title('Mapa warstwicowa')
    ax.set_ylabel('X[m]')
    ax.set_xlabel('Y[m]')
    cs = ax.tricontour(triang, h, levels=pas_h,linewidths=[0.5, 0.25], colors='saddlebrown')
    ax.clabel(cs, pas_h, inline=True, fontsize=10)
    plt.grid()
    plt.show()

def mapa_hipsometryczna(x,y,h,skok_wars):
    min_x = int(min(x))
    max_x = int(max(x)) + 1
    min_y = int(min(y))
    max_y = int(max(y)) + 1
    min_h = int(min(h))
    max_h = int(max(h)) + 1
    pas_h = np.arange(min_h, max_h + skok_wars, skok_wars)
    #Tworzenie mapy hipsometrycznej
    triang = tri.Triangulation(y, x)
    triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1),
                             y[triang.triangles].mean(axis=1)) < 0.15)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 2+10 * (max_x - min_x) / (max_y - min_y))
    cmap = cm.get_cmap(name='terrain')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_title('Mapa hipsometryczna')
    ax.set_ylabel('X[m]')
    ax.set_xlabel('Y[m]')
    cs = ax.tricontourf(triang, h, levels=pas_h)
    cbar = fig.colorbar(cs)
    plt.show()

def rzut_aksonometryczny(x,y,z):
    #Tworzenie rzutu aksonometrycznego
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(y, x, z, linewidth=0.2)
    plt.show()

def naglowek():
    print('----------------------------------------------------------------------------------------------')
    print('Zaawansowane techniki pomiarowe')
    print('Program: BATYMETRIA')
    print('Grupa 1')
    print('AGH 2020')
    print('----------------------------------------------------------------------------------------------\n')

def informacje():
    naglowek()
    print('Program integruje dane uzyskane przy pomocy sądy oraz danych GNSS.')
    print('Dane wejsciowe należy podzielić według poszczególnych dni i zamieścić w\n'
          'osobnych katalogach ktore należy umieścić w katalogu głównym, ktorego nazwę lub\n'
          'ścieżkę podano w ustawieniach. W każdym z odrębnych katalogów należy umieścić\n'
          'pliki csv z pomiaru sondą ( nazwy plików musą się zaczynać od słowa Chart i spacji\n'
          'pomiędzy słowem Chart a dalszą częścią nazwy. Plik z pomiaru GNSS wspólny dla\n'
          'wszystkich plików z sondy. Plik z pomiarów satelitarnych musi się nazywać GPS.xlsx\n'
          'W pliku tym w pierwszej kolumnie powinien znaleźć się numer punktu, w drugiej\n'
          'dokładność pomiaru (Pomierzony/Nawigacyjny), w trzeciej datę i godzinę pomiaru\n'
          'w czwartej współrzędna Y, w piątej współrzędna X w szóstej wysokość elipsoidalna.\n\n'
          'W pliku czasy.txt powinny znajdować się godziny wykonania poszczególnych pomiarów sondy.\n'
          'Odczyty powinny być poprzedzone nazwą pliku z pomiaru sondą (schemat pliku):\n'
          '----------------------------------------------------------------------------------------------\n'
          'Chart 26_5_10 [0]\n'
          'Sounding 371 11:16:08\n'
          '\n'
          'Chart 26_5_10 [1]\n'
          'Sounding 5849 11:54:35\n'
          '----------------------------------------------------------------------------------------------\n\n'
          'Ostatni z plików par.txt zawiera roznice wysokości między sondą a anteną GNSS oraz różnicę\n'
          'czasumiędzy sondą (czas GPS) a pomiarem GNSS (czas lokalny) wg schematu:\n'
          '----------------------------------------------------------------------------------------------\n'
          'Wysokośc tyczki\n'
          '2.000\n'
          'Różnica czasu GPS - sonda\n'
          '02:00:00\n'
          '----------------------------------------------------------------------------------------------\n\n'
          'W ustawieniach należy wskazać plik z modelem geoidy (zawartość wg schematu poniżej):\n'
          'pierwszy wiersz nagłówki kolumn\n'
          'pierwsza kolumna współrzędna X, druga Y, trzecia undulacja\n'
          '----------------------------------------------------------------------------------------------\n'
          'X\tY\tN\n'
          '5544636.0000\t7421704.0000\t39.7707\n'
          '----------------------------------------------------------------------------------------------\n\n'
          'Jeśli chcemy generować dane do profilu powinniśmy wskazać w ustawieniach plik zawierający\n'
          'dnne profilu (zawartość wg schematu poniżej):\n'
          'w pierwszym wierszu nazwa pliku wynikowego,\n'
          'w drugim wierszu współrzędne x i y punktu początkowego profilu,\n'
          'w trzecim wierszu współrzędne x i y punktu koncowego profilu.\n'
          'W poliku można wpisać dane kilku \n')
    C = input('Aby wrócić naciśnij dowolny klawisz: ')

def stopka():
    print('----------------------------------------------------------------------------------------------')
    print('Program opracowali')
    print('inż. Damian Ozga')
    print('inż. Kamil Olko')
    print('inż. Izabela Pawłowska')
    print('inż. Grzegorz Piekarczyk')
    print('----------------------------------------------------------------------------------------------\n')

def ust_sciezek(par_scie):
    while   True:
        os.system('cls')
        naglowek()
        print('1.Katalog z danymi wejsciowymi: {}'.format(par_scie[0]))
        print('2.Katalog z danymi wyjsciowymi: {}'.format(par_scie[1]))
        print('3.Ścieżka modelu geoidy: {}'.format(par_scie[2]))
        print('4.Ścieżka pliku z danymi profili: {}'.format(par_scie[3]))
        print('5.Przedrostek nazwy plików z zapisanymi\n'
              '  punktami dla poszczególnych pomiarów: {}'.format(par_scie[4]))
        print('6.Przedrostek nazwy plików z zapisanymi\n'
              '  wszystkimi punktami przetwarzanymi: {}'.format(par_scie[5]))
        print('7.Przedrostek nazwy plików z zapisanymi\n'
              '  punktami profilu podłużnego: {}'.format(par_scie[6]))
        print('8.Powrót\n')
        tmp = input('Aby wybrać podaj odpowiednią cyfrę: ')
        if tmp == '1':
            os.system('cls')
            naglowek()
            print('Podaj scieżkę katalog z danymi wejsciowymi:')
            par_scie[0] = input()
        elif tmp == '2':
            os.system('cls')
            naglowek()
            print('Podaj scieżkę katalog z danymi wyjsciowymi:')
            par_scie[1] = input()
        elif tmp == '3':
            os.system('cls')
            naglowek()
            print('Podaj scieżkę modelu geoidy:')
            par_scie[2] = input()
        elif tmp == '4':
            os.system('cls')
            naglowek()
            print('Podaj scieżkę pliku z danymi profili:')
            par_scie[3] = input()
        elif tmp == '5':
            os.system('cls')
            naglowek()
            print('Podaj przedrostek nazwy plików z zapisanymi\n'
              '  punktami dla poszczególnych pomiarów:')
            par_scie[4] = input()
        elif tmp == '6':
            os.system('cls')
            naglowek()
            print('Podaj przedrostek nazwy plików z zapisanymi\n'
              '  wszystkimi punktami przetwarzanymi:')
            par_scie[5] = input()
        elif tmp == '7':
            os.system('cls')
            naglowek()
            print('Przedrostek nazwy plików z zapisanymi\n'
              'punktami profilu podłużnego:')
            par_scie[6] = input()
        elif tmp == '8':
            break
    return par_scie

def ust_parametrow(par_tech):
    while   True:
        os.system('cls')
        naglowek()
        print('1.Skok zapisu punktów pla poszczególnych plików: {}'.format(par_tech[0]))
        print('2.Skok między punktami dla przetwarzania: {}'.format(par_tech[1]))
        print('3.Ilośc punktów branych do interpolacji: {}'.format(par_tech[2]))
        print('4.Stopień potęgi odwrotności odległości dla wagi\n'
              '  podczas interpolacji wysokości: {}'.format(par_tech[3]))
        print('5.Skok warstwic {}'.format(par_tech[4]))
        print('6.Odległość między punktami na profilu: {}'.format(par_tech[5]))
        print('7.Powrót\n')
        tmp = input('Aby wybrać podaj odpowiednią cyfrę: ')
        if tmp == '1':
            os.system('cls')
            naglowek()
            print('Podaj skok zapisu punktów pla poszczególnych plików:')
            par_tech[0] = int(input())
        elif tmp == '2':
            os.system('cls')
            naglowek()
            print('Podaj skok między punktami dla przetwarzania:')
            par_tech[1] = int(input())
        elif tmp == '3':
            os.system('cls')
            naglowek()
            print('Podaj ilośc punktów branych do interpolacji:')
            par_tech[2] = int(input())
        elif tmp == '4':
            os.system('cls')
            naglowek()
            print('Stopień potęgi odwrotności odległości dla wagi\n'
                  'podczas interpolacji wysokości:')
            par_tech[3] = int(input())
        elif tmp == '5':
            os.system('cls')
            naglowek()
            print('Podaj skok warstwic:')
            par_tech[4] = int(input())
        elif tmp == '6':
            os.system('cls')
            naglowek()
            print('Podaj odległość między punktami na profilu:')
            par_tech[5] = int(input())
        elif tmp == '7':
            break
    return par_tech

def ust_wynikow(par_wyni):
    while   True:
        os.system('cls')
        naglowek()
        print('1.Tworzyć mapę warstwicową (T/N): {}'.format(par_wyni[0].upper()))
        print('2.Tworzyć mapę hipsometryczną (T/N): {}'.format(par_wyni[1].upper()))
        print('3.Tworzyć rzut aksonometryczny (T/N): {}'.format(par_wyni[2].upper()))
        print('4.Generować dane do profilu podłużnego (T/N): {}'.format(par_wyni[3].upper()))
        print('5.Zapisywać do pliku zbiorczego wszystkie przetwarzane punkty (T/N): {}'.format(par_wyni[4].upper()))
        print('6.Zapisywać do pliku punkty z poszczególnych pomiarów (T/N): {}'.format(par_wyni[5].upper()))
        print('7.Powrót\n')
        tmp = input('Aby wybrać podaj odpowiednią cyfrę: ')
        if tmp == '1':
            os.system('cls')
            naglowek()
            print('Tworzyć mapę warstwicową (T/N)?:')
            par_wyni[0] = input().lower()
        elif tmp == '2':
            os.system('cls')
            naglowek()
            print('Tworzyć mapę hipsometryczną (T/N)?:')
            par_wyni[1] = input().lower()
        elif tmp == '3':
            os.system('cls')
            naglowek()
            print('Tworzyć rzut aksonometryczny (T/N)?:')
            par_wyni[2] = input().lower()
        elif tmp == '4':
            os.system('cls')
            naglowek()
            print('Generować dane do profilu podłużnego (T/N)?:')
            par_wyni[3] = input().lower()
        elif tmp == '5':
            os.system('cls')
            naglowek()
            print('5.Zapisywać do pliku zbiorczego wszystkie przetwarzane punkty (T/N)?:')
            par_wyni[4] = input().lower()
        elif tmp == '6':
            os.system('cls')
            naglowek()
            print('Zapisywać do pliku punkty z poszczególnych pomiarów (T/N)?:')
            par_wyni[5] = input().lower()
        elif tmp == '7':
            break
    return par_wyni

def okno_glowne (par_scie, par_tech, par_wyni):
    while   True:
        os.system('cls')
        naglowek()
        print('1.Ustawienia scieżek plików i katalogów')
        print('2.Wybór plików wyjsciowych')
        print('3.Ustawienia parametrów generowanych danych')
        print('4.Infomacje')
        print('5.START\n')
        tmp = input('Aby wybrać podaj odpowiednią cyfrę: ')
        if tmp == '1':
            os.system('cls')
            par_scie = ust_sciezek(par_scie)
        elif tmp == '2':
            os.system('cls')
            par_tech = ust_parametrow(par_tech)
        elif tmp == '3':
            os.system('cls')
            par_wyni = ust_wynikow(par_wyni)
        elif tmp == '4':
            os.system('cls')
            informacje()
        elif tmp == '5':
            os.system('cls')
            break
    return par_scie, par_tech, par_wyni