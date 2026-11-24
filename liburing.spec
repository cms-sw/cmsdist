### RPM external liburing 2.15
Source: https://github.com/axboe/%{n}/archive/refs/tags/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{n}-%{realversion}

# configure resolves the paths with realpath
mkdir -p %{i}
./configure \
  --prefix=%{i} \
  --libdir=%{i}/lib \
  --libdevdir=%{i}/lib \
  --includedir=%{i}/include \
  --mandir=%{i}/share/man

%build
make %{makeprocesses} -C src

%install
make %{makeprocesses} -C src install prefix=%{i} libdir=%{i}/lib libdevdir=%{i}/lib includedir=%{i}/include

# remove the static libraries
rm -f %{i}/lib/*.a

%post
