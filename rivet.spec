### RPM external rivet 2.4.0
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/rivet/rivet-%{realversion}-src.tgz

Requires: hepmc boost fastjet gsl yaml-cpp yoda
Requires: python cython

Patch0: rivet-1.4.0

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++11
%endif

%prep
%setup -n rivet/%{realversion}
%patch0 -p0

# Update config.{guess,sub} to detect aarch64 and ppc64le
rm -f %{_tmppath}/config.{sub,guess}
curl -L -k -s -o %{_tmppath}/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
curl -L -k -s -o %{_tmppath}/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
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

./configure --disable-silent-rules --prefix=%{i} --with-boost=${BOOST_ROOT} --with-hepmc=${HEPMC_ROOT} \
            --with-fastjet=${FASTJET_ROOT} --with-gsl=$GSL_ROOT --with-yoda=${YODA_ROOT} \
            --with-yaml-cpp=${YAML_CPP_ROOT} \
            --disable-doxygen --disable-pdfmanual --with-pic \
            PYTHONPATH=${CYTHON_ROOT}/${PYTHON_LIB_SITE_PACKAGES} \
            CXX="$(which %cms_cxx)" CXXFLAGS="%cms_cxxflags" CPPFLAGS="-I${BOOST_ROOT}/include"

# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC|g" bin/Makefile
%build
make %{makeprocesses} all PYTHONPATH=${CYTHON_ROOT}/${PYTHON_LIB_SITE_PACKAGES}
%install
make install PYTHONPATH=${CYTHON_ROOT}/${PYTHON_LIB_SITE_PACKAGES}

%post
%{relocateConfig}bin/rivet-config
%{relocateConfig}bin/rivet-buildplugin
