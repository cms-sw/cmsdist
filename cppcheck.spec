### RPM external cppcheck 1.89
Source: https://github.com/danmar/cppcheck/archive/%{realversion}.tar.gz

BuildRequires: cmake gmake
Requires: pcre python

%prep
%setup -n %{n}-%{realversion}
 
%build
cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_GUI=OFF \
  -DHAVE_RULES=OFF \
  -DUSE_MATCHCOMPILER=ON

make %{makeprocesses} VERBOSE=1

%install
make install

%post
