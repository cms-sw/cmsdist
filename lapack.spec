### RPM external lapack 3.3.0
Source0: http://www.netlib.org/lapack/lapack.tgz
Source1: http://www.netlib.org/lapack/manpages.tgz

Requires: cmake

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n lapack-%{realversion} 
%setup -q -D -T -a 1 -n lapack-%{realversion}

%build
# We remove the testing directory because it seems
# to not build correctly on the mac.
rm -rf TESTING
perl -p -i -e 's|add_subdirectory[(]TESTING[)]||' CMakeLists.txt
cmake . -DBUILD_SHARED_LIBS=YES -DCMAKE_Fortran_COMPILER="`which gfortran`" -DCMAKE_INSTALL_PREFIX="%i"
make %{makeprocesses} 

%install
make install
