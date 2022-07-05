### RPM external lcov 1.15
## NOCOMPILER
Source: https://github.com/linux-test-project/%{n}/archive/refs/tags/v%{realversion}.tar.gz
Patch0: lcov-merge-files-in-same-dir
Requires: fakesystem

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%ifarch darwin
# OS X does not support -D option
sed -ibak 's/install -p -D/install -p/g' bin/install.sh
%endif

%build
make %{makeprocesses}

%install
mkdir -p %{i}/bin
make PREFIX=%{i} BIN_DIR=%{i}/bin install
