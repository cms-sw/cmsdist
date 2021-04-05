### RPM external rivet 3.1.3
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
## OLD GENSER Source: http://cern.ch/service-spi/external/MCGenerators/distribution/rivet/rivet-%{realversion}-src.tgz
Source: git+https://gitlab.com/hepcedar/rivet.git?obj=master/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: hepmc fastjet fastjet-contrib yoda
BuildRequires: python py2-cython py2-setuptools autotools

Patch0: rivet-140-313

%prep
## OLD GENSER: %setup -n rivet/%{realversion}
%setup -n %{n}-%{realversion}
%patch0 -p0

# remove analyses that do not compile
rm analyses/pluginLEP/L3_2008_I825820.cc
rm analyses/pluginBELLE/BELLE_2019_I1762826.cc
rm analyses/pluginBELLE/BELLE_2020_I1796822.cc

# Update config.{guess,sub} to detect aarch64 and ppc64le
rm -f %{_tmppath}/config.{sub,guess}
%get_config_guess %{_tmppath}/config.guess
%get_config_sub %{_tmppath}/config.sub
for CONFIG_GUESS_FILE in $(find $RPM_BUILD_DIR -name 'config.guess')
do
  rm -f $CONFIG_GUESS_FILE
  cp %{_tmppath}/config.guess $CONFIG_GUESS_FILE
  chmod +x $CONFIG_GUESS_FILE
done
for CONFIG_SUB_FILE in $(find $RPM_BUILD_DIR -name 'config.sub')
do
  rm -f $CONFIG_SUB_FILE
  cp %{_tmppath}/config.sub $CONFIG_SUB_FILE
  chmod +x $CONFIG_SUB_FILE
done

case %{cmsplatf} in
  slc6*) sed -i -e 's#^ *OPENMP_CXXFLAGS=.*#OPENMP_CXXFLAGS=#' configure ;;
esac

autoreconf -fiv

#disable building Rivet with OpenMP as it crash executables due to static TLS blocks
%ifarch aarch64
sed -i -e 's|^ax_openmp_flags=".*"|ax_openmp_flags="none"|' ./configure
%endif
CXXFLAGS="-std=c++17"
%ifarch x86_64
    CXXFLAGS="${CXXFLAGS} -msse3"
%endif

./configure --disable-silent-rules --prefix=%{i} --with-hepmc=${HEPMC_ROOT} \
            --with-fastjet=${FASTJET_ROOT} --with-fjcontrib=${FASTJET_CONTRIB_ROOT} --with-yoda=${YODA_ROOT} \
            --disable-doxygen --disable-pdfmanual --with-pic \
            CXX="$(which g++)" CPPFLAGS="-I${BOOST_ROOT}/include" CXXFLAGS="${CXXFLAGS}"
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC|g" bin/Makefile
%build
make %{makeprocesses} all 
%install
make install 

%post
%{relocateConfig}bin/rivet-config
%{relocateConfig}bin/rivet-buildplugin
