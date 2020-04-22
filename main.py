from funkcje import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation, TriAnalyzer, UniformTriRefiner
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)
import datetime

# -*- coding: utf-8 -*-

if __name__ == '__main__':
    t1 = datetime.datetime.now()
    sciezka_modelu = 'dane/model.xlsx'
    katalog = 'dane'
    punkty_all = []
    sciezka = sciezki_plikow(katalog)
    for i in sciezka:
        for j in i[0]:
            punkty = laczenie_czasow(j, i[1] , i[2], i[3], sciezka_modelu,10,50)
            punkty_all += punkty
    print('Liczba punktów: ',len(punkty))
    save_excel('dane_wyjsciowe/PKT.xlsx', punkty)

    s1 = t1.minute * 60 + t1.second + t1.microsecond / (10 ** 6)
    t2 = datetime.datetime.now()
    s2 = t2.minute * 60 + t2.second + t2.microsecond / (10 ** 6)
    print("Czas petli: {:.6f}".format(s2-s1))

    # Tworzenie mapy warstwicowej
    x=[]
    y=[]
    z=[]
    for i in punkty_all:
        x.append( i.X )
        y.append( i.Y )
        z.append( i.H )
    minH = int(min(z)+1)
    maxH = int(max(z))+1
    skok = 5
    breaks = []
    breaks.append(minH)
    i = 0
    while breaks[i]<maxH:
        breaks.append(breaks[i]+skok)
        i +=1
    init_mask_frac = 20
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 20
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    tri = Triangulation(y, x)
    fig, ax = plt.subplots()
    fig.set_size_inches(10,15)
    ax.tick_params(labelsize=15)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_aspect('equal')
    ax.set_title("Mapa warstwicowa")
    CS = ax.tricontour(tri, z,breaks, linewidths=[0.5, 0.25], colors = 'saddlebrown')
    plt.clabel(CS, inline=5, fontsize=8)
    ax.set_ylabel('X[m]')
    ax.set_xlabel('Y[m]')
    plt.grid()
    plt.savefig('plot.png',dpi=300)
    plt.show()

    # Tworzenie mapy hipsometrycznej
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    tri = Triangulation(y, x)
    mask = TriAnalyzer(tri).get_flat_tri_mask(0.02)
    tri.set_mask(mask)
    fig, ax = plt.subplots()
    fig.set_size_inches(10,15)
    ax.tick_params(labelsize=15)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_aspect('equal')
    ax.set_title("Mapa warstwicowa")
    CS = ax.tricontourf(tri, z,cmap='RdBu')
    ax.tricontour(tri, z, breaks, linewidths=[0.5, 0.25], colors='saddlebrown')
    plt.clabel(CS, inline=1, fontsize=10)
    ax.set_ylabel('X[m]')
    ax.set_xlabel('Y[m]')
    plt.grid()
    plt.savefig('plotHipso.png',dpi=300)
    plt.show()

    #Tworzenie rzutu aksonometrycznego
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(x, y, z, linewidth=0.2)
    plt.show()






