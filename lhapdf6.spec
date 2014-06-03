### RPM external lhapdf6 6.1.0

%define realversion %(echo %{v} | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Source1: lhapdf6_makeLinks

Source2: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/cteq6l1.tar.gz
Source3: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/CT10.tar.gz
Source4: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MSTW2008nlo68cl.tar.gz

Requires: boost yaml-cpp python cython
BuildRequires: autotools

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
make all PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages

%install
make install PYTHONPATH=${CYTHON_ROOT}/lib/python@PYTHONV@/site-packages
mkdir -p %{i}/share/LHAPDF/PDFsets
cd %{i}/share/LHAPDF/PDFsets
ln -fs ../pdfsets.index pdfsets.index
ln -fs ../lhapdf.conf lhapdf.conf
#wget http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/cteq6l1.tar.gz
cp %{_sourcedir}/cteq6l1.tar.gz .
cp %{_sourcedir}/CT10.tar.gz .
cp %{_sourcedir}/MSTW2008nlo68cl.tar.gz .
tar xvfz cteq6l1.tar.gz
tar xvfz CT10.tar.gz
tar xvfz MSTW2008nlo68cl.tar.gz
rm -f cteq6l1.tar.gz
rm -f CT10.tar.gz
rm -f MSTW2008nlo68cl.tar.gz
chmod a+x %{_sourcedir}/lhapdf6_makeLinks
%{_sourcedir}/lhapdf6_makeLinks
cd -

%post
%{relocateConfig}bin/lhapdf-config
%{relocateConfig}full/bin/lhapdf-config
