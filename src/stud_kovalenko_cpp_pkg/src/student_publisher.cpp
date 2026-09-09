#include "stud_kovalenko_cpp_pkg/student_publisher.hpp"

using namespace std::chrono_literals;

StudentPublisher::StudentPublisher() : Node("stud_kovalenko_publisher")
{
    counter_ = 1;
    
    RCLCPP_INFO(this->get_logger(), "Publisher started");
    
    publisher_ = this->create_publisher<std_msgs::msg::String>("/stud_kovalenko/message", 10);
    timer_ = this->create_wall_timer(500ms, std::bind(&StudentPublisher::timer_callback, this));
}

void StudentPublisher::timer_callback()
{
    auto message = std_msgs::msg::String();
    message.data = "Kovalenko Message #" + std::to_string(counter_);
    
    RCLCPP_INFO(this->get_logger(), "Publishing: %s", message.data.c_str());
    
    publisher_->publish(message);
    counter_ += 1;
}