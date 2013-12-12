### RPM external rivet 1.9.0
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: hepmc boost fastjet swig gsl yamlcpp
Requires: python

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -n rivet/%{realversion}

./configure --disable-silent-rules --prefix=%i --with-boost=${BOOST_ROOT} --with-hepmc=$HEPMC_ROOT \
            --with-fastjet=$FASTJET_ROOT --with-gsl=$GSL_ROOT --with-yaml-cpp=${YAMLCPP_ROOT} \
            --disable-doxygen --disable-pdfmanual --with-pic \
            CXX="$(which %cms_cxx)" CXXFLAGS="%cms_cxxflags"

# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
perl -p -i -e "s|LIBS = $|LIBS = -lHepMC|g" bin/Makefile
%build
make %makeprocesses
%install
make install
