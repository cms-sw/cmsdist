### RPM external lapack 3.6.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source0: http://www.netlib.org/lapack/lapack-%realversion.tgz

Requires: cmake

%define keep_archives true

%prep
%setup -q -n lapack-%{realversion}

%build
# We remove the testing directory because it seems
# to not build correctly on the mac.
rm -rf TESTING
perl -p -i -e 's|add_subdirectory[(]TESTING[)]||' CMakeLists.txt
cmake . -DBUILD_TESTING=OFF -DCBLAS=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_Fortran_COMPILER="`which gfortran`" -DCMAKE_INSTALL_PREFIX="%i"
make %{makeprocesses}
make %{makeprocesses}
%install
make install
rm -rf %i/lib64/pkgconfig
# bla bla
