### RPM external gdbm 1.10
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://ftp.gnu.org/gnu/gdbm/gdbm-%realversion.tar.gz

%define thisuser %(id -u)
%define thisgroup %(id -g)

%prep
%setup -n %n-%{realversion}

%build
perl -p -i -e "s|BINOWN = bin|BINOWN = %{thisuser}|g" Makefile.in
perl -p -i -e "s|BINGRP = bin|BINGRP = %{thisgroup}|g" Makefile.in
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --enable-libgdbm-compat --prefix=%{i} --host=x86_64-k1om-linux
     ;;
   * )
     ./configure --enable-libgdbm-compat --prefix=%{i}
     ;;
esac
make %makeprocesses

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Look up documentation online.
%define drop_files %i/{info,man}
