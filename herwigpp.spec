### RPM external herwigpp 2.7.1
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/herwig++/herwig++-%{realversion}-src.tgz
Requires: boost thepeg gsl hepmc

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n herwig++/%{realversion}

%build
./configure \
  --disable-silent-rules --with-gsl=$GSL_ROOT --with-thepeg=$THEPEG_ROOT --with-boost=${BOOST_ROOT} --prefix=%i \
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

%post
%{relocateConfig}share/Herwig++/HerwigDefaults.rpo
