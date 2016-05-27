import sys
import scipy as sp
import scipy.fftpack as spf
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Function takes in a comma-delimited data file parses it for it's values, and returns an array for each column of data.  Currently only takes in two data points per line

def getarrays(fdest):
	timedata = []
	potatodata = []
	f = open(fdest, 'r') #Opening our data file, 
	for line in f:
		if "time" in line:
			continue
		else:
			ngone = line.rstrip("\n")
			linedata = ngone.split(",") #returns a list with the line's data points as strings
			timedata.append(float(linedata[0]))
			potatodata.append(float(linedata[1])) #want to work with numbers (so change to float, a numb
			#er type
	f.close()
	return timedata, potatodata

#Function makes a sine function, then plots the sine wave and it's FFT.  NOT TESTED
def plot_sinefunc():
	x = np.arange(0,5,0.1)
	y = np.sin(x)
	z = spf.fft(y)
	sine, = plt.plot(x,y, color='red', label='sinefunc')
	thefft, = plt.plot(x,z, color='green', label='SinesFFT')
	plt.show()

#Function takes in two arrays and produces a plot from the inputs.
def plot_data(X,Y):
	fig=plt.figure()
	fig.suptitle('Figure 1')
	dataline, =plt.plot(X,Y, color='green', linestyle='none', marker="v", label="No. potatoes")
	plt.legend()
	plt.xlabel('Time (sec)')
	plt.ylabel('Number of potatoes eaten')
	plt.show()
	fig.savefig('datfig.jpg')

#Exponential function used in the curve_fit call in plot_wdatafit
def arbexpfunc(x, a, b, c):
	answer = a * np.exp(b * x) + c
	return answer

#Function takes in two arrays, does an exponential fit to the data, plots the result, and then prints the resulting fit's parameters
def plot_datawfit(X,Y):
	x=np.array(X)
	y=np.array(Y) #curve_fit needs explicit np.array objects
	popt, pcov = curve_fit(arbexpfunc, x, y, p0=(1, 0.1,1))

	#Make nparrays that have the best fit's data points
	expfunc = lambda p, z: p[0]*np.exp(z*p[1]) + p[2] #Make a function item we can put our optimal values into
	xfit=np.arange(0,60, 1)
	yfit=[]
	for point in xfit:
		val = expfunc(popt, point)
		yfit.append(val) #Append value val to nparray y
	yfit=np.array(yfit)
		
	#Now we make the figure
	fig=plt.figure()
	fig.suptitle('Figure 2')
	dataline, =plt.plot(x,y, color='blue', linestyle='none', marker="v", label="No. potatoes")
	expfit, = plt.plot(xfit, yfit, color='black', label="Best Least Squares Fit")
	plt.legend()
	plt.xlabel('Time (sec)')
	plt.ylabel('Number of potatoes eaten')
	plt.show()
	fig.savefig('datfig_wfit.jpg')

if __name__ == "__main__":
	location = str(sys.argv[1])
	time, pots = getarrays(location)
	plot_data(time,pots)
	plot_datawfit(time,pots)	
