### RPM external elfutils 0.128-CMS3
#TODO: put everything in rpm.spec???
Source: ftp://sources.redhat.com/pub/systemtap/%{n}/%{n}-%{realversion}.tar.gz
%prep
%setup -n %n-%realversion
%build
./configure --prefix=%i
cd libelf
make %makeprocesses
%install
cd libelf
make install
rm -rf %i/bin
