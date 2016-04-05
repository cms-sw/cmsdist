### RPM external dmtcp 2.0-2212

%define pkg_version %(echo "%{realversion}" | cut -d- -f 1)
%define pkg_revision %(echo "%{realversion}" | cut -d- -f 2)

Source: svn://svn.code.sf.net/p/dmtcp/code/trunk?scheme=svn&revision=%{pkg_revision}&module=%{n}&output=/%{n}.tar.gz

%define drop_files %{i}/share

%prep
%setup -n %{n}

%build
./configure \
  --prefix=%{i} \
  --disable-test-suite \
  --disable-dependency-tracking

make %{makeprocesses}

%install

make install
