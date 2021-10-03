#!/bin/python3
import tkinter as tk

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from rclpy.qos import QoSProfile, QoSHistoryPolicy

class Application(tk.Frame):
    def __init__(self, master=None):
        self.number = 0

        # --- tkinter init ---
        super().__init__(master)
        self.pack()
        self.create_widgets()

        # --- ros2 init ---
        rclpy.init()
        self.node = Node('button_main')
        self.pub = self.node.create_publisher(Int32, '/int', QoSProfile(depth=10, history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST))

    def __del__(self):
        self.node.destroy_node()

    def create_widgets(self):
        # --- tkinter button ---
        self.send_time_btn = tk.Button(self)
        self.send_time_btn["text"] = "-1 Button"
        self.send_time_btn.pack(side="top")
        self.send_time_btn.bind("<Button-1>", self.button_update)
        
        # --- tkinter label ---
        self.time_label = tk.Label(self)
        self.time_label["text"] = "Pub Int32: "
        self.time_label.after(1000, self.timer_update)
        self.time_label.pack(side="top")

    # --- tkinter button event ---
    def button_update(self, event):
        self.number -= 1
        self.pub_int32(self.number)
    
    # --- tkinter loop 1sec ---
    def timer_update(self):
        self.number += 1
        self.time_label["text"] = "Pub Int32: " + str(self.number)
        self.time_label.after(1000, self.timer_update)
        self.pub_int32(self.number)

    # --- ros2 publish ---
    def pub_int32(self, number: int):
        time_msg = Int32()
        time_msg.data = number
        self.pub.publish(time_msg)

# main --------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
