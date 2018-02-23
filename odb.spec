### RPM external odb 2.4.0
Source0: http://www.codesynthesis.com/download/odb/2.4/odb-2.4.0.tar.gz
Source1: https://www.codesynthesis.com/download/libcutl/1.10/libcutl-1.10.0.tar.gz
Source2: http://www.codesynthesis.com/download/odb/2.4/libodb-sqlite-2.4.0.tar.gz
Source3: http://www.codesynthesis.com/download/odb/2.4/libodb-2.4.0.tar.gz

Requires: sqlite

%prep
%setup -T -D -b 0 -n odb-2.4.0
%setup -T -D -b 1 -n libcutl-1.10.0
%setup -T -D -b 2 -n libodb-sqlite-2.4.0
%setup -T -D -b 3 -n libodb-2.4.0

%build
export CC=/opt/rh/devtoolset-4/root/usr/bin/gcc
export CXX=/opt/rh/devtoolset-4/root/usr/bin/g++
cd ../libcutl-1.10.0
./configure --prefix=%{i}
make %{makeprocesses} install
cd ../%{n}-%{realversion}
./configure --prefix=%{i} --with-libcutl=../libcutl-1.10.0
make %{makeprocesses} install
cd ../libodb-2.4.0
./configure --prefix=%{i}
make %{makeprocesses} install
cd ../libodb-sqlite-2.4.0
./configure --prefix=%{i} --with-libodb=../libodb-2.4.0
make %{makeprocesses} install
%install
touch files
