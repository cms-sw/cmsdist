### RPM external file 5.13
## INITENV +PATH PATH %{i}/bin
## INITENV SET MAGIC %{i}/share/misc/magic.mgc

Source: ftp://ftp.fu-berlin.de/unix/tools/%{n}/%{n}-%{realversion}.tar.gz

%define keep_archives true
%define drop_files %{i}/share/man

%build
./configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
            --enable-static --disable-shared CFLAGS="-fPIC"
make %{makeprocesses}
