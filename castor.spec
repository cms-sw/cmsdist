### RPM external castor 2.1.0-0
%define downloadv %(echo %v | cut -d- -f1)

Source: http://cern.ch/castor/DIST/CERN/savannah/CASTOR.pkg/%v/castor-%downloadv.tar.gz

%prep
%setup -n castor-%downloadv
%build
mkdir -p %i/bin %i/lib %i/man/man4 %i/man/man3 %i/man/man1 %i/etc/sysconfig
make 
%install
make install EXPORTLIB=/ \
                DESTDIR=%i/ \
                PREFIX= \
                CONFIGDIR=etc \
                FILMANDIR=man/man4 \
                LIBMANDIR=man/man3 \
                MANDIR=man/man1 \
                LIBDIR=lib \
                BINDIR=bin \
                LIB=lib \
                BIN=bin \
                DESTDIRCASTOR=include/shift \
                TOPINCLUDE=include 
