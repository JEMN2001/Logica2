#-*-coding: utf-8-*-

def dibujar_tablero(f, w):
    fig, axes = plt.subplots()
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)

    axesL = []

    fig.subplots_adjust(bottom=0.02, left=0.03, top = 0.6, right=0.97)

    n = 4
    k = 10

    axes1 = plt.subplot(n, k, 1)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes1)

    axes2 = plt.subplot(n, k, 2)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes2)

    axes3 = plt.subplot(n, k, 3)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes3)

    axes4 = plt.subplot(n, k, 4)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes4)

    axes5 = plt.subplot(n, k, 5)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes5)

    axes6 = plt.subplot(n, k, 6)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes6)

    axes7 = plt.subplot(n, k, 7)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes7)

    axes8 = plt.subplot(n, k, 8)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes8)

    axes9 = plt.subplot(n, k, 9)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes9)

    axes10 = plt.subplot(n, k, 10)
    plt.xticks(())
    plt.yticks(())
    axesL.append(axes10)

    arr_img_bomb = plt.imread("bomba.png", format='png')
    imagebox_bomb = OffsetImage(arr_img_bomb, zoom=0.13)
    arr_img_one = plt.imread("uno.jpg", 0)
    imagebox_one = OffsetImage(arr_img_one, zoom=0.13)
    arr_img_two = plt.imread("dos.jpg", 0)
    imagebox_two = OffsetImage(arr_img_two, zoom=0.03)

    contador_m = 1
    for l in f:
    	if contador_m in range(1, 11):
	        if '~' not in l:
	            ab = AnnotationBbox(imagebox_bomb, [0.5, 0.5], frameon=False)
	            axesL[(int(l)%10)-1].add_artist(ab)
	elif contador_m in range(11, 21):
		if '~' not in l:
	            ab = AnnotationBbox(imagebox_one, [0.5, 0.5], frameon=False)
	            axesL[(int(l)%10)-1].add_artist(ab)
	elif contador_m in range(21, 31):
		if '~' not in l:
	            ab = AnnotationBbox(imagebox_two, [0.5, 0.5], frameon=False)
	            axesL[(int(l)%10)-1].add_artist(ab)
	contador_m += 1

    #plt.show()
    fig.savefig("tablero_" + str(w) + ".png")


#################
# importando paquetes para dibujar
print "Importando paquetes..."
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import csv
from sys import argv
print "Listo!"

data_archivo = "tableros.csv"
with open(data_archivo) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    contador = 1
    for l in data:
        print "Dibujando tablero:", l
        dibujar_tablero(l, contador)
        contador += 1
        
        

csv_file.close()
