### RPM external doxygen 1.8.16
%define doxygen_release Release_%(echo %{realversion} | tr '.' '_')

Source: https://github.com/doxygen/doxygen/archive/%{doxygen_release}.tar.gz
#Source: http://ftp.stack.nl/pub/users/dimitri/%{n}-%{realversion}.src.tar.gz
BuildRequires: flex bison graphviz autotools gmake cmake python

#define drop_files %{i}/man

%prep
%setup -n %{n}-%{doxygen_release}

%build
rm -rf ../build
mkdir -p ../build
cd ../build

cmake ../%{n}-%{doxygen_release} \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -Dbuild_doc=OFF \
  -Denglish_only=ON

make %{makeprocesses}

%install
cd ../build
make install
