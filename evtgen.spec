### RPM external evtgen 2.0.0

%define tag bcb7af4d35bf66a01c08fa4f8fffb623b7e24c59
%define branch cms/%realversion
%define github_user cms-externals

Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake

Requires: cmake
Requires: hepmc
Requires: pythia8
Requires: tauolapp
Requires: photospp

# See https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40267
# libgfortranbegin.a is finally removed and was obsolete since GCC 4.5
#Patch0: evtgen-1.6.0-configure-new-gcc
Patch0: evtgen-2.0.0

%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake -DCMAKE_INSTALL_PREFIX:PATH=%{i} ../%{n}-%{realversion} \
      -DEVTGEN_HEPMC3:BOOL=OFF -DHEPMC2_ROOT_DIR:PATH=$HEPMC_ROOT \
      -DEVTGEN_PYTHIA:BOOL=ON  -DPYTHIA8_ROOT_DIR:PATH=$PYTHIA8_ROOT \
      -DEVTGEN_PHOTOS:BOOL=ON  -DPHOTOSPP_ROOT_DIR:PATH=$PHOTOSPP_ROOT \
      -DEVTGEN_TAUOLA:BOOL=ON  -DTAUOLAPP_ROOT_DIR:PATH=$TAUOLAPP_ROOT

# One more fix-up for OSX (in addition to the patch above)
%ifos darwin
 perl -p -i -e "s|-shared|-dynamiclib -undefined dynamic_lookup|" make.inc
%endif

make

%install

cd ../build
make install
mkdir -p %i/lib
find %i/lib64 -name "*.*" -exec mv {} %i/lib \;
rm -rf %i/lib64
ls %{i}/lib
cd ..

%post
%relocateConfigAll share/EvtGen/cmake *.cmake
