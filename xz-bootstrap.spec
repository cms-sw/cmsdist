### RPM external xz-bootstrap 5.2.1
Source0: http://tukaani.org/xz/xz-%{realversion}.tar.gz

%prep
%setup -n xz-%{realversion}

%build
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
