### RPM external byacc 1.9.20130304
%define download_version 20130304
Source: ftp://invisible-island.net/%{n}/%{n}-%{download_version}.tgz

%prep
%setup -q -n %{n}-%{download_version}

# Revert default stack size back to 10000
# https://bugzilla.redhat.com/show_bug.cgi?id=743343
find . -type f -name \*.c -print0 |
  xargs -0 sed -ibak 's/YYSTACKSIZE 500/YYSTACKSIZE 10000/g'

%build
./configure --disable-dependency-tracking --prefix=%{i}
make %{makeprocesses}

%install
make install

%define drop_files %{i}/share
# bla bla
