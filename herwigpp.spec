### RPM external herwigpp 2.5.0
#
# Careful to change or get rid of the next line when the version changes
#
%define srcTag 2.5.0
#Source: http://projects.hepforge.org/herwig/files/Herwig++-%{srcTag}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/herwig++/herwig++-%{srcTag}-src.tgz
Patch0: herwigpp-2.5.0-fix-gcc47-cxx11
Patch1: herwigpp-2.5.0-fix-BaryonFactorizedDecayer-findModes
Requires: thepeg
Requires: gsl
Requires: hepmc

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n herwig++/%{realversion}

%patch0 -p1
%patch1 -p2

%build
./configure \
  --disable-silent-rules --with-gsl=$GSL_ROOT --with-thepeg=$THEPEG_ROOT --prefix=%i \
  CXXFLAGS="-fuse-cxa-atexit %cms_cxxflags" CXX="%cms_cxx"

# Fix up a configuration mistake coming from a test being confused
# by the "skipping incompatible" linking messages when linking 32bit on 64bit
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' Makefile
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' */Makefile
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' */*/Makefile
perl -p -i -e 's|/usr/lib64/libm.a /usr/lib64/libc.a||' */*/*/Makefile

make %makeprocesses 


%install
#tar -c -h lib include | tar -x -C %i
make install
rm %i/share/Herwig++/Doc/fixinterfaces.pl

%post
%{relocateConfig}share/Herwig++/HerwigDefaults.rpo

