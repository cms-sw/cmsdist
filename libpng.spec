### RPM external libpng 1.6.0
Source: http://download.sourceforge.net/%{n}/%{n}-%{realversion}.tar.gz
%define online %(case %{cmsplatf} in (*onl_*_*) echo true;; (*) echo false;; esac)

BuildRequires: cmake

%if "%{online}" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif

%prep
%setup -n %{n}-%{realversion}
 
%build
cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DBUILD_SHARED_LIBS=YES \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DCMAKE_SKIP_RPATH=YES \
  -DSKIP_INSTALL_FILES=1

make %{makeprocesses} VERBOSE=1

%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

%post
%{relocateConfig}bin/libpng-config
%{relocateConfig}bin/libpng16-config
