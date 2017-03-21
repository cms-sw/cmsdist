### RPM external cmake 3.7.0
%define downloaddir %(echo %realversion | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%realversion.tar.gz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
#Patch1: cmake
#Patch2: cmake-osx-nld
Requires: bz2lib curl expat

#We are using system zlib for the online builds:
%if "%online" != "true"
Requires: zlib
%endif

%prep

%setup -n cmake-%realversion
# This patch disables the warning about long doubles that some
# macosx compilers emit. Even if it matters only for macosx,
# we apply it anyway to avoid discrepancies and to avoid that 
# it's left behind if cmake version is changed. 
#%patch2 -p1

%build
cat > build-flags.cmake <<- EOF 
	# Disable Java capabilities; we don't need it and on OS X might miss
        # required /System/Library/Frameworks/JavaVM.framework/Headers/jni.h.
	SET(JNI_H FALSE CACHE BOOL "" FORCE)
	SET(Java_JAVA_EXECUTABLE FALSE CACHE BOOL "" FORCE)
	SET(Java_JAVAC_EXECUTABLE FALSE CACHE BOOL "" FORCE)

	# SL6 with GCC 4.6.1 and LTO requires -ltinfo with -lcurses for link
	# to succeed, but cmake is not smart enough to find it. We don't
	# really need ccmake anyway, so just disable it.
	SET(BUILD_CursesDialog FALSE CACHE BOOL "" FORCE)

	# Use system libraries, not cmake bundled ones.
	SET(CMAKE_USE_SYSTEM_LIBRARY_CURL TRUE CACHE BOOL "" FORCE)
	SET(CMAKE_USE_SYSTEM_LIBRARY_ZLIB TRUE CACHE BOOL "" FORCE)
	SET(CMAKE_USE_SYSTEM_LIBRARY_BZIP2 TRUE CACHE BOOL "" FORCE)
	SET(CMAKE_USE_SYSTEM_LIBRARY_EXPAT TRUE CACHE BOOL "" FORCE)
EOF

export CMAKE_PREFIX_PATH=$CURL_ROOT:$ZLIB_ROOT:$EXPAT_ROOT:$BZ2LIB_ROOT
./configure --prefix=%i --init=build-flags.cmake --parallel=%compiling_processes
make %makeprocesses

%install
make install/strip

# Look up documentation online.
%define drop_files %i/{doc,man}
