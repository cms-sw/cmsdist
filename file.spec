### RPM external file 5.04
## INITENV SET MAGIC %i/share/misc/magic.mgc

Source: ftp://ftp.fu-berlin.de/unix/tools/file/file-5.04.tar.gz

%build
./configure --prefix %i --enable-static --disable-shared CFLAGS=-fPIC
make %makeprocesses
