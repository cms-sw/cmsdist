### RPM external jemalloc 4.5.0
Source: https://github.com/jemalloc/jemalloc/releases/download/%{realversion}/jemalloc-%{realversion}.tar.bz2

%prep
%setup -n %{n}-%{realversion}

%build
./configure --enable-stats --prefix %{i}

%define drop_files %{i}/share
