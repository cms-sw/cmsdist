### RPM external lapack 3.3.1
Source0: http://www.netlib.org/lapack/lapack-%realversion.tgz

Requires: cmake

%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

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
