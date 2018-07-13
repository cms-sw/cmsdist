### RPM external odb 2.5.0-b.3
Source0: https://codesynthesis.com/~boris/tmp/odb/pre-release/b.3/odb-2.5.0-b.3.tar.gz
Source1: https://codesynthesis.com/~boris/tmp/odb/pre-release/b.3/libcutl-1.11.0-a1.tar.gz
Source2: https://codesynthesis.com/~boris/tmp/odb/pre-release/b.3/libodb-sqlite-2.5.0-b.3.tar.gz
Source3: https://codesynthesis.com/~boris/tmp/odb/pre-release/b.3/libodb-2.5.0-b.3.tar.bz2

Requires: sqlite

%prep
%setup -T -D -b 0 -n odb-%{realversion}
%setup -T -D -b 1 -n libcutl-1.11.0-a1
%setup -T -D -b 2 -n libodb-sqlite-%{realversion}
%setup -T -D -b 3 -n libodb-%{realversion}

%build
cd ../libcutl-1.11.0-a1
./configure --prefix=%{i}
make %{makeprocesses} install
cd ../%{n}-%{realversion}
./configure --prefix=%{i} --with-libcutl=../libcutl-1.11.0-a1
make %{makeprocesses} install
cd ../libodb-%{realversion}
./configure --prefix=%{i}
make %{makeprocesses} install
cd ../libodb-sqlite-%{realversion}
./configure --prefix=%{i} --with-libodb=../libodb-%{realversion}
make %{makeprocesses} install
%install
touch files
