### RPM external gdb 6.7.1-CMS19
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.bz2

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i}
make %makeprocesses

