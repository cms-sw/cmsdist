### RPM external elfutils 0.128-CMS3
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) true ;; Darwin:* ) false ;; * ) false ;; esac
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
