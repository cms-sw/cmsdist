### RPM external lz4 1.9.3

%define github_user lz4
Source: https://github.com/%{github_user}/%{n}/archive/v%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
CC="$(which gcc)" make %{makeprocesses}

%install
make PREFIX=%{i} install

