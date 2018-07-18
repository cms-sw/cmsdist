### RPM external odb 2.4.0
Source0: http://www.codesynthesis.com/download/odb/2.4/odb-2.4.0.tar.gz
Source1: https://www.codesynthesis.com/download/libcutl/1.10/libcutl-1.10.0.tar.gz
Source2: http://www.codesynthesis.com/download/odb/2.4/libodb-sqlite-2.4.0.tar.gz
Source3: http://www.codesynthesis.com/download/odb/2.4/libodb-2.4.0.tar.gz
Patch0: odb_gcc6
Patch1: odb_gcc6_fix

Requires: sqlite

%prep
%setup -T -D -b 0 -n odb-2.4.0
%patch0 -p1
%patch1 -p1
%setup -T -D -b 1 -n libcutl-1.10.0
%setup -T -D -b 2 -n libodb-sqlite-2.4.0
%setup -T -D -b 3 -n libodb-2.4.0

%build
export CC=gcc
export CXX=g++
export CXXFLAGS=-std=c++11

cd ../libcutl-1.10.0
./configure --prefix=%{i}
make %{makeprocesses} install LDFLAGS="-Wl,-L%{i}/lib"
cd ../%{n}-%{realversion}
./configure --prefix=%{i} --with-libcutl=../libcutl-1.10.0 
make %{makeprocesses} install LDFLAGS="-Wl,-L%{i}/lib"
cd ../libodb-2.4.0
./configure --prefix=%{i}
make %{makeprocesses} install LDFLAGS="-Wl,-L%{i}/lib"
cd ../libodb-sqlite-2.4.0
./configure --prefix=%{i} --with-libodb=../libodb-2.4.0
make %{makeprocesses} install LDFLAGS="-Wl,-L%{i}/lib"
%install
touch files
