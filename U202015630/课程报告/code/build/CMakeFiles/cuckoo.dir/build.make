# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build

# Include any dependencies generated for this target.
include CMakeFiles/cuckoo.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/cuckoo.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cuckoo.dir/flags.make

CMakeFiles/cuckoo.dir/src/cuckoo.cpp.o: CMakeFiles/cuckoo.dir/flags.make
CMakeFiles/cuckoo.dir/src/cuckoo.cpp.o: ../src/cuckoo.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/cuckoo.dir/src/cuckoo.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cuckoo.dir/src/cuckoo.cpp.o -c /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/cuckoo.cpp

CMakeFiles/cuckoo.dir/src/cuckoo.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cuckoo.dir/src/cuckoo.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/cuckoo.cpp > CMakeFiles/cuckoo.dir/src/cuckoo.cpp.i

CMakeFiles/cuckoo.dir/src/cuckoo.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cuckoo.dir/src/cuckoo.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/cuckoo.cpp -o CMakeFiles/cuckoo.dir/src/cuckoo.cpp.s

CMakeFiles/cuckoo.dir/src/graph.cpp.o: CMakeFiles/cuckoo.dir/flags.make
CMakeFiles/cuckoo.dir/src/graph.cpp.o: ../src/graph.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/cuckoo.dir/src/graph.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cuckoo.dir/src/graph.cpp.o -c /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/graph.cpp

CMakeFiles/cuckoo.dir/src/graph.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cuckoo.dir/src/graph.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/graph.cpp > CMakeFiles/cuckoo.dir/src/graph.cpp.i

CMakeFiles/cuckoo.dir/src/graph.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cuckoo.dir/src/graph.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/graph.cpp -o CMakeFiles/cuckoo.dir/src/graph.cpp.s

CMakeFiles/cuckoo.dir/src/main.cpp.o: CMakeFiles/cuckoo.dir/flags.make
CMakeFiles/cuckoo.dir/src/main.cpp.o: ../src/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/cuckoo.dir/src/main.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cuckoo.dir/src/main.cpp.o -c /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/main.cpp

CMakeFiles/cuckoo.dir/src/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cuckoo.dir/src/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/main.cpp > CMakeFiles/cuckoo.dir/src/main.cpp.i

CMakeFiles/cuckoo.dir/src/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cuckoo.dir/src/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/src/main.cpp -o CMakeFiles/cuckoo.dir/src/main.cpp.s

# Object files for target cuckoo
cuckoo_OBJECTS = \
"CMakeFiles/cuckoo.dir/src/cuckoo.cpp.o" \
"CMakeFiles/cuckoo.dir/src/graph.cpp.o" \
"CMakeFiles/cuckoo.dir/src/main.cpp.o"

# External object files for target cuckoo
cuckoo_EXTERNAL_OBJECTS =

cuckoo: CMakeFiles/cuckoo.dir/src/cuckoo.cpp.o
cuckoo: CMakeFiles/cuckoo.dir/src/graph.cpp.o
cuckoo: CMakeFiles/cuckoo.dir/src/main.cpp.o
cuckoo: CMakeFiles/cuckoo.dir/build.make
cuckoo: CMakeFiles/cuckoo.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable cuckoo"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cuckoo.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cuckoo.dir/build: cuckoo

.PHONY : CMakeFiles/cuckoo.dir/build

CMakeFiles/cuckoo.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cuckoo.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cuckoo.dir/clean

CMakeFiles/cuckoo.dir/depend:
	cd /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build /mnt/d/lmq/material/undergraduate/dasan/big_data_storage/cuckoo_hash/build/CMakeFiles/cuckoo.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cuckoo.dir/depend

