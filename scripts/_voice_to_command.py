#!/usr/bin/env python
#encoding: utf8
import rospy, os, socket
from std_srvs.srv import Trigger
from pimouse_ros.srv import TimedMotion

class JuliusReceiver:
    def __init__(self):   #socketの準備だけ
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("localhost",10500))
                break
            except:
                rate.sleep()

        #rospy.on_shutdown(self.sock.close)

    def get_line(self):
        line = ""
        while not rospy.is_shutdown():
            v = self.sock.recv(1)
            if v == '\n':
                return line
            line += v

    def get_command(self,th):
        line = self.get_line()

        if "WHYPO" not in line:
	    return None

        score_str = line.split('CM="')[-1].split('"')[0]
        if float(score_str) < th:
            return None

        command = None
        if "左" in line:   command = "left"
        elif "右" in line: command = "right"
        elif "前" in line: command = "forward"
        elif "後" in line: command = "backward"

        return command

def shutdown():
    j.sock.close()
    rospy.ServiceProxy('/motor_off', Trigger).call()

if __name__ == '__main__': 
    rospy.init_node("voice_to_command")
    rospy.wait_for_service('/timed_motion')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')

    rospy.ServiceProxy('/motor_on', Trigger).call()
    tm = rospy.ServiceProxy('/timed_motion', TimedMotion)

    rospy.on_shutdown(shutdown)

    j = JuliusReceiver()
    while not rospy.is_shutdown():
        com = j.get_command(0.999)
        if com == "left": tm(-400,400,300)
        elif com == "right": tm(400,-400,300)
        elif com == "forward": tm(400,400,3000)
        elif com == "backward": tm(-400,-400,1500)
