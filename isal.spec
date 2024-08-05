### RPM external isal 2.30.0

%define strip_files %i/lib
%define tag %{realversion}
%define branch master
%define github_user xrootd
Source: https://github.com/intel/isa-l/archive/refs/tags/v%{realversion}.tar.gz

%ifarch x86_64
BuildRequires: nasm
%endif
BuildRequires: autotools

%prep
%setup -n isa-l-%{realversion}

%build
./autogen.sh
./configure --prefix=%{i} --with-pic

make %{makeprocesses}

%install
make install
