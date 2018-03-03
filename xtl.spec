### RPM external xtl 0.4.1
Source: https://github.com/QuantStack/xtl/archive/%{realversion}.tar.gz
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}

%build

cmake -DCMAKE_INSTALL_PREFIX=%{i}
make %{makeprocesses}

%install

make install

