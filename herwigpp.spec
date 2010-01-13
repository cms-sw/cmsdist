### RPM external herwigpp 2.4.0.UEfix
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

#
# Careful to change or get rid of the next line when the version changes
#
%define srcTag 2.4.0-UEfix
Source: http://projects.hepforge.org/herwig/files/Herwig++-%{srcTag}.tar.gz
Requires: thepeg
Requires: gsl
Requires: hepmc

Patch0: herwigpp-2.3.2-g77
Patch1: herwigpp-2.3.2-amd64

%prep
%setup -q -n Herwig++-%{srcTag}
case %gccver in
  3.*)
%patch0 -p1
%patch1 -p1
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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="herwigpp" version="%v">
    <client>
      <environment name="HERWIGPP_BASE" default="%i"/>
      <environment name="LIBDIR" default="$HERWIGPP_BASE/lib"/>
      <environment name="INCLUDE" default="$HERWIGPP_BASE/include"/>
    </client>
    <runtime name="HERWIGPATH" value="$HERWIGPP_BASE/share/Herwig++"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
%{relocateConfig}share/Herwig++/HerwigDefaults.rpo
