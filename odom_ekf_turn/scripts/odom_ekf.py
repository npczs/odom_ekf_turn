#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry


class OdomEKF():
   odom= Odometry()
   def __init__(self):
       # Give the node a name
       rospy.init_node('odom_ekf', anonymous=False)

       # Publisher of type nav_msgs/Odometry
       self.ekf_pub = rospy.Publisher('output', Odometry, queue_size=10)
       
       # Wait for the /odom_combined topic to become available
       rospy.wait_for_message('input', PoseWithCovarianceStamped)
       
       # Subscribe to the /odom_combined topic
       rospy.Subscriber('input', PoseWithCovarianceStamped, self.pub_ekf_odom)
       rospy.Subscriber('/odom', Odometry, self.pub_ekf_odom2)
       rospy.loginfo("Publishing combined odometry on /odom_ekf")
       
   def pub_ekf_odom(self, msg):
       
       self.odom.header = msg.header
       self.odom.header.frame_id = '/odom'
       self.odom.child_frame_id = 'base_footprint'
       self.odom.pose = msg.pose
      

   def pub_ekf_odom2(self, msg2):

       self.odom.twist = msg2.twist
       self.ekf_pub.publish(self.odom)
       
if __name__ == '__main__':
      
   try:
     
       OdomEKF()
       rospy.spin()
   except:
       pass
