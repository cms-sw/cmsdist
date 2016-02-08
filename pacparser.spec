### RPM external pacparser 1.3.5
Source: https://github.com/%{n}/%{n}/releases/download/%{realversion}/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
make -C src PREFIX=%{i}

%install
make -C src install PREFIX=%{i}

%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
