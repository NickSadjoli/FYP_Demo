import numpy as np
from pywt import dwt, idwt
import pywt
import pandas as pd
from utils import *
#from scipy.fftpack import dwt, idwt
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from numpy.linalg import norm
import time
from statsmodels.robust import mad 


if len(sys.argv) == 5:
    start_index = int(sys.argv[1])
    y_fl = sys.argv[2]
    repeats = int(sys.argv[3])
    output_folder = sys.argv[4]
else:
    print "Invalid, please try again! \n(Args expected: [start index for checking] [y's file(\w .h5 subfix)] [# repeats/testing to be done] [output_folder])"
    sys.exit(0)

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

	


y_whole, _, _, _ = take_data(y_fl)
step = 25600
runtime_list = []
for i in range(0,repeats):
    y_data = y_whole[i*step: (i+1)*step]
    t0 = time.time()
    '''
    y_init = np.zeros((np.shape(y_data)[0], 1))
    y_init[:] = y_data[:]
    file_create("dwt/initial_y.h5", y_init, np.shape(y_init)[0], np.shape(y_init)[1])
    '''
    y_data = np.reshape(y_data, (len(y_data), ))
    
    x = np.arange(0, len(y_data))
    #print np.shape(y_data), type(y_data), np.count_nonzero(y_data)	
    #transform y using dwt into freq domain, and get dwt representation(approximate and detailed coeff)
    #y_dwtA, y_dwtD = dwt(y_data, 'db4')
    coeff = pywt.wavedec(y_data, "db20", mode="per")

    sigma = mad(coeff[-1])
    threshold = sigma * np.sqrt(2*np.log(len(y_data)))

    #coeff[1:] = (pywt.threshold(i, value=threshold, mode="soft") for i in coeff[1:])
    coeff[1: ] = (pywt.threshold(i, value=threshold, mode="hard") for i in coeff[1:])

    y_cmp = pywt.waverec(coeff, "db20", mode="per")
    y_cmp = np.reshape(y_cmp, (len(y_cmp), 1))
    file_create(output_folder + "/dwt_"+str(i)+".h5", y_cmp, np.shape(y_cmp)[0], np.shape(y_cmp)[1])
    tf = time.time()
    #print "compressed slice number: ", i, "kept_ coefficients: ", needA, needD,  "||compressed nonzero elements:", np.count_nonzero(y_cmp), "detected data type: ", type(y_cmp[0]), tf-t0
    print "compressed slice number: ", i,  "||compressed nonzero elements:", np.count_nonzero(y_cmp), "detected data type: ", type(y_cmp[0]), tf-t0
    runtime_list.append(tf-t0)

runtime_list = np.reshape(runtime_list, (len(runtime_list), 1))
file_create(output_folder + "/dwt_runtime.h5", runtime_list, np.shape(runtime_list)[0], np.shape(runtime_list)[1])
