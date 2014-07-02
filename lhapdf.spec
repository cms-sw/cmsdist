### RPM external lhapdf 5.9.1

%define realversion %(echo %{v} | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: lhapdf-5.9.0-disable-examples-and-tests
Patch1: lhapdf-5.9.1-tests-no-srcdir

Source1: lhapdf_makeLinks

Requires: python
BuildRequires: autotools swig

%define keep_archives true
%if "%(case %{cmsplatf} in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
%patch1 -p2

# Remove wrapper generated w/ SWIG 1.3* version. Makefile will
# regenerate it w/ our SWIG version.
rm ./pyext/lhapdf_wrap.cc

%build
# We do everything in install because we need to do it twice.
%install
autoreconf -fiv

FC="`which gfortran` -fPIC"
CXX="`which %{cms_cxx}` -fPIC"
CC="`which gcc` -fPIC"

# Configure first with low memory.
./configure --prefix=%{i} --enable-static --disable-shared --enable-pyext \
            --disable-octave --disable-doxygen --enable-low-memory \
            --with-max-num-pdfsets=1 \
            FC="$FC" CXX="$CXX" CC="$CC" \
            CXXFLAGS="%cms_cxxflags"
make %{makeprocesses}
make install

# do another install-round for full libs
make distclean
./configure --prefix=%{i}/full --enable-static --disable-shared \
            --enable-pyext --disable-octave --disable-doxygen \
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
