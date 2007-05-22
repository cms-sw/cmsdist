### RPM external sqlite 3.3.5-XXXX
Source: http://www.sqlite.org/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i --disable-tcl
make %makeprocesses
