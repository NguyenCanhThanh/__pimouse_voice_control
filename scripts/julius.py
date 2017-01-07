#!/usr/bin/env python

#motors.py
#Copyright (c) 2016 Ryuichi Ueda <ryuichiueda@gmail.com>
#This software is released under the MIT License.
#http://opensource.org/licenses/mit-license.php

import rospy, os

def kill():
    os.system("killall julius")

os.chdir(os.path.dirname(__file__) + "/../etc")
rospy.init_node("julius")
rospy.on_shutdown(kill)
os.system("julius -C command.jconf -input mic")

rospy.spin()
