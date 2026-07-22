set(CMAKE_CXX_REQUIRED 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

cmake_minimum_required(VERSION 4.4.0)
project(PID_Tests)

add_subdirectory(matplotplusplus)
add_subdirectory(pid)
add_subdirectory(test)