### RPM external elfutils 0.128-wt1
#TODO: put everything in rpm.spec???
Source: ftp://sources.redhat.com/pub/systemtap/%{n}/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%realversion
%build
./configure --prefix=%i
make %makeprocesses
%install
make install
rm -rf %i/bin
