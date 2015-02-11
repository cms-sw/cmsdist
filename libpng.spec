### RPM external libpng 1.6.16
%define tag 88dd30b232362b65cca374dda39096888163dd6b
%define branch cms/v1.6.16
%define github_user cms-externals
Source: git+https://github.com/%github_user/%n.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: zlib

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
