#
# Copyright (c) 2011 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# The following is derived from the slides presented by
# Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
# CSLU / OHSU, Spring Term 2011.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import scipy.signal as sig

def filter_graph(b, a, SFnorm, zpln=False):
    '''
    Sketch filter Magnitude. Phase response and z plane
    
    Parameters
    ----------
    Numerator : (ndarray)
        Numerator polynomial.
    Denominator : (ndarray)
        Denominator polynomial.
    SFnorm : (int)
        Normalized  frequencies, Nyquist frequency. Units of half-cycles/sample.
        https://en.wikipedia.org/wiki/Normalized_frequency_(unit)
    zpln : (boolian)
        Sketch z plane and return zeros, poles and system gain. 
        
    Returns if zpln is True
    ----------
    z : (ndarray)
        Zeros of the transfer function.
    p : (ndarray)
        Poles of the transfer function.
    k : (float)
        System gain.
    '''
    wr, Hr = sig.freqz(b, a, 1024)
    
    fig = plt.figure(figsize=(16,14))
    fig.tight_layout()
    ax1 = fig.add_subplot(221)
    ax1.set_title("Magnitude Response")
    ax1.set_xlabel("Hz")
    ax1.set_ylabel("Amp [dB]")
    ax1.plot(wr/np.pi * (SFnorm), 20*np.log10(np.abs(Hr)))

    ax2 = fig.add_subplot(222)
    ax2.set_title("Phase Response")
    ax2.set_xlabel("Hz")
    ax2.set_ylabel("Angle [radian]")
    ax2.plot(wr/np.pi * (SFnorm), np.unwrap(np.angle(Hr)))
    
    if zpln:
        ax3 = fig.add_subplot(212)
        (z, p, k) = zplane(b, a, axes = ax3, axis_lim = 2, circlecolor='white')
        print(f'Zeros: {z} \nPoles: {p}')
        return z, p

    
def zplane(b, a, axis_lim=1, axes= None, circlecolor='black', figsize=(8,8), filename=None):
    """
    Plot the complex z-plane given a transfer function.
        
    Parameters
    ----------
    Numerator : (ndarray)
        Numerator polynomial.
    Denominator : (ndarray)
        Denominator polynomial.
    circlecolor: (string, optional)
        Color of the r circle in z plane. Default to 'black'
    figsize: (tuple, optional)
        Figure size. Default to (8,8)
    filename: (string, optional)
        Name of the png file. Defaults to None
        
    Returns
    ----------
    z : (ndarray)
        Zeros of the transfer function.
    p : (ndarray)
        Poles of the transfer function.
    k : (float)
        System gain.
    """

    # get a figure/plot    
    if axes != None:
        ax = axes
    else:
        ax = plt.subplot(111)
        
    plt.rcParams["figure.figsize"] = figsize
    
    # create the unit circle
    uc = patches.Circle((0,0), radius=1, fill=False,
                        color=circlecolor, ls='dashed')
    ax.add_patch(uc)

    # The coefficients are less than 1, normalize the coeficients
    if np.max(b) > 1:
        kn = np.max(b)
        b = b/float(kn)
    else:
        kn = 1

    if np.max(a) > 1:
        kd = np.max(a)
        a = a/float(kd)
    else:
        kd = 1
        
    # Get the poles and zeros
    p = np.roots(a)
    z = np.roots(b)
    k = kn/float(kd)
    
    # Plot the zeros and set marker properties    
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)
    plt.setp( t1, markersize=10.0, markeredgewidth=1.0,
              markeredgecolor='k', markerfacecolor='g')

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
    plt.setp( t2, markersize=12.0, markeredgewidth=3.0,
              markeredgecolor='r', markerfacecolor='r')

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # set the ticks
    r = axis_lim; r_axis = r + 0.5; plt.axis('scaled'); plt.axis([-r_axis, r_axis, -r_axis, r_axis])
    ticks = np.arange(-r, r + 0.5, 0.5); plt.xticks(ticks); plt.yticks(ticks)
    
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
    

    return z, p, k