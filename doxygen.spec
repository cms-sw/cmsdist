### RPM external doxygen 1.8.11

Source: http://ftp.stack.nl/pub/users/dimitri/%{n}-%{realversion}.src.tar.gz
BuildRequires: flex bison graphviz autotools gmake cmake

#define drop_files %{i}/man

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir -p ../build
cd ../build

export M4=$(which m4)

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -Dbuild_doc=OFF \
  -Denglish_only=ON

make %{makeprocesses}

%install
cd ../build
make install
