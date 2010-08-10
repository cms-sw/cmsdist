### RPM external herwigpp 2.4.2
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

#
# Careful to change or get rid of the next line when the version changes
#
%define srcTag 2.4.2
#Source: http://projects.hepforge.org/herwig/files/Herwig++-%{srcTag}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/herwig++-%{srcTag}-src.tgz
Requires: thepeg
Requires: gsl
Requires: hepmc

Patch0: herwigpp-2.4.2-amd64

%prep
%setup -q -n %{n}/%{realversion}
case %gccver in
  3.*)
%patch0 -p2
  ;;
esac

%build
./configure --with-hepmc=$HEPMC_ROOT --with-gsl=$GSL_ROOT --with-thepeg=$THEPEG_ROOT --prefix=%i CXXFLAGS="-O2 -fuse-cxa-atexit"
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
