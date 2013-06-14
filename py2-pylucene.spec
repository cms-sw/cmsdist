### RPM external py2-pylucene 2.0.0-3

%define ddn PyLucene 

Source: http://downloads.osafoundation.org/%{ddn}/src/%{ddn}-src-%{v}.tar.gz
Requires: gcj db4 python


%prep
%setup -n %{ddn}-src-%v
%build
make PREFIX=%i GCJ_HOME=$GCJ_HOME PREFIX_PYTHON=$PYTHON_ROOT PREFIX_DB=$DB4_ROOT 
