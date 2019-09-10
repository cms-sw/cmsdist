### RPM external cppcheck 1.89
Source: https://github.com/danmar/cppcheck/archive/%{realversion}.tar.gz

BuildRequires: cmake gmake
Requires: pcre

%prep
%setup -n %{n}-%{realversion}
 
%build
cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DBUILD_GUI=OFF \
  -DHAVE_RULE=ON \
  -DUSE_MATCHCOMPILER=ON

make %{makeprocesses} VERBOSE=1

%install
make install

%post
