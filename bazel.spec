### RPM external bazel 7.7.0
## INCLUDE cpp-standard

%ifarch x86_64
Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-linux-x86_64
%ifarch aarch64
Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-darwin-arm64
%endif

BuildRequires: java-env
%prep
%setup -T -c -n bazel-%{realversion}
cp %{_sourcedir}/bazel-%{realversion}-linux-x86_64 bazel
%build
# nothing to build prebuilt binary
%install
mkdir -p %{i}/bin
install -m 0755 bazel %{i}/bin/bazel
