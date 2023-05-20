cmake_minimum_required (VERSION 3.15)

project (proj_name)

add_library(proj_nameLib INTERFACE)
add_library(proj_nameLib::proj_nameLib ALIAS proj_nameLib)

set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)

target_include_directories(
  proj_nameLib
  INTERFACE
    $<BUILD_INTERFACE:${INCLUDE_DIR}>
)

# I stole this mechanism from https://github.com/rollbear/trompeloeil/blob/09e013bc0026630f6e721c1ba61a42aa6256d5eb/CMakeLists.txt#L32
# It allows us to be included gracefully in another project via CMake FetchContent
set(MASTER_PROJECT OFF)
if (${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_SOURCE_DIR})
  set(MASTER_PROJECT ON)
endif()

# Include sub-projects.
if (MASTER_PROJECT)
  # The GCC in MinGW requires this, for some reason.
  if(WIN32 AND CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ -lwsock32 -lws2_32 ${CMAKE_CXX_STANDARD_LIBRARIES}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Bstatic,--whole-archive -lwinpthread -Wl,--no-whole-archive")
  endif()

  add_subdirectory(test)
  add_subdirectory(examples)

  set(package_files proj_name/  CMakeLists.txt)
  add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.${PROJECT_VERSION}.zip
    COMMAND ${CMAKE_COMMAND} -E tar c ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.${PROJECT_VERSION}.zip --format=zip -- ${package_files}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${package_files})
  add_custom_target(${PROJECT_NAME}_package DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.${PROJECT_VERSION}.zip)
endif() # MASTER_PROJECT
