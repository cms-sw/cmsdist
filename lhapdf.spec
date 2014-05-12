### RPM external lhapdf 5.8.5
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
%define realversion %(echo %{v} | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch1: lhapdf-5.8.5-gzio
Patch2: lhapdf-data-5.8.5-gzio
Patch3: lhapdf-5.8.5-disable-examples-and-tests
Patch4: lhapdf-mic-5.8.5

Requires: zlib
%if "%mic" != "true"
Requires: python
%endif
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
%patch3 -p2

# Remove wrapper generated w/ SWIG 1.3* version. Makefile will
# regenerate it w/ our SWIG version.
rm ./pyext/lhapdf_wrap.cc

%patch1 -p2

cd share/lhapdf/PDFsets
%patch2 -p5

rm -f *gz NNPDF*1000*
cat <<\EOF > ../compress.mk
FILES=$(addsuffix .gz,$(wildcard *))
all: ${FILES}
%.gz: %
	gzip -9 $<
EOF

make %{makeprocesses} -f ../compress.mk all

%build
# We do everything in install because we need to do it twice.
%install
libtoolize --force --copy
autoupdate
aclocal -I m4
autoconf
automake --add-missing

%if "%mic" == "true"
FC="`which ifort` -mmic -fPIC"
CXX="`which icpc` -mmic -fPIC"
CC="`which icc` -mmic -fPIC"
patch -p0 <%_sourcedir/lhapdf-mic-5.8.5
%else
FC="`which gfortran` -fPIC"
CXX="`which %{cms_cxx}` -fPIC"
CC="`which gcc` -fPIC"
%endif
# Configure first with low memory.
./configure --prefix=%{i} --enable-static --disable-shared --enable-pyext \
            --disable-octave --disable-doxygen --enable-low-memory \
            --with-max-num-pdfsets=1 \
            CPPFLAGS="-I${ZLIB_ROOT}/include" CXXFLAGS="%cms_cxxflags" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"  \
%if "%mic" == "true"
            FC="$FC" CXX="$CXX" CC="$CC" --host=x86_64-k1om-linux --disable-pyext
%else
            FC="$FC" CXX="$CXX" CC="$CC"
%endif
make %{makeprocesses}
make install

# do another install-round for full libs
make distclean
./configure --prefix=%{i}/full --enable-static --disable-shared \
            --enable-pyext --disable-octave --disable-doxygen \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" CXXFLAGS="%cms_cxxflags" LDFLAGS="-L${ZLIB_ROOT}/lib -lz" \
%if "%mic" == "true"
            FC="$FC" CXX="$CXX" CC="$CC" --host=x86_64-k1om-linux --disable-pyext
%else
            FC="$FC" CXX="$CXX" CC="$CC"
%endif
make %{makeprocesses}
make install


mkdir -p %{i}/share/lhapdf/PDFsets
%{i}/bin/lhapdf-getdata --force --repo=http://www.hepforge.org/archive/lhapdf/pdfsets/%{realversion} --dest=%{i}/share/lhapdf/PDFsets cteq6l ct10 MSTW2008nlo68cl
cd %{i}/share/lhapdf/PDFsets
chmod a+x %{_sourcedir}/lhapdf_makeLinks
%{_sourcedir}/lhapdf_makeLinks


# Remove all libtool archives
find %{i} -name '*.la' -exec rm -f {} \;

# Remove egg-info
find %{i} -name '*.egg-info' -delete

%post
%{relocateConfig}bin/lhapdf-config
%{relocateConfig}full/bin/lhapdf-config
