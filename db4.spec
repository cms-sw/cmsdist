### RPM external db4 4.4.20-CMS3
Source: http://downloads.sleepycat.com/db-%{realversion}.tar.gz

%prep
%setup -n db-%{realversion}
%build
mkdir obj
cd obj
../dist/configure --prefix=%{i} --disable-java --disable-tcl
make %makeprocesses
%install
cd obj
make install
#
