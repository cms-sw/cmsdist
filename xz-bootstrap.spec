### RPM external xz-bootstrap 5.2.1
Source0: http://tukaani.org/xz/xz-%{real_version}.tar.gz

%prep
%setup -n xz-%{real_version}

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
