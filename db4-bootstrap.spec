### RPM external db4-bootstrap 4.5.20
Source: http://download.oracle.com/berkeley-db/db-%{realversion}.NC.tar.gz
%define drop_files %i/docs
%define strip_files %i/lib

%prep
%setup -n db-%{realversion}.NC

%build
mkdir obj
cd obj
../dist/configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
                  --disable-java --disable-tcl --disable-static
make %{makeprocesses}

%install
cd obj
make install
