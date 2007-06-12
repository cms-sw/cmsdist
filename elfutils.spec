### RPM external elfutils 0.128
#TODO: put everything in rpm.spec???
Source: ftp://sources.redhat.com/pub/systemtap/elfutils/elfutils-0.128.tar.gz

%build
./configure --prefix=%i
make %makeprocesses
%install
make install
rm -rf %i/bin
