### RPM external libffi 3.2.1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

Source: ftp://sourceware.org/pub/%{n}/%{n}-%{realversion}.tar.gz

Patch0: libffi-3.2.1-fix-include-path

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
./configure \
  --prefix=%{i} \
  --enable-portable-binary \
  --disable-dependency-tracking \
  --disable-static

make %{makeprocesses}

%install
make %{makeprocesses} install

rm -rf %{i}/lib
rm -rf %{i}/lib64/*.la

%define drop_files %{i}/share
