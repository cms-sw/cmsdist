### RPM external sherpa 2.2.16
Source: git+https://gitlab.com/sherpa-team/sherpa.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz 
Requires: hepmc lhapdf blackhat sqlite python3 fastjet openmpi hepmc3
BuildRequires: mcfm swig autotools
Patch0: sherpa-2.2.16-hepmcshort
#Avoid calling setenv: https://gitlab.com/sherpa-team/sherpa/-/commit/6ead62d7a2758612f8965fb5b61df8c012cf9cae.diff
Patch1: sherpa-setenv
#Disable build Manual and Examples
Patch2: sherpa-disable-manual

%{!?without_openloops:Requires: openloops}

%prep
%setup -q -n sherpa-%{realversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1

autoreconf -i --force

# Force architecture based on %%cmsplatf
%ifarch x86_64
  ARCH_CMSPLATF="-m64"
%endif

%build
export PYTHON=$(which python3)
./configure --prefix=%i --enable-analysis --disable-silent-rules \
            --enable-fastjet=$FASTJET_ROOT \
            --enable-hepmc2=$HEPMC_ROOT \
            --enable-hepmc3=$HEPMC3_ROOT \
            --enable-lhapdf=$LHAPDF_ROOT \
            --enable-blackhat=$BLACKHAT_ROOT \
            --enable-pyext \
            --enable-ufo \
            ${OPENLOOPS_ROOT+--enable-openloops=$OPENLOOPS_ROOT} \
            --enable-mpi \
            --with-sqlite3=$SQLITE_ROOT \
            --enable-analysis \
            CC="mpicc" \
            CXX="mpicxx" \
            MPICXX="mpicxx" \
            FC="mpifort" \
            CXXFLAGS="-fuse-cxa-atexit $ARCH_CMSPLATF -O2 -std=c++0x -I$LHAPDF_ROOT/include -I$BLACKHAT_ROOT/include -I$RIVET_ROOT/include" \
            LDFLAGS="-ldl -L$BLACKHAT_ROOT/lib/blackhat -L$QD_ROOT/lib"

make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -delete
sed -i -e 's|^#!/.*|#!/usr/bin/env python3|' %{i}/bin/Sherpa-generate-model

%post
%{relocateConfig}lib/python%{cms_python3_major_minor_version}/site-packages/ufo_interface/sconstruct_template
%{relocateConfig}bin/make2scons
%{relocateConfig}share/SHERPA-MC/makelibs
%{relocateConfig}bin/Sherpa-config
%{relocateConfig}bin/Sherpa-generate-model
%{relocateConfig}include/SHERPA-MC/ATOOLS/Org/CXXFLAGS*.H
