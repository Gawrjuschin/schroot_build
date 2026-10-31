cmake_minimum_required(VERSION 4.1)

project(
  example
  VERSION 1.0.0
  LANGUAGES CXX)

#
# Targets
#
add_library(example)

target_sources(
  example
  PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src/example.cpp
  PUBLIC FILE_SET HEADERS BASE_DIRS ${CMAKE_CURRENT_LIST_DIR}/include FILES
         ${CMAKE_CURRENT_LIST_DIR}/include/example/example.hpp)

add_executable(hello)
target_sources(hello PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src/main.cpp)
target_link_libraries(hello PRIVATE example)

#
# Install
#
include(GNUInstallDirs)

install(
  TARGETS example
  EXPORT ${PROJECT_NAME}-targets
  DESTINATION ${CMAKE_INSTALL_LIBDIR}
  FILE_SET HEADERS
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(
  EXPORT ${PROJECT_NAME}-targets
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  NAMESPACE ${PROJECT_NAME}::
  FILE ${PROJECT_NAME}-config.cmake)

#
# Packaging
#
set(CPACK_GENERATOR "DEB")
set(CPACK_PACKAGE_CONTACT "Dmitriy Gavryushin <nihsuyrvag@gmail.com>")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY
    "An Cmake based C++ project build using schroot")
set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")

# Auto deps search
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS_PRIVATE_DIRS
    "${CMAKE_SYSROOT}/usr/lib;${CMAKE_SYSROOT}/lib")

include(CPack)
