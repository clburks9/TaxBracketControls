#Tr: table row
#td: table element

import numpy as np; 
import matplotlib.pyplot as plt
import csv

def readInData():
	
	with open('incomePercentileDataRaw.txt','r') as myFile:
		fileData = myFile.readlines(); 


	data = np.zeros(shape=(99,5)); 

	#rows: percentiles
	#cols: percentile, 2017 income floor, 2016 income floor, percent increase, absolute increase

	fileData = np.array(fileData[0].split('<tr>')); 
	#print(fileData[2])

	fileData = fileData[2:]
	for i in range(0,len(fileData)):
		tmp = fileData[i].split('<td>'); 
		tmp = tmp[1:]
		#print(tmp);

		#first one, remove first 4, and last 10
		data[i][0] = float(tmp[0][4:-11])/100; 
		
		#second one, remove last 5, first 1
		data[i][1] = float(tmp[1][1:-5].replace(',','')); 
		
		#third, same
		data[i][2] = float(tmp[2][1:-5].replace(',','')); 

		#forth, last 6
		data[i][3] = float(tmp[3][:-6])/100;

		#fifth, cut by </td>, then take off $
		data[i][4] = float(tmp[4].split('</td>')[0].replace("$","").replace(",","")); 

	np.save('parsedPercentileData.npy',data);


def investigativePlotting():
	data = np.load('parsedPercentileData.npy'); 
	
	fig,axarr = plt.subplots(2,sharex = True);
	axarr[0].plot(np.arange(1,100),data[:,1]); 
	axarr[0].set_ylabel('Income Floor'); 
	axarr[0].axhline(0,linestyle='--',color='k');


	axarr[1].semilogy(np.arange(1,100),data[:,1])
	axarr[1].set_xlabel('Percentile'); 
	axarr[1].set_ylabel('Income Floor'); 

	
	fig.suptitle('Income by Percentile'); 
	
	#plt.show();


	fig,axarr = plt.subplots(2,sharex = True); 

	axarr[0].plot(np.arange(1,100),data[:,4])
	axarr[0].set_ylabel('Absolute Change'); 
	axarr[0].axhline(0,linestyle='--',color='k'); 

	axarr[1].plot(np.arange(1,100),data[:,3])
	axarr[1].set_ylabel('Percent Change'); 
	axarr[1].set_xlabel('Percentile');
	axarr[1].axhline(0,linestyle='--',color='k'); 
	fig.suptitle('Change By Percentile') 

	plt.show();


def readAlternativeData():
	#From the federal Reserve Data
	with open('IncomeSurvey.txt','r') as myFile:
		fileData = myFile.readlines(); 

	data = []; 
	for i in range(0,len(fileData)):
		data.append(float(fileData[i]));
	data = np.array(data); 
	data = np.sort(data); 

	
	cutoffs = []; 
	for i in range(1,100):
		cutoffs.append(data[int(i*len(data)/100)]); 

	dataUni = np.zeros(shape=(99,2)); 
	for i in range(0,len(cutoffs)):
		dataUni[i] = [i+1,cutoffs[i]]; 

	plt.semilogy(dataUni[:,0],dataUni[:,1])
	plt.show(); 


def readHistoricalData():

	yearly = {}; 
	for i in range(1962,2020):
		yearly[str(i)] = []; 

	with open('cps_00003.csv') as csv_file:
		csv_reader = csv.reader(csv_file,delimiter=',');
		for row in csv_reader:
			if(row[2] == '99999999' or row[2] == ''):
				continue; 
			if(row[0] == 'YEAR'):
				continue; 

			yearly[row[0]].append(int(row[2])); 
	
	data = {};

	for key in yearly.keys():
		if(len(yearly[key]) > 0):
			data[key] = np.zeros(shape=(99,2)); 
		else:
			continue; 

		tmp = yearly[key]; 
		tmp = np.array(tmp); 
		tmp = np.sort(tmp); 
		cutoffs = []; 
		for i in range(1,100):
			cutoffs.append(tmp[int(i*len(tmp)/100)]); 
		for i in range(0,len(cutoffs)):
			data[key][i] = [i+1,cutoffs[i]]; 

	np.save('historicalData.npy',data); 



def investigativeHistorical():

	data = np.load('historicalData.npy').item(); 

	# plt.plot(data['2018'][:,0],data['2018'][:,1]); 
	# plt.show(); 


	fig,axarr = plt.subplots(2,sharex=True); 
	for key in data.keys():
		axarr[0].plot(data[key][:,0],data[key][:,1],color=[(2018-int(key))/(2018-1960),1-(2018-int(key))/(2018-1960),0.0]);
		axarr[1].semilogy(data[key][:,0],data[key][:,1],color=[(2018-int(key))/(2018-1960),1-(2018-int(key))/(2018-1960),0.0]);
	
	axarr[1].set_xlabel('Percentile')
	axarr[0].set_ylabel('Income Floor'); 
	axarr[1].set_ylabel("Log-Scale Income")
	axarr[1].set_xlim([0,100])
	axarr[1].set_ylim([10e1,10e5])
	fig.suptitle('Income Over the Years 1960-2018, Red to Green')
	plt.show()
	
	fig,ax = plt.subplots(); 

	perchange = np.zeros(shape=(2019-1965,99)); 
	for y in range(1965,2019):
		a = (data[str(y)][:,1]-data[str(y-1)][:,1])/data[str(y-1)][:,1];
		perchange[y-1965] = a
	for i in range(0,len(perchange)):
		for j in range(0,len(perchange[i])):
			if(perchange[i,j] > 2):
				perchange[i,j] = 0;
			elif(perchange[i,j] < -2):
				perchange[i,j] = 0;  

	plt.imshow(perchange,origin='lower left'); 
	plt.yticks([i*2 for i in range(0,(2019-1965)//2)],[i*2 +1965 for i in range(0,(2019-1965)//2)])
	plt.colorbar()
	plt.show();

	fig,ax = plt.subplots(); 

	for i in range(1966,2019):
		ax.plot(data[str(i)][:,0],(data[str(i)][:,1]-data[str(i-1)][:,1])/data[str(i-1)][:,1],color=[(2018-i)/(2018-1960),1-(2018-i)/(2018-1960),0.0])
	ax.set_ylim([-1,1])
	ax.axhline(0,linestyle='--',color='k'); 
	ax.set_title("Percentage Change in Income"); 
	ax.set_xlabel("Percentile"); 
	#plt.show();


	fig,ax = plt.subplots(); 

	for i in range(1966,2019):
		ax.plot(data[str(i)][:,0],(data[str(i)][:,1]-data[str(i-1)][:,1]),color=[(2018-i)/(2018-1960),1-(2018-i)/(2018-1960),0.0])
	#ax.set_ylim([-1,1])
	ax.axhline(0,linestyle='--',color='k'); 
	ax.set_title("Absolute Change in Income"); 
	ax.set_xlabel("Percentile"); 
	plt.show();


if __name__ == '__main__':
	#readInData(); 
	#investigativePlotting();
	#readAlternativeData();

	#readHistoricalData(); 
	investigativeHistorical(); 