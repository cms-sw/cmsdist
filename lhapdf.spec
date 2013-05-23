### RPM external lhapdf 5.8.5

%define realversion %(echo %{v} | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch1: lhapdf-5.8.5-gzio
Patch2: lhapdf-data-5.8.5-gzio
Patch3: lhapdf-5.8.5-disable-examples-and-tests

Requires: zlib
BuildRequires: autotools

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

touch src/gzio.inc ; touch src/gzio.F ; touch src/ftn_gzio.c 
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

make -j %{makeprocesses} -f ../compress.mk all

%build
# We do everything in install because we need to do it twice.
%install
libtoolize --force --copy
autoupdate
aclocal -I m4
autoconf
automake --add-missing

FC="`which gfortran` -fPIC"
CXX="`which %{cms_cxx}` -fPIC"
CC="`which gcc` -fPIC"

# Configure first with low memory.
./configure --prefix=%{i} --enable-static --disable-shared --disable-pyext \
            --disable-octave --disable-doxygen --enable-low-memory \
            --with-max-num-pdfsets=1 \
            FC="$FC" CXX="$CXX" CC="$CC" \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" CXXFLAGS="%cms_cxxflags" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"
make %{makeprocesses}
make install

mkdir %{i}/share/lhapdf/PDFsets
mv share/lhapdf/PDFsets/*gz %{i}/share/lhapdf/PDFsets
pushd %{i}/share/lhapdf/PDFsets
  for x in `ls *.gz`; do
    ln -sf $x `echo $x | sed -e's|\.gz$||'`
  done
popd

# do another install-round for full libs
make distclean
./configure --prefix=%{i}/full --enable-static --disable-shared \
            --disable-pyext --disable-octave --disable-doxygen \
            FC="$FC" CXX="$CXX" CC="$CC" \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" CXXFLAGS="%cms_cxxflags" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"
make %{makeprocesses}
make install

# Remove all libtool archives
find %{i} -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}bin/lhapdf-config
%{relocateConfig}full/bin/lhapdf-config
