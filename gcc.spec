### RPM external gcc 3.2.3
## BUILDIF [ $(uname) != Darwin ]
Source: ftp://ftp.fu-berlin.de/unix/gnu/%n/%n-%v/%n-%v.tar.gz

%build
# FIXME: --enable-__cxa_atexit can't be used with gcc 3.2.3 on RH 7.3,
# enabling it causes qt's uic to die with segmentation violation half
# way down the build of qt (projecsettings.ui or something like that;
# not the first or only call to uic).  Disabling the flag removes the
# issue, so clearly the option does not work correctly on this
# platform combination.
mkdir -p obj
cd obj
../configure --prefix=%i --enable-languages=c,c++,f77 \
    --enable-shared # --enable-__cxa_atexit
make bootstrap

%install
cd obj && make install
ln -s gcc %i/bin/cc
