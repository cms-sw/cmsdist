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
rm -rf %{i}/docs
rm -f %i/lib/*.{l,}a
find %i/lib -type f -perm -a+x -exec strip {} \;
