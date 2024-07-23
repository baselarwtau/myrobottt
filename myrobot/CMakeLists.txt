cmake_minimum_required(VERSION 3.28)
project(myrobot)

set(CMAKE_CXX_STANDARD 20)

add_executable(myrobot main.cpp
        MyAlgorithm.cpp
        MyBattery_meter.cpp
        MyDirt_sensor.cpp
        MySimulator.cpp
        MyWall_sensor.cpp)
