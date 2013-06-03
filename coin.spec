### RPM external coin 3.1.0
# Source: ftp://ftp.coin3d.org/pub/coin/src/snapshots/Coin-%realversion.tar.gz
# Source: cvs://:pserver:cvs@cvs.coin3d.org:2401/export/cvsroot?passwd=Ah<Z&tag=-D%{v}&module=Coin&output=/Coin-%realversion.tar.gz
Source: http://ftp.coin3d.org/coin/src/all/Coin-%realversion.tar.gz
Patch0: coin-3.0.0-remove-semicolumns

%define openinventor_version		coin
## INITENV SET OPENINVENTOR_VERSION	%openinventor_version

%prep
%setup -n Coin-%realversion
%patch0 -p1

%build
cfgflags=; 
case %cmsos in
  slc*_amd64)
    cfgflags="-x-libraries=/usr/X11R6/lib64";;
  slc*_ia32)
    cfgflags="-x-libraries=/usr/X11R6/lib";;
  osx*)
    cfgflags="-without-framework --without-x";;
esac
./configure --prefix=%i $cfgflags --disable-libtool-lock --disable-dependency-tracking
make %makeprocesses

%install
make install

%post
%{relocateConfig}bin/coin-config
%{relocateConfig}lib/libCoin.la
