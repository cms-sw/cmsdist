### RPM external cmake 3.10.2
%define downloaddir %(echo %realversion | cut -d. -f1,2)
Source: http://www.cmake.org/files/v%{downloaddir}/%n-%realversion.tar.gz
Requires: bz2lib curl expat zlib

%prep
%setup -n cmake-%realversion

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
# For OS X 10.8 ("Mountain Lion") do not use Objective-C in
# C and C++ code.
case %cmsplatf in
  osx108_*)
    CXXFLAGS="-DOS_OBJECT_USE_OBJC=0" CFLAGS="-DOS_OBJECT_USE_OBJC=0" \
      ./configure --prefix=%i --init=build-flags.cmake --parallel=%compiling_processes
  ;;
  *)
    ./configure --prefix=%i --init=build-flags.cmake --parallel=%compiling_processes
  ;;
esac
make %makeprocesses

%install
make install/strip

# Look up documentation online.
%define drop_files %i/{doc,man}
# bla bla
