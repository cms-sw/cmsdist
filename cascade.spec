### RPM external cascade 2.2.04

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: cascade-2.2.0-nomanual
Patch1: cascade-2.2.04-getenv
# Drop dcasrn symbol, which we need to redifine in CMSSW. Do not build cascade
# executable, since it would use the wrong symbol in anycase.
Patch2: cascade-2.2.04-drop-dcasrn
Requires: lhapdf pythia6

%define keep_archives true

%prep
rm -rf %{n}
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2
%patch2 -p1

# Notice that cascade expects a flat pythia installation,
# where libraries and headers are all in the same place.
# Since the source code is not actually needed, we point
# it to the library location so that it links correctly.
PYTHIA="$PYTHIA6_ROOT"
LHAPDF="$LHAPDF_ROOT"
F77="$(which gfortran) -fPIC"
PLATF_CONFIG_OPTS="--enable-static --disable-shared"
LIBS="-lstdc++ -lz"

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
chmod +x ./config.{sub,guess}

./configure $PLATF_CONFIG_OPTS --with-pythia6=$PYTHIA  --with-lhapdf=$LHAPDF --prefix=%i F77="$F77" LIBS="$LIBS" 
%build
make %makeprocesses

%install
make install

# In case we build archive libraries we need to merge all of them, because
# otherwise that results some missing symbol due to a circular dependency among
# them which cannot be solved by reshuffling the various -l statements.
cd %{i}/lib
find . -name '*.a' -exec ar -x {} \;
ar rcs libcascade_merged.a *.o
rm -rf *.o
