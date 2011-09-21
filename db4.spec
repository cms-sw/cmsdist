### RPM external db4 4.4.20-CMS19
Source: http://download.oracle.com/berkeley-db/db-%{realversion}.NC.tar.gz

%prep
%setup -n db-%{realversion}.NC
%build
mkdir obj
cd obj
../dist/configure --prefix=%{i} --disable-java --disable-tcl --disable-static
make %makeprocesses
%install
cd obj
make install

%define drop_files %i/docs
%define strip_files %i/lib
