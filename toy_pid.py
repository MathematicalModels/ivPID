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

# title           :toy_pid.py
# description     :python pid controller test
# author          :Yuqing Hou
# date            :20190318
# version         :0.1
# notes           :
# python_version  :3.6
# dependencies    : matplotlib, numpy, scipy
# ==============================================================================

import PID
import time
import matplotlib.pyplot as plt
import numpy as np
# from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline  # Switched to BSpline


def test_pid(P=0.2, I=0.0, D=0.0, L=100):
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

    pid.SetPoint = 0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_record = [] #record env feedbacks
    time_list = []
    setpoint_record = [] #record setpoints
    output_record = []   #record PI outputs
    abs_ITerm_list = []  #record |ITerm|

    #output_accumulation_record (OAR) records the accumulation of the previous |outputs|,
    # i.e. OAR[i] = \Sum_{0}^{i} |outputs|
    output_accumulation_record = []

    #output_pattern_record (OPR) records the accumulation of the latest #windowsize outputs,
    # i.e. OPR[i] = \Sum_{i - windows + 1}^{i} |outputs|,
    # or equivalently, OPR[i] = ORA[i] - ORA[i - windowsize]
    # OPR[0] = OPR[1] = … = OPR [windowsize - 2] = 0, for accumulation only valid after i > = windowsize -1
    output_pattern_record = []

    windowsize = 6
    partial_sum_of_abs_output = 0.0 # |output_i|
    threshold = 10 # threshold for breaking from the current environment
    break_record = [] #record where breaks happens

    Env4_x = np.linspace(0, 1999, 2000) # only for Env4

    for i in range(0, END):

        print(i)

        if i < windowsize - 1:
            pid.update(feedback, 0)
        else:
            pid.update(feedback, output_pattern_record[i-1])#?

        output = pid.output

        #print("Kp* PTerm = %f   Ki*ITerm= %f" %(P*pid.PTerm, I*pid.ITerm))

        if pid.SetPoint > 0:
            feedback += (output - (1 / i))

        """# Env 1: some steps contain noise ( 50, 50(noise),50), each step = 50， each step only up/down up to 1
        if i > 0:
            pid.SetPoint = 1
        if i > 10:
            pid.SetPoint = 2
        if i > 30:
            pid.SetPoint = 2 + np.random.normal(0, 0.5, 1)[0]
            #pid.SetPoint = 2
        if i > 40:
            pid.SetPoint = 2
        if i > 50:
            pid.SetPoint = 3
        if i > 70:
            pid.SetPoint = 4
        if i > 90:
            pid.SetPoint = 5
        if i > 110:
            pid.SetPoint = 6
        if i > 130:
            pid.SetPoint = 6 + np.random.normal(0, 0.5, 1)[0]
            #pid.SetPoint = 6
        if i > 150:
            pid.SetPoint = 6
        if i > 170:
            pid.SetPoint = 5
        if i > 190:
            pid.SetPoint = 4
        if i > 210:
            pid.SetPoint = 3
        if i > 230:
            pid.SetPoint = 3 + np.random.normal(0, 0.5, 1)[0]
            #pid.SetPoint = 3
        if i > 250:
            pid.SetPoint = 3
        if i > 270:
            pid.SetPoint = 2
        if i > 290:
            pid.SetPoint = 1
        if i > 310:
            pid.SetPoint = 1 + np.random.normal(0, 0.5, 1)[0]
            #pid.SetPoint = 1
        if i > 330:
            pid.SetPoint = 1
        if i > 350:
            pid.SetPoint = 2
        """
        """# Env 3: some steps contain noise ( 100, 100(noise), 100), each step = 100
        if i > 9:
            pid.SetPoint = 1
        if i > 100:
            pid.SetPoint = 2
        if i > 200:
            pid.SetPoint = 2 + np.random.normal(0, 1, 1)[0]
            # pid.SetPoint = 2
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
            pid.SetPoint = 16 + np.random.normal(0, 1, 1)[0]
            # pid.SetPoint = 16
        if i > 900:
            pid.SetPoint = 16
        if i > 1000:
            pid.SetPoint = 15
        if i > 1100:
            pid.SetPoint = 13
        if i > 1200:
            pid.SetPoint = 10
        if i > 1300:
            pid.SetPoint = 10 + np.random.normal(0, 1, 1)[0]
            # pid.SetPoint = 10
        if i > 1400:
            pid.SetPoint = 10
        if i > 1500:
            pid.SetPoint = 6
        if i > 1600:
            pid.SetPoint = 1
        if i > 1700:
            pid.SetPoint = 1 + np.random.normal(0, 1, 1)[0]
            # pid.SetPoint = 1
        if i > 1800:
            pid.SetPoint = 1
        if i > 1900:
            pid.SetPoint = 2

        """
        # Env 4: sine curve (states are changed continuously)
          # split the horizon, then pid.SetPoint = np.

        pid.SetPoint = 3*np.sin(Env4_x[i]/200) + 5 + np.random.normal(0, 0.1, 1)[0]
        if ( i >200 and i < 300 ) or (i > 800 and i <900) or (i > 1300 and i <1400) or (i > 1700 and i <1800):
            pid.SetPoint = pid.SetPoint + np.random.normal(0, 1, 1)[0]

        # Env 5: sine curve with small noise for each state and big noise for noisy-TV


        time.sleep(0.02)

        partial_sum_of_abs_output += abs(output)

        output_accumulation_record.append(partial_sum_of_abs_output)

        feedback_record.append(feedback)
        setpoint_record.append(pid.SetPoint)
        time_list.append(i)
        output_record.append(output)
        abs_ITerm_list.append(pid.abs_ITerm)

        if i < windowsize - 1:
            output_pattern_record.append(0.0)
        else:
            output_pattern_record.append(output_accumulation_record[i] - output_accumulation_record[i - windowsize])

        if output_pattern_record[i] > threshold:
            break_record.append((i, -3)) # save each break points as a tuple


    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 2000)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    # Using make_interp_spline to create BSpline
    helper_x3 = make_interp_spline(time_list, feedback_record)
    feedback_smooth = helper_x3(time_smooth)

    #plt.plot(time_smooth, feedback_smooth)

    plt.plot(time_list, setpoint_record)
    plt.plot(time_list, output_record)
    # plt.plot(time_list, abs_ITerm_list)
    # plt.plot(time_list, current_window_abs_ITerm_list)
    # plt.plot(time_list, current_window_abs_ITerm_list)
    # plt.plot(time_list, PTerm_list)
    # plt.plot(time_list, output_accumulation_list)
    plt.plot(time_list, output_pattern_record)
    # plt.plot(time_list, break_record,'ro') # draw the tuples
    for j in range(0, break_record.__len__()):
        plt.plot( break_record[j][0],break_record[j][1],'ro')
        print("escape at %d" % break_record[j][0])

    plt.xlim((0, L))
    # plt.ylim((min(feedback_list) - 0.5, max(feedback_list) + 0.5))
    plt.ylim(-10, 20)
    plt.xlabel('time (s)')
    plt.ylabel('PI (PV)')
    plt.title('TEST PI')

    plt.grid(True)
    plt.show()

# auto save with specific names
# plot the break action
# change pid.output to reset sth.


if __name__ == "__main__":
    test_pid(1.2, 1, 0, L=2000)
#    test_pid(0.8, L=50)


"""Env 2: some steps contain noise ( 50, 50(noise),50), each step = 50
        if i > 9:
            pid.SetPoint = 1
        if i > 100:
            pid.SetPoint = 2
        if i > 150:
            pid.SetPoint = 2 + np.random.normal(mu_0, sigma_0, 1)[0]
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
            pid.SetPoint = 16 + np.random.normal(mu_2, sigma_2, 1)[0]
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
            pid.SetPoint = 10 + np.random.normal(mu_4, sigma_4, 1)[0]
            # pid.SetPoint = 10
        if i > 750:
            pid.SetPoint = 10
        if i > 800:
            pid.SetPoint = 6
        if i > 850:
            pid.SetPoint = 1
        if i > 900:
            pid.SetPoint = 1 + np.random.normal(mu_5, sigma_5, 1)[0]
            # pid.SetPoint = 1
        if i > 950:
            pid.SetPoint = 1
        if i > 1000:
            pid.SetPoint = 2
        """