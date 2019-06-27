### RPM external readline 6.3
Source: ftp://ftp.cwru.edu/pub/bash/%{n}-%{realversion}.tar.gz
%define keep_archives true
%define drop_files %{i}/lib/*.so

#Patch to fix DEL key crashing python/gdb issue: http://pkgs.fedoraproject.org/cgit/rpms/readline.git/plain/readline6.3-upstream-patches1-6.patch
Patch0: readline6.3-upstream-patches1-6

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
./configure --prefix %{i} --build="%{_build}" --host="%{_host}" \
            --disable-shared --enable-static
make %{makeprocesses} CFLAGS="-O2 -fPIC"


%install
make install
# bla bla
