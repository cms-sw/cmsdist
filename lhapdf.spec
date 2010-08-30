### RPM external lhapdf 5.6.0

%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: lhapdf-5.6.0-g77
Patch1: lhapdf-5.6.0-32bit-on-64bit-recheck-workaround

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif
  
%prep
%setup -q -n %{n}/%{realversion}
# This applies both old and new fixes, probably the gcc4 ones can go (to check) 
case %gccver in
  4.*)
    # Switch to gfortran
    perl -p -i -e 's|^export F77\=g77|export F77=gfortran|' .scripts/platform_functions
    perl -p -i -e 's| -Wno-globals||' configure
  ;;
  3.*)
%patch0 -p2
  ;;
esac
%patch1 -p2

%build
case %cmsplatf in 
  # Looks like configure was generated with an ancient version
  # of autotools which does not work on snow leopard.
  # This seems to fix it.
  osx*)
    glibtoolize --force --copy
    autoupdate 
    aclocal -Im4
    autoconf
    automake --add-missing
  ;;
esac
./configure --disable-pyext --enable-low-memory --prefix=%i --with-max-num-pdfsets=1

perl -p -i -e 's|/usr/lib64/libm.a||g' config.status
perl -p -i -e 's|/usr/lib64/libc.a||g' config.status
perl -p -i -e 's|/usr/lib64/libm.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
perl -p -i -e 's|/usr/lib64/libc.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
make 

%install
make install
# do another install-round for full libs
make distclean
%define fulllibpath %(echo %i"/full")
%define fullname %(echo %n"full")
./configure --disable-pyext --prefix=%fulllibpath --disable-pdfsets
perl -p -i -e 's|/usr/lib64/libm.a||g' config.status
perl -p -i -e 's|/usr/lib64/libc.a||g' config.status
perl -p -i -e 's|/usr/lib64/libm.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
perl -p -i -e 's|/usr/lib64/libc.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
make
make install

%post
%{relocateConfig}lib/libLHAPDF.la
%{relocateConfig}lib/libLHAPDFWrap.la
