### RPM external xz 5.1.2alpha
Source: http://tukaani.org/%{n}/%{n}-%{realversion}.tar.xz

%prep
%setup -n %{n}-%{realversion}

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
