#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#title           :test_pid.py
#description     :python pid controller test
#author          :Caner Durmusoglu
#date            :20151218
#version         :0.1
#notes           :
#python_version  :2.7
#dependencies    : matplotlib, numpy, scipy
#==============================================================================

import PID
import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID.PID(P, I, D)

    pid.SetPoint=0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.SetPoint > 0:
            feedback += (output - (1/i))
        """" Env 0: some steps are full of noise, each step = 100
        if i>9:
            pid.SetPoint = 1
        if i>100:
            pid.SetPoint = 2
        if i>200:
            #pid.SetPoint = 2 + np.random.normal(mu_0,sigma_0,1)
            pid.SetPoint = 4 + np.random.normal(mu_0,sigma_0,1)
        if i>300:
            pid.SetPoint = 7
        if i>400:
            pid.SetPoint = 11
        if i>500:
            pid.SetPoint = 16 + np.random.normal(mu_1,sigma_1,1)
        if i>600:
            pid.SetPoint = 15
            #pid.SetPoint = 8 + abs(np.random.normal(mu_1,sigma_1,1))
        if i>700:
            pid.SetPoint = 13
        if i>800:
            #pid.SetPoint = 7 + (-1)*abs(np.random.normal(mu_2,sigma_2,1))
            pid.SetPoint = 10 + np.random.normal(mu_2,sigma_2,1)
        if i>900:
            pid.SetPoint = 6
        if i>1000:
            #pid.SetPoint = 4 + np.random.normal(mu_3,sigma_3,1)
            pid.SetPoint = 1 + np.random.normal(mu_3,sigma_3,1)
        if i>1100:
            pid.SetPoint = 6
        if i>1200:
            pid.SetPoint = 10
        if i>1300:
            pid.SetPoint = 13 + np.random.normal(mu_4,sigma_4,1)
        if i>1400:
            #pid.SetPoint = 2 + np.random.normal(mu_0,sigma_0,1)
            pid.SetPoint = 15
        if i>1500:
            pid.SetPoint = 16
        if i>1600:
            pid.SetPoint = 11
        if i>1700:
            pid.SetPoint = 7 + np.random.normal(mu_5,sigma_5,1)
        if i>1800:
            pid.SetPoint = 3
            #pid.SetPoint = 8 + abs(np.random.normal(mu_1,sigma_1,1))
        if i>1900:
            pid.SetPoint = 2
        """

        """Env 1: some steps contain noise ( 100, 100(noise), 100), each step = 100
        if i > 9:
            pid.SetPoint = 1
        if i > 100:
            pid.SetPoint = 2
        if i > 200:
            pid.SetPoint = 2 + np.random.normal(mu_0,sigma_0,1)
            #pid.SetPoint = 2
        if i > 300:
            pid.SetPoint = 2
        if i > 400:
            pid.SetPoint = 4
        if i > 500:
            pid.SetPoint = 7
        if i > 600:
            pid.SetPoint = 11
        if i > 700:
            pid.SetPoint = 16
        if i > 800:
            pid.SetPoint = 16 + np.random.normal(mu_2, sigma_2, 1)
            #pid.SetPoint = 16
        if i > 900:
            pid.SetPoint = 16
        if i > 1000:
            pid.SetPoint = 15
        if i > 1100:
            pid.SetPoint = 13
        if i > 1200:
            pid.SetPoint = 10
        if i > 1300:
            pid.SetPoint = 10 + np.random.normal(mu_4, sigma_4, 1)
            #pid.SetPoint = 10
        if i > 1400:
            pid.SetPoint = 10
        if i > 1500:
            pid.SetPoint = 6
        if i > 1600:
            pid.SetPoint = 1
        if i > 1700:
            pid.SetPoint = 1 + np.random.normal(mu_5, sigma_5, 1)
            #pid.SetPoint = 1
        if i > 1800:
            pid.SetPoint = 1
        if i > 1900:
            pid.SetPoint = 2
        """
        """Env 2: some steps contain noise ( 50, 50(noise),50), each step = 50
        if i > 9:
            pid.SetPoint = 1
        if i > 100:
            pid.SetPoint = 2
        if i > 150:
            pid.SetPoint = 2 + np.random.normal(mu_0, sigma_0, 1)
           # pid.SetPoint = 2
        if i > 200:
            pid.SetPoint = 2
        if i > 250:
            pid.SetPoint = 4
        if i > 300:
            pid.SetPoint = 7
        if i > 350:
            pid.SetPoint = 11
        if i > 400:
            pid.SetPoint = 16
        if i > 450:
            pid.SetPoint = 16 + np.random.normal(mu_2, sigma_2, 1)
            # pid.SetPoint = 16
        if i > 500:
            pid.SetPoint = 16
        if i > 550:
            pid.SetPoint = 15
        if i > 600:
            pid.SetPoint = 13
        if i > 650:
            pid.SetPoint = 10
        if i > 700:
            pid.SetPoint = 10 + np.random.normal(mu_4, sigma_4, 1)
            # pid.SetPoint = 10
        if i > 750:
            pid.SetPoint = 10
        if i > 800:
            pid.SetPoint = 6
        if i > 850:
            pid.SetPoint = 1
        if i > 900:
            pid.SetPoint = 1 + np.random.normal(mu_5, sigma_5, 1)
            # pid.SetPoint = 1
        if i > 950:
            pid.SetPoint = 1
        if i > 1000:
            pid.SetPoint = 2
        """
        #Env 3: some steps contain noise ( 50, 50(noise),50), each step = 50， each step only up/down up to 1
        if i > 9:
            pid.SetPoint = 1
        if i > 100:
            pid.SetPoint = 2
        if i > 150:
            #pid.SetPoint = 2 + np.random.normal(mu_0, sigma_0, 1)
            pid.SetPoint = 2
        if i > 200:
            pid.SetPoint = 2
        if i > 250:
            pid.SetPoint = 3
        if i > 300:
            pid.SetPoint = 4
        if i > 350:
            pid.SetPoint = 5
        if i > 400:
            pid.SetPoint = 6
        if i > 450:
            #pid.SetPoint = 6 + np.random.normal(mu_2, sigma_2, 1)
            pid.SetPoint = 6
        if i > 500:
            pid.SetPoint = 6
        if i > 550:
            pid.SetPoint = 5
        if i > 600:
            pid.SetPoint = 4
        if i > 650:
            pid.SetPoint = 3
        if i > 700:
            #pid.SetPoint = 3 + np.random.normal(mu_4, sigma_4, 1)
            pid.SetPoint = 3
        if i > 750:
            pid.SetPoint = 3
        if i > 800:
            pid.SetPoint = 2
        if i > 850:
            pid.SetPoint = 1
        if i > 900:
            pid.SetPoint = 1 + np.random.normal(mu_5, sigma_5, 1)
            # pid.SetPoint = 1
        if i > 950:
            pid.SetPoint = 1
        if i > 1000:
            pid.SetPoint = 2
            
        time.sleep(0.02)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    # Using make_interp_spline to create BSpline
    helper_x3 = make_interp_spline(time_list, feedback_list)
    feedback_smooth = helper_x3(time_smooth)

    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)
    plt.xlim((0, L))
    plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')

    plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_pid(1.2, 1, 0.001, L=50)
#    test_pid(0.8, L=50)
