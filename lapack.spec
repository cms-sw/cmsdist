### RPM external lapack 3.3.1
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
cmake . -DBUILD_SHARED_LIBS=YES -DCMAKE_Fortran_COMPILER="`which gfortran`" -DCMAKE_INSTALL_PREFIX="%i"
make %{makeprocesses} 

%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
