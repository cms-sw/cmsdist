### RPM external xtensor 0.20.1
Source: https://github.com/QuantStack/xtensor/archive/%{realversion}.tar.gz
BuildRequires: cmake
Requires: xtl

%prep
%setup -n %{n}-%{realversion}

%build

cmake -DCMAKE_INSTALL_PREFIX=%{i} -Dxtl_DIR=${XTL_ROOT}/lib64/cmake/xtl/
make %{makeprocesses}

%install

make install

# bla bla
