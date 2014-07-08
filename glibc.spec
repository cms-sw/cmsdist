### RPM external glibc 2.12.2
## NOCOMPILER

Source0: http://ftp.gnu.org/gnu/glibc/%{n}-%{realversion}.tar.gz

Patch0: glibc-2.12.2-fix-dl-tls

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build

rm -rf ../glibc-build
mkdir ../glibc-build
cd ../glibc-build
../glibc-%{realversion}/configure \
  --prefix=/ \
  --without-selinux \
  --disable-sanity-checks

make %{makeprocesses}

%install
cd ../glibc-build
make install install_root=%{i}

# Remove everything except dynamic loader. All changes are contained
# within the loader.
find %{i} ! -type d | grep -Z -v 'ld-%{realversion}' | xargs rm -f
find %{i} -empty -type d -delete
