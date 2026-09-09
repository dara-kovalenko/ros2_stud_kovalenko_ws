#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureMonitor(Node):
    def __init__(self):
        super().__init__('stud_kovalenko_monitor')
        self.get_logger().info("Temperature Monitor started")
        
        self.sub_celsius = self.create_subscription(
            Float32, '/stud_kovalenko/temperature/celsius', self.celsius_callback, 10)
            
        self.sub_fahrenheit = self.create_subscription(
            Float32, '/stud_kovalenko/temperature/fahrenheit', self.fahrenheit_callback, 10)

    def celsius_callback(self, msg):
        temp = msg.data
        if temp > 25.0:
            self.get_logger().warning(f"УВАГА! Температура зависока: {temp:.1f} °C")
        elif temp < 15.0:
            self.get_logger().info(f"Холодно: {temp:.1f} °C")
        else:
            self.get_logger().info(f"Норма: {temp:.1f} °C")

    def fahrenheit_callback(self, msg):
        self.get_logger().info(f"Температура у Фаренгейтах: {msg.data:.1f} °F")

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureMonitor()
    
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()