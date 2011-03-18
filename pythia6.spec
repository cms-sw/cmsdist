### RPM external pythia6 424
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
case %cmsplatf in
  slc*)
    PLATF_LD=`which gfortran`
    PLATF_CONFIG_OPTS="--enable-shared --disable-static"
    ;;
  osx*_*_gcc*)
    PLATF_LDFLAGS="-Wl,-commons,use_dylibs -Wl,-flat_namespace"
    PLATF_LD=`which gcc`
    PLATF_CONFIG_OPTS="--disable-shared --enable-static"
  ;;
  *)
    echo "Make sure you handle commons!" ; exit 1 ;;
esac

# Make sure we always build -fPIC, even if we use archive libraries.
PLATF_F77="`which gfortran` -fPIC"

%setup -q -n %{n}/%{realversion}

./configure $PLATF_CONFIG_OPTS --with-hepevt=4000 \
            F77="$PLATF_F77" LD="$PLATF_LD" LDFLAGS="$PLATF_LDFLAGS"
# NOTE: force usage of gcc to link shared libraries in place of gfortran since
# the latter causes a:
#
# ld: codegen problem, can't use rel32 to external symbol __gfortrani_compile_options in __gfortrani_init_compile_options
#
# error when building.
# I couldn't find any better way to replace "CC" in the F77 section of libtool.
case %cmsplatf in
  osx*)
    perl -p -i -e 's|^CC=.*$|CC=gcc|' libtool
  ;;
esac

%build
make 
make install

%install
tar -c lib include | tar -x -C %i
