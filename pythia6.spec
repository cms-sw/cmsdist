### RPM external pythia6 426
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

%define keep_archives true

%prep
PLATF_CONF_OPTS="--disable-shared --enable-static"
F77="$(which gfortran) -fPIC"

# Notice we need to define LDFLAGS like this to avoid dropping 
# the dynamic linker options on slc5_amd64_gcc434
case %cmsplatf in
  osx*) 
    PLATF_LDFLAGS="LDFLAGS='-Wl,-commons,use_dylibs -Wl,-flat_namespace'"
    PLATF_LDFLAGS=""
    PLATF_LD="LD='$(which gcc)'" ;;
  *)
    PLATF_LD="" ;;
esac

%setup -q -n %{n}/%{realversion}

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
%get_config_sub ./config/config.sub
%get_config_guess ./config/config.guess
chmod +x ./config/config.{sub,guess}

# Unfortunately we need the two cases because LDFLAGS= does not work on linux
# and I couldn't get the space between use_dylibs and -Wl, preseved if
# I tried to have the whole "LDFLAGS=foo" in a variable.
case %cmsplatf in
  osx*)
    ./configure $PLATF_CONF_OPTS --with-hepevt=4000 F77="$F77" \
		LD='$(which gcc)' LDFLAGS='-Wl,-commons,use_dylibs -Wl,-flat_namespace'
  ;;
  *)
    ./configure $PLATF_CONF_OPTS --with-hepevt=4000 F77="$F77" 
  ;;
esac

perl -p -i -e 's|^CC=.*$|CC="gcc -fPIC"|' libtool

%build
make 
make install

%install
tar -c lib include | tar -x -C %i

