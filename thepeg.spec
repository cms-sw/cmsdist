### RPM external thepeg 1.9.2
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib/ThePEG

%define thepegCommit b03496397c12
%define branch cms/v%realversion

Source: git+https://github.com/cms-externals/thepeg.git?obj=%{branch}/%{thepegCommit}&export=thepeg-%{realversion}-%{thepegCommit}&module=thepeg-%realversion-%thepegCommit&output=/thepeg-%{realversion}-%{thepegCommit}.tgz
Requires: lhapdf
Requires: gsl
Requires: hepmc
Requires: zlib
BuildRequires: autotools
# FIXME: rivet?
%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++11
%endif

%prep
%setup -q -n thepeg-%{realversion}-%{thepegCommit}

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which %{cms_cxx}) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"
LIBGFORTRAN="$(gfortran --print-file-name=libgfortran.so)"

case %{cmsplatf} in
  osx*)
    LIBGFORTRAN="$(gfortran --print-file-name=libgfortran.a)"
    LIBQUADMATH="-lquadmath"
    ;;
esac

./configure $PLATF_CONF_OPTS \
            --disable-silent-rules \
            --with-LHAPDF=$LHAPDF_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            --with-gsl=$GSL_ROOT --with-zlib=$ZLIB_ROOT \
            --without-javagui --prefix=%{i} \
            --disable-readline CXX="$CXX" CC="$CC" CXXFLAGS="%{cms_cxxflags}" \
            LIBS="$LIBGFORTRAN -lz $LIBQUADMATH"

make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}lib/ThePEG/Makefile.common
%{relocateConfig}lib/ThePEG/Makefile
%{relocateConfig}lib/ThePEG/ThePEGDefaults.rpo
%{relocateConfig}lib/ThePEG/ThePEGDefaults-1.9.2.rpo
