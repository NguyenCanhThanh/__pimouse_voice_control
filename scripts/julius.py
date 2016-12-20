#!/usr/bin/env python
import rospy, os
import socket, time

def kill():
    os.system("killall julius")

def get_line(s):
    line = ""
    while not rospy.is_shutdown():
        v = s.recv(1)
        line += v
        if v == '\n':
            return line

def connect():
    while not rospy.is_shutdown():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost",10500))
            return s
        except:
            time.sleep(1.0)


os.chdir(os.path.dirname(__file__) + "/../etc")
rospy.init_node("julius")
rospy.on_shutdown(kill)
os.system("julius -C command.jconf -input mic")

s = connect()
#rate = rospy.Rate(10)

while not rospy.is_shutdown():
    print get_line(s),
#    rate.sleep()
