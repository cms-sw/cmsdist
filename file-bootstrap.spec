### RPM external file-bootstrap 5.13
## INITENV SET MAGIC %{i}/share/misc/magic.mgc

Source: ftp://ftp.fu-berlin.de/unix/tools/file/file-%{realversion}.tar.gz

%define keep_archives true
%define drop_files %{i}/share/man

%build
./configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
            --enable-static --disable-shared CFLAGS="-fPIC"
make %{makeprocesses}
