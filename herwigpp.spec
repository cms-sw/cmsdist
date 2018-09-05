### RPM external herwigpp 7.1.4
Source: https://www.hepforge.org/archive/herwig/Herwig-%{realversion}.tar.bz2

# Tried to comment out the parts which build HerwigDefaults.rpo during make install

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isaarch64 %(case %{cmsplatf} in (*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)

Requires: lhapdf
Requires: boost 
Requires: hepmc
Requires: yoda
Requires: thepeg
Requires: gsl 
Requires: fastjet
Requires: gosamcontrib gosam
Requires: madgraph5amcatnlo


%if %isamd64
Requires: openloops
%endif

# Patch since otherwise Boost wants multithreaded lib, even though only single-threaded lib is installed
# Problem exists since Herwig++3Beta

Patch0: herwigpp-missingBoostMTLib

BuildRequires: autotools

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%prep
%setup -q -n Herwig-%{realversion}

%patch0 -p1 




# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"

./configure $PLATF_CONF_OPTS \
            --with-thepeg=$THEPEG_ROOT \
            --with-fastjet=$FASTJET_ROOT \
            --with-gsl=$GSL_ROOT \
            --with-boost=$BOOST_ROOT \
	    --with-madgraph=$MADGRAPH5AMCATNLO_ROOT \
            --with-gosam=$GOSAM_ROOT \
            --with-gosam-contrib=$GOSAMCONTRIB_ROOT \
	    --with-hepmc=$HEPMC_ROOT \
%if %isamd64
            --with-openloops=$OPENLOOPS_ROOT \
%endif
            --prefix=%i \
            CXX="$CXX" CC="$CC" \
%if %isaarch64
            FCFLAGS="-fno-range-check" \
%endif
	    BOOST_ROOT="$BOOST_ROOT" LDFLAGS="$LDFLAGS -L$BOOST_ROOT/lib" \
            LD_LIBRARY_PATH=$LHAPDF_ROOT/lib:$GSL_ROOT/lib:$GOSAMCONTRIB_ROOT/lib:$MADGRAPH5AMCATNLO_ROOT/HEPTools/lib:$HEPMC_ROOT/lib:$LD_LIBRARY_PATH


make %makeprocesses all LD_LIBRARY_PATH=$LHAPDF_ROOT/lib:$THEPEG_ROOT/lib/ThePEG:$GSL_ROOT/lib:$FASTJET_ROOT/lib:$BOOST_ROOT/lib:$GOSAMCONTRIB_ROOT/lib:$MADGRAPH5AMCATNLO_ROOT/HEPTools/lib:$LD_LIBRARY_PATH:$HEPMC_ROOT/lib LIBRARY_PATH=$FASTJET_ROOT/lib
#FIX for 7.1.4: need to fix path in Makefile to build the FxFx.so library correctly
#Maybe not needed for future versions.  Bug has been reported to the authors

sed -i -e "s|^HERWIGINCLUDE.*|HERWIGINCLUDE = -I${PWD}/include|g" Contrib/FxFx/Makefile
sed -i -e "s|^RIVETINCLUDE.*|RIVETINCLUDE = -I${RIVET_ROOT}/include|g" Contrib/FxFx/Makefile
sed -i -e "s|^HEPMCINCLUDE.*|HEPMCINCLUDE = -I${HEPMC_ROOT}/include|g" Contrib/FxFx/Makefile
sed -i "/^FASTJETLIB.*/a YODAINCLUDE= -I${YODA_ROOT}/include" Contrib/FxFx/Makefile
sed -i -e "/^INCLUDE.*/s/$/ \$(YODAINCLUDE)/" Contrib/FxFx/Makefile
sed -i "/^FASTJETLIB.*/a HERWIGINSTALL = ${PWD}" Contrib/FxFx/Makefile
sed -i -e '0,/\$(HERWIGINSTALL)\/lib\/Herwig/s//\$(HERWIGINSTALL)\/lib\/./' Contrib/FxFx/Makefile

cd Contrib/FxFx           
make FxFx.so LD_LIBRARY_PATH=${GCC_ROOT}/lib:$LD_LIBRARY_PATH   
make install                                                                                                                                                            
cd - 
# end of fix

%install
make install LD_LIBRARY_PATH=$LHAPDF_ROOT/lib:$THEPEG_ROOT/lib/ThePEG:$GSL_ROOT/lib:$FASTJET_ROOT/lib:$BOOST_ROOT/lib:$GOSAMCONTRIB_ROOT/lib:$MADGRAPH5AMCATNLO_ROOT/HEPTools/lib:$LD_LIBRARY_PATH LIBRARY_PATH=$FASTJET_ROOT/lib:$THEPEG_ROOT/lib/ThePEG:$LHAPDF_ROOT/lib:$GOSAMCONTRIB_ROOT/lib:$HEPMC_ROOT/lib LHAPDF_DATA_PATH=$LHAPDF_ROOT/share/LHAPDF
cp lib/FxFx.so %{i}/lib/Herwig/FxFx.so
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
