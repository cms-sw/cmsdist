### RPM external binutils 2.17.50
%define realVersion %(echo %v | cut -d- -f1)
Source: ftp://sourceware.org/pub/binutils/snapshots/%n-%realVersion.tar.bz2
%define cpu %(echo %cmsplatf | cut -d_ -f2)

%prep

%setup  -n %{n}-%{realVersion}

%build

./configure --prefix=%i 

make %makeprocesses 

%install
make install

%post


