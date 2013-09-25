### RPM external pythia6 426
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%define keep_archives true

%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
# NOTE: Old gcc versions (up to 4.3.4) were building 
#       dynamic libraries. from 4.5.1 (and on mac)
#       we build archive ones.
case %cmsplatf in
  *_mic_*) 
    PLATF_CONF_OPTS="--enable-shared"
    F77="`which ifort` -mmic"
  ;;
  slc5_*_gcc4[01234]*) 
    PLATF_CONF_OPTS="--enable-shared"
    F77="`which gfortran`"
  ;;
  *) 
    PLATF_CONF_OPTS="--disable-shared --enable-static"
    F77="`which gfortran` -fPIC"
  ;;
esac

# Notice we need to define LDFLAGS like this to avoid dropping 
# the dynamic linker options on slc5_amd64_gcc434
case %cmsplatf in
  osx*) 
    PLATF_LDFLAGS="LDFLAGS='-Wl,-commons,use_dylibs -Wl,-flat_namespace'"
    PLATF_LDFLAGS=""
    PLATF_LD="LD='`which gcc`'" ;;
  *)
    PLATF_LD="" ;;
esac

%setup -q -n %{n}/%{realversion}

# Unfortunately we need the two cases because LDFLAGS= does not work on linux
# and I couldn't get the space between use_dylibs and -Wl, preseved if
# I tried to have the whole "LDFLAGS=foo" in a variable.
case %cmsplatf in
  osx*)
    ./configure $PLATF_CONF_OPTS --with-hepevt=4000 F77="$F77" \
		LD='`which gcc`' LDFLAGS='-Wl,-commons,use_dylibs -Wl,-flat_namespace' 
  ;;
  *_mic_*)
    CC="icc -mmic" CXX="icpc -mmic" ./configure --host=x86_64-k1om-linux  $PLATF_CONF_OPTS --with-hepevt=4000 F77="$F77" 
  ;;
  *)
    ./configure $PLATF_CONF_OPTS --with-hepevt=4000 F77="$F77" 
  ;;
esac

# NOTE: force usage of gcc to link shared libraries in place of gfortran since
# the latter causes a:
#
# ld: codegen problem, can't use rel32 to external symbol __gfortrani_compile_options in __gfortrani_init_compile_options
#
# error when building.
# I couldn't find any better way to replace "CC" in the F77 section of libtool.
case %cmsplatf in
  *_mic_*) perl -p -i -e 's|^CC=.*$|CC="icc -fPIC"|' libtool ;;
  slc5_*_gcc4[01234]*) ;;
  *) perl -p -i -e 's|^CC=.*$|CC="gcc -fPIC"|' libtool ;;
esac

%build
make %makeprocesses
make install

%install
tar -c lib include | tar -x -C %i

