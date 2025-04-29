### RPM external xz-bootstrap 5.6.4
%define keep_archives true
Source0: http://tukaani.org/xz/xz-%{realversion}.tar.gz

%prep
%setup -n xz-%{realversion}

%build
./configure CFLAGS='-fPIC -D_FILE_OFFSET_BITS=64 -Ofast' --prefix=%{i} --disable-shared --enable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
