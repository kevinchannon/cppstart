cmake_minimum_required(VERSION 3.15)

add_executable(proj_name
  main.cpp
)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set_property(TARGET proj_name PROPERTY CXX_STANDARD 20)

target_compile_options(proj_name PRIVATE
	$<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
	$<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic -Werror>
)

target_include_directories(proj_name PRIVATE
	${CMAKE_SOURCE_DIR}
)

target_link_libraries(proj_name
  PRIVATE
    proj_nameLib::proj_nameLib
)
