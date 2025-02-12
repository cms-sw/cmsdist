### RPM external gperftools 2.11
Source: https://github.com/gperftools/gperftools/archive/refs/tags/gperftools-%{realversion}.tar.gz

BuildRequires: autotools

%prep
%setup -n %{n}-%{n}-%{realversion}

%build
./autogen.sh
./configure \
  --prefix=%{i} \
  --disable-dependency-tracking \
  --enable-sized-delete \
  --enable-dynamic-sized-delete-support \
  --disable-libunwind \
  --disable-debugalloc 

make %{makeprocesses}

%install

make install

rm -rf %{i}/share/{doc,man}
