### RPM external bazel 0.4.5

Source: https://github.com/bazelbuild/bazel/releases/download/0.4.5/bazel-0.4.5-dist.zip
BuildRequires: java-env
Patch1: bazel-0.4.5-java-vm
%prep

%define __unzip unzip -d bazel-%{realversion}

%setup -q -n bazel-%{realversion}
%patch1 -p1

%build
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.


