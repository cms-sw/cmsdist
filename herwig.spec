### RPM external herwig 6.521
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Requires: lhapdf photos 
Patch1: herwig-6.520-tauoladummy

%define keep_archives true

%prep
%setup -q -n %n/%{realversion}
F77="$(which gfortran) -fPIC"
PLATF_CONFIG_OPTS="--disable-shared --enable-static"

%patch1 -p2

# Update to detect aarch64 and ppc64le
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

./configure $PLATF_CONFIG_OPTS --prefix=%i F77="$F77"

%build
make %{makeprocesses} LHAPDF_ROOT=$LHAPDF_ROOT PHOTOS_ROOT=$PHOTOS_ROOT

make check

%install
make install

# then hack include area as jimmy depends on missing header file..
# but only on slc*. On macosx HERWIG65.INC == herwig65.inc
# what is actually needed is a link to herwig6510.inc
%ifos darwin
ln -sf herwig6521.inc %{i}/include/herwig65.inc
%else
ln -sf HERWIG65.INC %{i}/include/herwig65.inc
%endif

rm -rf %i/lib/*.la
# bla bla
