### RPM external pythia6 424
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
# NOTE: Old gcc versions (up to 4.3.4) were building 
#       dynamic libraries. from 4.5.1 (and on mac)
#       we build archive ones.
case %cmsplatf in
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
    PLATF_LD="LD='`which gcc`'" ;;
  *)
    PLATF_LD="" ;;
esac

%setup -q -n %{n}/%{realversion}

./configure $PLATF_CONF_OPTS --with-hepevt=4000 \
            F77="$F77" $PLATF_LD $PLATF_LDFLAGS
# NOTE: force usage of gcc to link shared libraries in place of gfortran since
# the latter causes a:
#
# ld: codegen problem, can't use rel32 to external symbol __gfortrani_compile_options in __gfortrani_init_compile_options
#
# error when building.
# I couldn't find any better way to replace "CC" in the F77 section of libtool.
case %cmsplatf in
  slc5_*_gcc4[01234]*) ;;
  *) perl -p -i -e 's|^CC=.*$|CC="gcc -fPIC"|' libtool ;;
esac

%build
make 
make install

%install
tar -c lib include | tar -x -C %i
