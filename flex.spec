### RPM external flex 2.5.37
Source: http://switch.dl.sourceforge.net/project/%{n}/%{n}-%{realversion}.tar.bz2

BuildRequires: autotools

%prep
%setup -q -n %{n}-%{realversion}

%build
./configure --disable-dependency-tracking --disable-nls \
            --build=%{_build} --host="%{_host}" --prefix=%{i}
make %{makeprocesses}

%install
make install

%define drop_files %{i}/share
