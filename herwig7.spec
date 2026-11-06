### RPM external herwig7 7.2.2
## INCLUDE cpp-standard
%define tag 22022c47c363d202eb5a6c82768f4eaadd281a6d
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/herwig.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: lhapdf
Requires: boost
Requires: hepmc
Requires: yoda 
Requires: thepeg
Requires: gsl OpenBLAS
Requires: fastjet
Requires: gosamcontrib gosam
Requires: madgraph5amcatnlo
Requires: python3
%{!?without_openloops:Requires: openloops}
BuildRequires: autotools

%prep
%setup -q -n %{n}-%{realversion}

# Regenerate build scripts
autoreconf -fiv

%build
EX_FLAGS="-fPIC -std=c++%{cms_cxx_standard}"
%if %{is_debug_build herwig7}
EX_FLAGS="${EX_FLAGS} -g -O0"
%endif
CXX="$(which g++)"
CC="$(which gcc)"
PLATF_CONF_OPTS="--enable-shared --disable-static"
FCFLAGS=""
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then FCFLAGS="-fallow-argument-mismatch" ; fi
%ifnarch x86_64
FCFLAGS="${FCFLAGS} -fno-range-check"
%endif
sed -i -e "s|-lgslcblas|-lopenblas|" ./configure
PYTHON=python3 ./configure --prefix=%i \
            --with-thepeg=$THEPEG_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-boost=$BOOST_ROOT \
            --with-madgraph=$MADGRAPH5AMCATNLO_ROOT \
            --with-gosam=$GOSAM_ROOT \
            --with-gosam-contrib=$GOSAMCONTRIB_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            ${OPENLOOPS_ROOT+--with-openloops=$OPENLOOPS_ROOT} \
            $PLATF_CONF_OPTS \
            CXX="$CXX" CC="$CC" LDFLAGS="-L${OPENBLAS_ROOT}/lib" \
            CXXFLAGS="${EX_FLAGS}" CFLAGS="${EX_FLAGS}" \
            FCFLAGS="$FCFLAGS"

%ifarch riscv64
sed -i -e 's|^install-data-hook:|install-data-hook:\n\techo Skip data\n\ninstall-data-hookX:|' src/Makefile
%endif

make %makeprocesses all V=1

%install
make %makeprocesses install LHAPDF_DATA_PATH=$LHAPDF_ROOT/share/LHAPDF


mv %{i}/bin/Herwig  %{i}/bin/Herwig-cms
cat << \HERWIG_WRAPPER > %{i}/bin/Herwig
#!/bin/bash
REPO_OPT=""
if [ "$HERWIGPATH" != "" ] && [ -e "$HERWIGPATH/HerwigDefaults.rpo" ] ; then
  if [ $(echo " $@" | grep ' --repo' | wc -l) -eq 0 ] ; then REPO_OPT="--repo $HERWIGPATH/HerwigDefaults.rpo" ; fi
fi
$(dirname $0)/Herwig-cms $REPO_OPT "$@"
HERWIG_WRAPPER
chmod +x %{i}/bin/Herwig

sed -i -e 's|^#!.*python|#!/usr/bin/env python3|' %{i}/bin/ufo2herwig %{i}/bin/slha2herwig %{i}/bin/herwig-mergegrids %{i}/bin/gosam2herwig %{i}/bin/mg2herwig
sed -i -e 's|^#!.*python|#!/usr/bin/env python3|' %{i}/lib/Herwig/python/ufo2herwig %{i}/lib/Herwig/python/slha2herwig

%post
%{relocateConfig}bin/herwig-config
%{relocateConfig}bin/Herwig-cms
%{relocateConfig}bin/ufo2herwig
%{relocateConfig}lib/Herwig/*.la
%{relocateConfig}lib/Herwig/python/Makefile-FR
%{relocateConfig}share/Herwig/Makefile-UserModules
%{relocateConfig}share/Herwig/defaults/PDF.in
%{relocateConfig}share/Herwig/HerwigDefaults.rpo
%{relocateConfig}share/Herwig/Doc/*.conf
%{relocateConfig}share/Herwig/defaults/setup.gosam.in
