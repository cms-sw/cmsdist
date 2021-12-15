### RPM external libffi 3.4.2
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

%define tag v%{realversion}
%define github_user libffi
%define github_repo libffi
%define branch master

Source: git+https://github.com/%{github_user}/%{github_repo}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz 
BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}
autoreconf -fiv

%build
./configure \
  --prefix=%{i} \
  --enable-portable-binary \
  --disable-dependency-tracking \
  --disable-static --disable-docs

make %{makeprocesses}

%install
make %{makeprocesses} install

rm -rf %{i}/lib
rm -rf %{i}/lib64/*.la

%define drop_files %{i}/share
