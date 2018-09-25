import csv
import string
import time

import os
 


#Primeiro, abro cada arquivo contendo os logs

##data_file_oi_2600_4G = open('CELLMEAS_3G_OI2600_ANDAR0.txt', 'r')
#data_file_tim_1800_4G = open('CELLMEAS_4G_Tim1800.txt', 'r')
#data_file_tim_2600_4G = open('CELLMEAS_4G_Tim2600.txt', 'r')
#data_file_vivo_1800_4G = open('CELLMEAS_4G_OI1800_ANDAR0.txt', 'r')
#data_file_vivo_2600_4G = open('CELLMEAS_4G_VIVO2600_ANDAR0.txt', 'r')
data_file_consolidado = open('CONSOLIDADO'+str(time.time())+'.txt', 'w')
data_file_statistics = open('statistics'+str(time.time())+'.txt', 'w')

#Escrevo o cabecalho do CSV consolidado
fieldnames = ['X', 'Y', 'Sinal', 'Range', 'Operadora', 'tipo_teste','tecnologia','frequencia','andar','venue']
writer = csv.DictWriter(data_file_consolidado, fieldnames=fieldnames)
writer.writeheader()

#fieldnames_statistics = ['Tecnologia','Target','andar','venue', 'Range', 'Average', 'Desvio_Padrao', 'limite_inferior','limite_superior', 'Operadora']
#writer_statistics = csv.DictWriter(data_file_statistics, fieldnames=fieldnames_statistics)
#writer_statistics.writeheader()


#coloco o conteudo dos arquivos em listas de linhas para poder iterar no for

#linhas_oi_2100=data_file_oi_2100_3G.readlines()
#linhas_oi_2600=data_file_oi_2600_3G.readlines()
#linhas_tim_1800=data_file_tim_1800_4G.readlines();
#linhas_tim_2600=data_file_tim_2600_4G.readlines();
#linhas_vivo_1800=data_file_vivo_1800_4G.readlines();
#linhas_vivo_2600=data_file_vivo_2600_4G.readlines();


#Funcao para iterar sobre cada linha dos arquivos de log
def ler_arquivo_log(linhas_do_arquivo,operadora,tipo_teste,tecnologia,frequencia,andar,venue):
	i=0
	index_signal=0
	for linha in linhas_do_arquivo:
		if i!=0:
			try:
				aux= linha.split()#faco uma lista das palavras da linha
				signal=float(aux[index_signal])#pego o sinal
				x=float(aux[0])#pego a coordenada y
				y=float(aux[1])#pego a coordenada x
				xint=round(x)#arredondo a coordenada para inteiro
				yint=round(y)#arredondo a coordenada para inteiro
				#Verifico qual range o sinal esta
				
				range=""
				if tipo_teste.upper() == "SINAL":
					if  signal<-100:
						range="<-100"
					elif signal<-95:
						range="<-95 to <-100"
					elif signal<-90:
						range="<-90 to <-95"
					elif signal<-85:
						range="<-85 to <-90";
					elif signal<-80:
						range="<-80 to <-85"
					elif signal<-75:
						range="<-75 to <-80"
					elif signal<-65:
						range="<-65 to <-75"
					else:
						range=">=-65"
				writer.writerow({'X': yint, 'Y': xint, 'Sinal': signal, 'Range': range, 'Operadora': operadora, 'tipo_teste': tipo_teste ,'tecnologia': tecnologia,'frequencia':frequencia, 'andar': andar,'venue': venue })	
				
			except Exception as e:
				print(str(e))
		else:
		  i=i+1
		  aux= linha.split()#faco uma lista das palavras da linha
		  t=0
		  for name in aux:
		  	if tipo_teste.upper() == "SINAL" and tecnologia == "3G" and "RSCP" in name.upper() :
		  		index_signal=t
		  		break
		  	elif tipo_teste.upper()== "SINAL" and tecnologia == "4G" and "RSRP" in name.upper() :
		  		index_signal=t
		  		break
		  	elif tipo_teste.upper() == "DL" and "RLC" in name.upper() :
		  		index_signal=t
		  		break
		  	elif tipo_teste.upper() == "UL" and "RLC" in name.upper() :
		  		index_signal=t
		  		break
		  	t+=1


	#writer_statistics.writerow({'Tecnologia': tecnologia,'Target': target,'andar': andar,'venue': venue, 'Range': range, 'Average', 'Desvio_Padrao': ,'Operadora','limite_inferior','limite_superior'

dirpath = os.getcwd() #pega os nomes dos arquivos que estao na pasta
print("current directory is : " + dirpath)
foldername = os.path.basename(dirpath)
lista_arquivos= os.listdir(dirpath)

for path,dirs,files in os.walk(dirpath):
    for filename in files:
        path_file=path.replace(dirpath, "")+filename
        if ".txt" in filename and ("RLCRATE" in filename.upper() or "CELLMEAS_3G" in filename.upper() or "CELLMEAS_4G" in filename.upper()) and "LONG" not in filename.upper() and "SHORT" not in filename.upper():
        	aux= path_file.split("/")
        	venue=aux[1]
        	andar=aux[3]
        	operadora= aux[4]
        	if "DL" in filename:
        		tipo_teste="DL"
        	else if "UL" in filename:
        		tipo_teste="UL"
        	else: 
        		tipo_teste="SINAL"
        		aux2= aux[5].split()
			    tecnologia=aux2[2]
				frequencia=aux2[1]
			
			data_file = open(filename, 'r')
			linhas_do_arquivo=data_file.readlines()
						
			ler_arquivo_log(linhas_do_arquivo, operadora,tipo_teste,tecnologia,frequencia,andar,venue)
        	print(aux)




