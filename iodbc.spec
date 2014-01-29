### RPM external iodbc 3.52.4
%define downloadn libiodbc
Source: http://www.iodbc.org/downloads/iODBC/%downloadn-%v.tar.gz
%prep
%setup -n %downloadn-%v
%build
./configure --prefix=%{i} --disable-gui
make %makeprocesses
