cmake_minimum_required(VERSION 3.8)
project(stud_kovalenko_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

include_directories(include)

add_executable(stud_kovalenko_publisher
  src/student_publisher.cpp
  src/main.cpp
)

ament_target_dependencies(stud_kovalenko_publisher
  rclcpp
  std_msgs
)

install(TARGETS
  stud_kovalenko_publisher
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()