#!/usr/bin/env python
#encoding: utf8
import rospy, os
import socket, time

class JuliusReceiver:
    def __init__(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("localhost",10500))
                break
            except:
                rate.sleep()

        rospy.on_shutdown(self.sock.close)

    def get_line(self):
        line = ""
        while not rospy.is_shutdown():
            v = self.sock.recv(1)
            line += v
            if v == '\n':
                return line

    def output(self):
        while not rospy.is_shutdown():
            command = None
            line = self.get_line()
            if "左" in line:   command = "left"
            elif "右" in line: command = "right"
            elif "前" in line: command = "forward"
            elif "後" in line: command = "back"
        
            if command == None:
                continue
        
            print command

if __name__ == '__main__': 
    rospy.init_node("voice_to_command")
    JuliusReceiver().output()
   
