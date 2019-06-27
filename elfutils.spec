### RPM external elfutils 0.131
#TODO: put everything in rpm.spec???
Source: ftp://sources.redhat.com/pub/systemtap/%{n}/%{n}-%{realversion}.tar.gz
%prep
%setup -n %n-%realversion
perl -p -i -e "s/-Wextra//g;s/-Werror//" `find . -name \*.in`
%build
%if "%(echo %cmsos | sed -e 's/osx.*/osx/')" != "osx"
./configure --prefix=%i
cd libelf
make %makeprocesses
%endif
%install
%if "%(echo %cmsos | sed -e 's/osx.*/osx/')" != "osx"
cd libelf
make install
rm -rf %i/bin
%endif
# bla bla
