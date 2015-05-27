### RPM external rivet 2.2.1
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/rivet/rivet-%{realversion}-src.tgz

Requires: hepmc boost fastjet gsl yaml-cpp yoda
Requires: python cython

Patch0: rivet-1.4.0
Patch1: rivet-2.2.1

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -n rivet/%{realversion}
%patch0 -p0
%patch1 -p0

./configure --disable-silent-rules --prefix=%i --with-boost=${BOOST_ROOT} --with-hepmc=$HEPMC_ROOT \
            --with-fastjet=$FASTJET_ROOT --with-gsl=$GSL_ROOT --with-yoda=${YODA_ROOT} \
            --with-yaml-cpp=${YAML_CPP_ROOT} \
            --disable-doxygen --disable-pdfmanual --with-pic \
            PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages \
            CXX="$(which %cms_cxx)" CXXFLAGS="%cms_cxxflags" CPPFLAGS="-I${BOOST_ROOT}/include"

# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC|g" bin/Makefile
%build
make %makeprocesses all PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages
%install
make install PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages

%post
%{relocateConfig}bin/rivet-config
%{relocateConfig}bin/rivet-buildplugin
