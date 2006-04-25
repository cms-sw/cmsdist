### RPM external db4 4.4.20
Source: http://downloads.sleepycat.com/db-%{v}.tar.gz

%prep
%setup -n db-%{v}
%build
mkdir obj
cd obj
../dist/configure --prefix=%{i} --disable-java --disable-tcl
make %makeprocesses
%install
cd obj
make install
