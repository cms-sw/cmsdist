### RPM external xz 5.2.2

%define tag c430948daefd58f01ac444af2aeb9850c191fa1d
%define branch cms/v%{realversion}
%define github_user cms-externals
Source0: git+https://github.com/%github_user/xz.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh
./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static --disable-nls --disable-rpath --disable-dependency-tracking --disable-doc
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
# bla bla
