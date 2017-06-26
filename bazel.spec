### RPM external bazel 0.4.5

Source: https://github.com/bazelbuild/bazel/releases/download/0.4.5/bazel-0.4.5-dist.zip

%prep

%define __unzip unzip -d bazel-%{realversion}

%setup -q -n bazel-%{realversion}

%build
bash ./compile.sh

%install
mkdir %{i}/bin
ls
cp output/bazel %{i}/bin/.


