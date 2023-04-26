### RPM external rust 1.61.0
%ifarch ppc64le
%define build_arch powerpc64le-unknown-linux-gnu
%else
%define build_arch %{_arch}-unknown-linux-gnu
%endif
%define github_user rust-lang
%define branch master
%define tag %{realversion}
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz
Patch0: rust-libstdc
BuildRequires: python3
Requires: llvm

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
cat << EOF > config.toml
[llvm]
link-shared = true

[build]
docs = false
build = "%{build_arch}"
extended = true

[install]
prefix = "%i"
sysconfdir = "etc"

[rust]
channel = "stable"
rpath = false
codegen-tests = false

[target.%{build_arch}]
llvm-config = "${LLVM_ROOT}/bin/llvm-config"
EOF

mkdir -p %{_tmppath}/cargo_home
export CARGO_HOME=%{_tmppath}/cargo_home
python3 ./x.py build -vv --exclude src/tools/miri  %{makeprocesses}

%install
export CARGO_HOME=%{_tmppath}/cargo_home
export RUSTUP_HOME=%{i}
python3 ./x.py install  -vv --exclude src/tools/miri %{makeprocesses}
chmod 0755 %i/lib//librustc_driver*.so
