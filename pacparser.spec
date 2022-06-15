### RPM external pacparser 1.4.0
Source: https://github.com/%{n}/%{n}/releases/download/v%{realversion}/%{n}-v%{realversion}.tar.gz

%prep
%setup -n %{n}-v%{realversion}

%build
make -C src PREFIX=%{i}

%install
make -C src install PREFIX=%{i}

find %{i}/lib -type f | xargs chmod 0755

%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
