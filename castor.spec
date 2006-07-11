### RPM external castor 2.1.0-0
Source: none 

%prep
%build
%install
mkdir -p %i/lib %i/bin %i/man/man1 %i/include/shift
cp /usr/include/shift.h %i/include/shift.h
cp /usr/include/shift/* %i/include/shift/
cp -d /usr/lib/libshift.* %i/lib
cp /usr/bin/rfcat %i/bin
cp /usr/bin/rfchmod %i/bin
cp /usr/bin/rfcp %i/bin
cp /usr/bin/rfdir %i/bin
cp /usr/bin/rfmkdir %i/bin
cp /usr/bin/rfrename %i/bin
cp /usr/bin/rfrm %i/bin
cp /usr/bin/rfstat %i/bin
cp /usr/share/man/man1/rfcat.1castor %i/man/man1
cp /usr/share/man/man1/rfchmod.1castor %i/man/man1
cp /usr/share/man/man1/rfcp.1castor %i/man/man1
cp /usr/share/man/man1/rfdir.1castor %i/man/man1
cp /usr/share/man/man1/rfmkdir.1castor %i/man/man1
cp /usr/share/man/man1/rfrename.1castor %i/man/man1
cp /usr/share/man/man1/rfrm.1castor %i/man/man1
