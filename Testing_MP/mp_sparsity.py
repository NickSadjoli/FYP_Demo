'''
Author: Nicholas Sadjoli
Description: Test script for checking performance of chosen MP based on varying sparsity of input signal

Main difference with current mp_sparsity_test.py: Errors are measured between recovered sparse signal compared 
to original sparse signal. Not comparison between original random signal vs recovered signal
'''

from __future__ import division
import sys 
import matplotlib.pyplot as plt
import scipy as sp
from scipy.stats import signaltonoise
from scipy.signal import argrelextrema
from pylab import * 

from sklearn.preprocessing import normalize
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.linear_model import OrthogonalMatchingPursuitCV
from sklearn.datasets import make_sparse_coded_signal
import numpy as np


from mp_functions import * #mp_functions contains all the MP algorithms to be tested.
from utils import *
from Phi import Phi
import matplotlib.pyplot as plt
import unittest

import operator


def SNR_Custom(signal, noise): # definition of SNR = 10 * log10(Psignal/Pnoise), where Psignal = (1/len(signal)) * sum(signal[i]^2)
    #Asignal = (1/signal.shape[0]) * np.sum(np.power(np.abs(signal),2))
    Anoise = (1/noise.shape[0]) * np.sum(np.power(np.abs(noise),2))
    signal_noise = signal+noise
    Atotal = (1/signal_noise.shape[0]) * np.sum(np.power(np.abs(signal_noise),2))
    return 10 * np.log10((Atotal+Anoise)/Anoise)

n_components = 128

x = [ 7.14872976, 7.99683485, 6.77462035, 7.35682238, 3.46190329, 8.55134831, 1.23216904, 8.02565473, \
      2.48947843, 0.4399024, 3.55781487, 2.50578499, 1.03091104, 7.78104952, 9.40652756, 3.77218784, \
      8.71719537, 2.04096106, 3.91879149, 1.12852764, 4.11943121, 0.8026437, 4.27436005, 2.22510807, \
      4.24192647, 5.13894762, 7.97346514, 4.25494931,0.18219066,1.03641905, 4.92143153, 6.45918122, \
      4.45901416, 4.88407393, 2.09664697, 9.26577278, 3.23315769, 5.10595863, 0.39743349, 6.85745321, \
      5.80064463, 4.08567124, 8.73795576, 1.6692493, 4.15961993, 8.07245449, 0.7881806, 0.49578293, \
      1.67697071, 0.35945209, 4.66053785, 3.60989746, 7.54721211, 0.43692716, 8.04713456, 4.32884169, \
      9.95651014, 0.40068128, 4.97639291, 2.48643936, 5.73888652, 8.22627389, 9.95704624, 0.67972128, \
      5.80171823, 8.4017826 , 8.39536605, 5.58673626, 7.46459042, 8.66673671, 0.38849337, 8.84118978, \
      7.12208901, 7.28906882, 7.0982191 , 7.45902509, 2.12682096, 1.72751311, 5.48903346, 2.61131723, \
      3.02831813, 3.32375689, 4.18218502, 4.86000617, 9.72692941, 3.16326772, 0.75072162, 2.27796348, \
      2.71191956, 7.72377838, 2.77066899, 1.76803678, 2.80066975, 6.1347283 , 8.64868878, 5.53528607, \
      0.5610447 , 2.65741932, 4.14732198, 4.53096657, 5.60758129, 2.58230706, 2.56200613, 5.76862782, \
      1.86675798, 4.40260582, 0.45601149, 0.94533482, 1.76847433, 1.50444219, 7.52284895, 4.43420321, \
      2.02678887, 5.48042672, 8.10572836, 6.7875623 , 4.84552806, 2.76148075, 9.47333587, 4.93576891, \
      1.23842482, 0.8383871 , 1.63126236, 3.65153318, 2.78567095, 9.52601736, 4.68414818,5.85502263]

x_actual = np.array(x)
#print Phi
Phi = np.array(Phi)


'''
y, Phi, x = make_sparse_coded_signal(n_samples=1,
                                   n_components=n_components,
                                   n_features=n_features,
                                   n_nonzero_coefs=n_nonzero_coefs,
                                   random_state=0)
'''


chosen_mp = None
max_iter = None

if len(sys.argv) > 1:
  if len(sys.argv) == 2:
    chosen_mp = sys.argv[1]
  elif len(sys.argv) == 3:
    chosen_mp = sys.argv[1]
    max_iter = sys.argv[2]
else:
	print "Please choose an MP to use"
	sys.exit(0)

rms = [0]
R_error = [0]
rms_w_noise = [0]
R_error_w_noise = [0]
runtime = [0]
runtime_w_noise = [0]
snr_values = [0]
sparsity_values = range(0, 81)
'''
if verbose == None:
  verbose = False
else:
  verbose = verbose
'''

vbose = input("Verbose? ==> ")
'''
if vbose == "yes" or vbose == "Y" or vbose == "YES" or vbose == "y":
  vbose = True
elif vbose == "no" or vbose == "N" or vbose == "NO" or vbose == "n":
  vbose = False
else:
  vbose = False
'''

for s in sparsity_values[1:]: #cannot start with sparsity 0, since that means there is no non-zero components anyways
  '''
  # generate the data
  ###################
  # y = Phi * x
  # |Phi|_0 = n_nonzero_coefs
  #generate sparse signal for later processing using MP or other versions of MP.
  '''
  #x_test = x_actual
  
  x_test = np.zeros(x_actual.shape[0])
  x_test[0:s] = x_actual[0:s]
  
  n = len(x_test)
  m = 105 #int(2.5*s*math.log10(n))

  #Phi = np.random.normal(0, 0.5, [m,n])

  y_test = np.dot(Phi, x_test)
  #print y_test

  #y, Phi, x = make_sparse_coded_signal(n_samples=1, n_components=n_components, n_features=n_features, n_nonzero_coefs=s, random_state=0)
  noise = np.random.normal(0, 10 * 1/25, y_test.shape[0])

  if chosen_mp == "omp-scikit":
    omp_process = OrthogonalMatchingPursuit(n_nonzero_coefs=s)
    omp_process.fit(Phi, y_test)
    x_mp = omp_process.coef_
    omp_process_noise = OrthogonalMatchingPursuit(n_nonzero_coefs=s)
    omp_process_noise.fit(Phi, y_test+noise)
    x_mp_noise = omp_process_noise.coef_
  
  #print verbose
  else:
    
    if max_iter is None:
      x_mp, numit, time = mp_process(Phi, y_test, chosen_mp, ncoef=s, verbose=vbose)
      x_mp_noise,numit,time_noise = mp_process(Phi, y_test + noise, chosen_mp, ncoef=s, verbose=vbose)
    else:
      x_mp, numit, time = mp_process(Phi, y_test, chosen_mp, ncoef=s, maxit=max_iter, verbose=vbose)
      x_mp_noise,numit,time_noise = mp_process(Phi, y_test + noise, chosen_mp, ncoef=s, maxit=max_iter, verbose=vbose)
  

  #noise = np.random.normal(0, 1/25, y.shape[0])
  rms_cur = np.sqrt(np.mean(abs(x_test - x_mp)**2, axis=None))
  R_error_cur = Recovery_Error(x_test, x_mp)
  rms_noise_cur = np.sqrt(np.mean(abs(x_test - x_mp_noise)**2, axis=None))
  R_error_noise_cur = Recovery_Error(x_test, x_mp_noise)
  
  if chosen_mp == 'bomp':
    if rms_cur < 20:
      rms.append(rms_cur)
    else:
      test, _, _ = mp_process(Phi, y_test, chosen_mp, ncoef=s, verbose=True)
      rms.append(0.5)
    #runtime.append(time)
  
    if rms_noise_cur < 20:
      rms_w_noise.append(rms_noise_cur)
    else:
      rms_w_noise.append(0.5)
    if R_error_cur < 20:
      R_error.append(R_error_cur)
    else:
      R_error.append(0.5)
    if R_error_noise_cur < 20:
      R_error_w_noise.append(R_error_noise_cur)
    else:
      R_error_w_noise.append(0.5)
  
  else:
    rms.append(rms_cur)
    rms_w_noise.append(rms_noise_cur)
    R_error.append(R_error_cur)
    R_error_w_noise.append(R_error_noise_cur)
  
  if chosen_mp != "omp-scikit":
    runtime.append(time)
    runtime_w_noise.append(time_noise)
  snr_values.append(SNR_Custom(y_test, noise)) 
  print 'done for s = ' + str(s) + ": " + str(rms_cur)


def plot_to_axis(ax, X, Y, color, x_label, y_label, fontsize=10):
  ax.plot(X, Y, color+'o')
  trend = trendline_fit(X,Y)
  ax.plot(X, trend(X), color+'--')
  ax.set_ylabel(y_label, fontsize=fontsize)
  ax.set_xlabel(x_label, fontsize=fontsize)


#print snr_values
#plt.figure(1)
fig, ((ax1,ax2,ax3)) = plt.subplots(nrows=3, ncols=1)
plot_to_axis(ax1, sparsity_values, rms, 'g', 'Sparsity', 'RMS of {}'.format(chosen_mp))
plot_to_axis(ax2, sparsity_values, R_error, 'y', 'Sparsity', 'RE of {}'.format(chosen_mp))
plot_to_axis(ax3, sparsity_values, runtime, 'k', 'Sparsity', 'Runtime of {}'.format(chosen_mp))
#plot_to_axis(ax7, sparsity_values, R_error_w_noise, 'b', 'RMS of {}'.format(chosen_mp), 'Sparsity')
plt.tight_layout()
plt.show()

'''
plt.subplot2grid((4,2), (0,0), colspan=1)
plt.plot(sparsity_values, rms, 'go')
rms_trend = trendline_fit(sparsity_values, rms)
plt.plot(sparsity_values, rms_trend(sparsity_values), 'g--')
plt.ylabel('RMS of {}'.format(chosen_mp))
plt.xlabel('Sparsity')
#plt.tight_layout()

plt.subplot2grid((4,2), (1,0), colspan=1)
plt.plot(sparsity_values, rms_w_noise, 'ro')
rms_noise_trend = trendline_fit(sparsity_values, rms_w_noise)
plt.plot(sparsity_values, rms_noise_trend(sparsity_values), 'r--')
plt.ylabel('RMS w/ stable noise for {} '.format(chosen_mp))
plt.xlabel('Sparsity')
#plt.tight_layout()

plt.subplot2grid((4,2), (2,0), colspan=1)
plt.plot(sparsity_values, R_error, 'yo')
R_error_trend = trendline_fit(sparsity_values, R_error)
plt.plot(sparsity_values, R_error_trend(sparsity_values), 'y--')
plt.ylabel('RE for {} '.format(chosen_mp))
plt.xlabel('Sparsity')

plt.subplot2grid((4,2), (3,0), colspan=1)
plt.plot(sparsity_values, R_error_w_noise, 'bo')
R_error_noise_trend = trendline_fit(sparsity_values, R_error_w_noise)
plt.plot(sparsity_values, R_error_noise_trend(sparsity_values), 'b--')
plt.ylabel('RE w/ stable noise for {} '.format(chosen_mp))
plt.xlabel('Sparsity')


plt.subplot2grid((4,2), (0,1), colspan=1)
plt.plot(sparsity_values, snr_values, 'b-')
plt.ylabel('SNR(in dB)')
plt.xlabel('Sparsity')



if chosen_mp != "omp-scikit":

  plt.subplot2grid((4,2), (1,1), colspan=1)
  plt.plot(sparsity_values, runtime, 'ko')
  runtime_trend = trendline_fit(sparsity_values, runtime)
  plt.plot(sparsity_values, runtime_trend(sparsity_values), 'k--')
  plt.ylabel('Runtime of {}'.format(chosen_mp))
  plt.xlabel('Sparsity')
  
  plt.subplot2grid((4,2), (2,1), colspan=1)
  plt.plot(sparsity_values, runtime_w_noise, 'ro')
  runtime_noise_trend = trendline_fit(sparsity_values, runtime_w_noise)
  plt.plot(sparsity_values, runtime_noise_trend(sparsity_values), 'r--')
  plt.ylabel('Runtime w/stable noise of {}'.format(chosen_mp))
  plt.xlabel('Sparsity')
'''


plt.show()

sys.exit(0)