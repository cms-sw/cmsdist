### RPM external bazel 7.7.0
## INCLUDE cpp-standard

%ifarch x86_64
%define bazelarch linux-x86_64
%endif
%ifarch aarch64
%define bazelarch linux-arm64
%endif

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-%{bazelarch}

BuildRequires: java-env
%prep
%setup -T -c -n bazel-%{realversion}
cp %{_sourcedir}/bazel-%{realversion}-%{bazelarch} bazel
%build
# nothing to build prebuilt binary
%install
mkdir -p %{i}/bin
install -m 0755 bazel %{i}/bin/bazel
