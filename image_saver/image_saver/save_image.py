import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from sensor_msgs.msg import Image, CameraInfo
import cv_bridge
import cv2
import rclpy.qos as qos


class saver(Node):
    def __init__(self):
        super().__init__("saver")
        self.profile1 = qos.QoSProfile(reliability=qos.QoSReliabilityPolicy.BEST_EFFORT, history=qos.QoSHistoryPolicy.KEEP_LAST, depth=5)
        self.im_subscriber = self.create_subscription(Image, "/zenith_camera/image_raw", self.im_callback, qos_profile=self.profile1)
        self.profile2 = qos.QoSProfile()
        self.str_subscriber = self.create_subscription(Int32, "/cmd", self.str_callback, 10)
        self.cmd = 0
        self.spin = True

    def str_callback(self, msg):
        print("\tclb_str")
        self.cmd = msg.data

    def im_callback(self, msg):
        print("clb_im")
        bridge = cv_bridge.CvBridge()
        cv_im = bridge.imgmsg_to_cv2(msg.data)
        if self.cmd == 1:
            print("cmd = 1, affichage window")
            cv2.imshow("cv_im", cv_im)
        elif self.cmd == 2:
            cv2.imwrite("/home/user/Documents/UE5.8/CrabeBot_ws/src/TennisBallCollector/image_saver/data/im001.png", cv_im)
            self.spin = False
            print("sauvegarde done")
        elif self.cmd == 0:
            cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = saver()
    
    rate = node.create_rate(10)
    while node.spin:
        rate.sleep()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()