### RPM external lhapdf 6.1.6
%define setsversion 6.1.6

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Source1: lhapdf_makeLinks

Source2: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/cteq6l1.tar.gz
Source3: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/CT10.tar.gz
Source4: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MSTW2008nlo68cl.tar.gz
Source5: https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014lo68cl.tar.gz
Source6: https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014nlo68cl.tar.gz

Source7: lhapdf_pdfsetsindex

Requires: boost yaml-cpp python cython

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}

./configure --prefix=%{i} --with-boost=${BOOST_ROOT} --with-yaml-cpp=${YAML-CPP_ROOT} PYTHON=${PYTHON_ROOT}/bin/python CYTHON=${CYTHON_ROOT}/bin/cython PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages

%build
make all %makeprocesses PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages

%install
make install PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages
mkdir -p %{i}/share/LHAPDF
cd %{i}/share/LHAPDF
cp %{_sourcedir}/cteq6l1.tar.gz .
cp %{_sourcedir}/CT10.tar.gz .
cp %{_sourcedir}/MSTW2008nlo68cl.tar.gz .
cp %{_sourcedir}/MMHT2014lo68cl.tar.gz .
cp %{_sourcedir}/MMHT2014nlo68cl.tar.gz .
tar xvfz cteq6l1.tar.gz
tar xvfz CT10.tar.gz
tar xvfz MSTW2008nlo68cl.tar.gz
tar xvfz MMHT2014lo68cl.tar.gz
tar xvfz MMHT2014nlo68cl.tar.gz
rm -f cteq6l1.tar.gz
rm -f CT10.tar.gz
rm -f MSTW2008nlo68cl.tar.gz
rm -f MMHT2014lo68cl.tar.gz
rm -f MMHT2014nlo68cl.tar.gz
chmod a+x %{_sourcedir}/lhapdf_makeLinks
%{_sourcedir}/lhapdf_makeLinks %{setsversion}
rm -f pdfsets.index
cp -f %{_sourcedir}/lhapdf_pdfsetsindex pdfsets.index
cd -

# Remove all libtool archives
find %{i} -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}bin/lhapdf-config
%{relocateConfig}bin/lhapdf
