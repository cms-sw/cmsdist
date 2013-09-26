### RPM external libpng 1.6.0
Source: http://download.sourceforge.net/%{n}/%{n}-%{realversion}.tar.gz
%define online %(case %{cmsplatf} in (*onl_*_*) echo true;; (*) echo false;; esac)
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%else
BuildRequires: cmake
%endif

%if "%{online}" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif

%prep
%setup -n %{n}-%{realversion}
 
%build
%if "%mic" == "true"
cmake . \
  -DCMAKE_C_COMPILER="icc" \
  -DCMAKE_C_FLAGS="-fPIC -mmic" \
  -DCMAKE_CXX_COMPILER="icpc" \
  -DCMAKE_CXX_FLAGS="-fPIC -mmic" \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DBUILD_SHARED_LIBS=YES \
  -DZLIB_INCLUDE_DIR:PATH=${ZLIB_ROOT}/include \
  -DZLIB_LIBRARY:FILEPATH=${ZLIB_ROOT}/lib/libz.so \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DCMAKE_SKIP_RPATH=YES \
  -DSKIP_INSTALL_FILES=1
%else
cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DBUILD_SHARED_LIBS=YES \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DCMAKE_SKIP_RPATH=YES \
  -DSKIP_INSTALL_FILES=1
%endif
make %{makeprocesses} VERBOSE=1

%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng16-config
