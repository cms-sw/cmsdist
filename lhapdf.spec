### RPM external lhapdf 6.4.0
%define setsversion 6.5.1c

Source: http://www.hepforge.org/archive/lhapdf/LHAPDF-%{realversion}.tar.gz
Source1: lhapdf_makeLinks
Source2: http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MSTW2008nlo68cl.tar.gz
Source3: lhapdf_pdfsetsindex
Requires: python3
BuildRequires: py3-cython

%define keep_archives true

%prep
%setup -q -n LHAPDF-%{realversion}

PYTHON=$(which python3) \
  ./configure --prefix=%{i} \
  --enable-python

%build
make all %makeprocesses 

%install
make install 
mkdir -p %{i}/share/LHAPDF
cd %{i}/share/LHAPDF
cp %{_sourcedir}/MSTW2008nlo68cl.tar.gz .
tar xvfz MSTW2008nlo68cl.tar.gz
rm -f MSTW2008nlo68cl.tar.gz
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
