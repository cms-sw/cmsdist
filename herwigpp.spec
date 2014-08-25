### RPM external herwigpp 2.7.1
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/herwig++/herwig++-%{realversion}-src.tgz
Requires: thepeg
Requires: gsl
Requires: boost
Requires: hepmc

%prep
%setup -q -n herwig++/%{realversion}

%build
./configure --with-gsl=$GSL_ROOT --with-thepeg=$THEPEG_ROOT --with-boost=${BOOST_ROOT} --prefix=%i \
  CXXFLAGS="-O2 -fuse-cxa-atexit"

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
