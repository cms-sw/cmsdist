### RPM external file 5.04
Source: ftp://ftp.fu-berlin.de/unix/tools/file/file-5.04.tar.gz

%build
./configure --prefix %i --enable-static --disable-shared
make %makeprocesses
