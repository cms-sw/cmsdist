### RPM external db6 6.0.30
Source: http://davidlt.web.cern.ch/davidlt/sources/db-%{realversion}.tar.gz
%define drop_files %{i}/docs
%define strip_files %{i}/lib

%prep
%setup -n db-%{realversion}

%build
mkdir ./obj
cd ./obj
../dist/configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
                  --disable-java --disable-tcl --disable-static
make %{makeprocesses}

%install
cd ./obj
make install
