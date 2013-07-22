### RPM external doxygen 1.8.4

Source: http://ftp.stack.nl/pub/users/dimitri/%{n}-%{realversion}.src.tar.gz

BuildRequires: flex bison graphviz

%define drop_files %{i}/man

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11
%endif

%prep
%setup -n %{n}-%{realversion}

%build

./configure \
  --prefix %{i} \
  --release \
  --english-only

make %{makeprocesses} \
  CXX="%{cms_cxx}" \
  CXXFLAGS="-pipe -fno-exceptions -fno-rtti -D_LARGEFILE_SOURCE -DENGLISH_ONLY -Wall -W -O2 %{cms_cxxflags}"

%install

make install
