### RPM external cppunit 1.15.x
%define tag     2b72f2b3ef94452ae649fc6a44bec049f1acb173
%define branch master
%define github_user git/libreoffice
Source: git+https://anongit.freedesktop.org/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: gmake autotools

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
./autogen.sh
./configure --prefix=%i --disable-static
make %makeprocesses

%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
# Remove unneded files
rm -rf %i/lib/*.{l,}a
# Read documentation online
%define drop_files %i/share

