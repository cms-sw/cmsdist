### RPM external herwigpp 7.1.4
Source: https://www.hepforge.org/archive/herwig/Herwig-%{realversion}.tar.bz2

Requires: lhapdf
Requires: boost
Requires: hepmc
Requires: yoda 
Requires: thepeg
Requires: gsl 
Requires: fastjet
Requires: gosamcontrib gosam
Requires: madgraph5amcatnlo
%ifnarch ppc64le
Requires: openloops
%endif
BuildRequires: autotools

# Patch since otherwise Boost wants multithreaded lib, even though only single-threaded lib is installed
# Problem exists since Herwig++3Beta
Patch0: herwigpp-missingBoostMTLib
Patch1: herwigpp-7.1.2-gcc8

%prep
%setup -q -n Herwig-%{realversion}

%patch0 -p1
%patch1 -p1

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which g++) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"

./configure --prefix=%i \
            --with-thepeg=$THEPEG_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-boost=$BOOST_ROOT \
	    --with-madgraph=$MADGRAPH5AMCATNLO_ROOT \
            --with-gosam=$GOSAM_ROOT \
            --with-gosam-contrib=$GOSAMCONTRIB_ROOT \
            --with-hepmc=$HEPMC_ROOT \
%ifnarch ppc64le
            --with-openloops=$OPENLOOPS_ROOT \
%endif
%ifnarch x86_64
            FCFLAGS="-fno-range-check" \
%endif
            $PLATF_CONF_OPTS \
            CXX="$CXX" CC="$CC"
make %makeprocesses all

%install
make %makeprocesses install LHAPDF_DATA_PATH=$LHAPDF_ROOT/share/LHAPDF

#FxFx.so needs to be build after herwigpp installation so that it can correctly pick up needed headers
#FIX for 7.1.4: need to fix path in Makefile to build the FxFx.so library correctly
#Maybe not needed for future versions.  Bug has been reported to the authors
sed -i -e "s|UEBase.fh|Shower/UEBase.fh|g" Shower/UEBase.h
sed -i -e "s|Herwig/Shower/Couplings/ShowerAlpha.h|Herwig/Shower/Core/Couplings/ShowerAlpha.h|g" Contrib/FxFx/FxFxHandler.h
sed -i -e "s|^HERWIGINCLUDE.*|HERWIGINCLUDE = -I%{i}/include|g" Contrib/FxFx/Makefile
sed -i -e "s|^RIVETINCLUDE.*|RIVETINCLUDE = -I${RIVET_ROOT}/include|g" Contrib/FxFx/Makefile
sed -i -e "s|^HEPMCINCLUDE.*|HEPMCINCLUDE = -I${HEPMC_ROOT}/include|g" Contrib/FxFx/Makefile
sed -i "/^FASTJETLIB.*/a YODAINCLUDE= -I${YODA_ROOT}/include" Contrib/FxFx/Makefile
sed -i "/^YODAINCLUDE=.*/a BOOSTINCLUDE= -I${BOOST_ROOT}/include" Contrib/FxFx/Makefile
sed -i -e "/^INCLUDE.*/s/$/ \$(YODAINCLUDE) \$(BOOSTINCLUDE)/" Contrib/FxFx/Makefile
sed -i "/^FASTJETLIB.*/a HERWIGINSTALL = %{i}" Contrib/FxFx/Makefile
sed -i -e '0,/\$(HERWIGINSTALL)\/lib\/Herwig/s//\$(HERWIGINSTALL)\/lib\/./' Contrib/FxFx/Makefile

make -C Contrib/FxFx %makeprocesses FxFx.so FxFxHandler.so FxFxAnalysis.so
cp Contrib/FxFx/*.so %{i}/lib/Herwig/.

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

%post
%{relocateConfig}bin/herwig-config
%{relocateConfig}bin/Herwig++
%{relocateConfig}bin/Herwig-cms
%{relocateConfig}bin/ufo2herwig
%{relocateConfig}lib/Herwig/*.la
%{relocateConfig}lib/Herwig/python/Makefile-FR
%{relocateConfig}share/Herwig/Makefile-UserModules
%{relocateConfig}share/Herwig/defaults/PDF.in
%{relocateConfig}share/Herwig/HerwigDefaults.rpo
sed -i -e "s|^.*/BUILDROOT/[0-9a-f][0-9a-f]*%{installroot}/|$CMS_INSTALL_PREFIX/|g" $RPM_INSTALL_PREFIX/%{pkgrel}/share/Herwig/HerwigDefaults.rpo
