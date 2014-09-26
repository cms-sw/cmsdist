### RPM external lhapdf 5.9.1

%define tag 06440aa
%define branch cms/v5.9.1
%define github_user cms-externals
Source: git+https://github.com/%github_user/lhapdf.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
%define realversion %(echo %{v} | cut -d- -f1)

Source1: lhapdf_makeLinks

Requires: python
BuildRequires: autotools swig

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -n %{n}-%{realversion}

%build
# We do everything in install because we need to do it twice.
%install
autoreconf -fiv

FC="`which gfortran` -fPIC"
CXX="`which %{cms_cxx}` -fPIC"
CC="`which gcc` -fPIC"

# Configure first with low memory.
./configure --prefix=%{i} --enable-static --disable-shared --enable-pyext \
            --without-octave --disable-octave --disable-doxygen --enable-low-memory \
            --with-max-num-pdfsets=1 \
            FC="$FC" CXX="$CXX" CC="$CC" \
            CXXFLAGS="%cms_cxxflags"
make %{makeprocesses}
make install

# do another install-round for full libs
make distclean
./configure --prefix=%{i}/full --enable-static --disable-shared \
            --enable-pyext --disable-octave --disable-doxygen \
            --with-max-num-pdfsets=5 \
            FC="$FC" CXX="$CXX" CC="$CC" \
            CXXFLAGS="%cms_cxxflags"
make %{makeprocesses}
make install


mkdir -p %{i}/share/lhapdf/PDFsets
%{i}/bin/lhapdf-getdata --force --repo=http://www.hepforge.org/archive/lhapdf/pdfsets/%{realversion} --dest=%{i}/share/lhapdf/PDFsets cteq6l ct10 MSTW2008nlo68cl
cd %{i}/share/lhapdf/PDFsets
chmod a+x %{_sourcedir}/lhapdf_makeLinks
%{_sourcedir}/lhapdf_makeLinks
cd %{i}/full/share/lhapdf
ln -fs ../../../share/lhapdf/PDFsets PDFsets


# Remove all libtool archives
find %{i} -name '*.la' -exec rm -f {} \;

# Remove egg-info
find %{i} -name '*.egg-info' -delete

%post
%{relocateConfig}bin/lhapdf-config
%{relocateConfig}full/bin/lhapdf-config
