### RPM external bazel 3.7.1

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-installer-linux-x86_64.sh

BuildRequires: java-env python3

# For some build steps, bazel uses a process-wrapper that is executed in an empty environment.
# Therefore, the wrapper is linked to the system library /lib64/libstdc++.so.6, and complains about
# a missing GLIBCXX_3.4.21 version when (e.g.) used during the compilation of tensorflow python
# modules invoked via swig. This mechanism of bazel is actually only useful in combination with its
# remote compilation features. When disabling the process-wrapper, the local environment is taken
# into account which is the desired behavior for us. For example, see:
#   - https://github.com/bazelbuild/bazel/issues/4137
#   - https://github.com/bazelbuild/bazel/issues/4510
#   - https://github.com/tensorflow/tensorboard/issues/1611

%prep
pwd

%build
ls -l ${_sourcedir}
chmod +x %{_sourcedir}/bazel-%{realversion}-installer-linux-x86_64.sh

%install
%{_sourcedir}/bazel-%{realversion}-installer-linux-x86_64.sh --prefix=$PWD/install
mkdir -p %{i}
cp -rpv install/* %{i}
