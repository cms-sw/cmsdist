### RPM external byacc 1.73.20210808
%define download_version 20210808
Source: ftp://invisible-island.net/%{n}/%{n}-%{download_version}.tgz

%prep
%setup -q -n %{n}-%{download_version}

%build
./configure --disable-dependency-tracking --prefix=%{i}
make %{makeprocesses}

%install
make install

%define drop_files %{i}/share
