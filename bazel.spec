### RPM external bazel 6.1.0
## INCLUDE cpp-standard

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-dist.zip

BuildRequires: java-env python3 python-python3

# For some build steps, bazel uses a process-wrapper that is executed in an empty environment.
# Therefore, the wrapper is linked to the system library /lib64/libstdc++.so.6, and complains about
# a missing GLIBCXX_3.4.21 version when (e.g.) used during the compilation of tensorflow python
# modules invoked via swig. This mechanism of bazel is actually only useful in combination with its
# remote compilation features. When disabling the process-wrapper, the local environment is taken
# into account which is the desired behavior for us. For example, see:
#   - https://github.com/bazelbuild/bazel/issues/4137
#   - https://github.com/bazelbuild/bazel/issues/4510
#   - https://github.com/tensorflow/tensorboard/issues/1611

# configuration issue
# https://github.com/bazelbuild/bazel/issues/9392
Patch0: bazel-3.7.0-patches
Patch1: bazel-absl

%prep
%setup -q -c -n bazel-%{realversion}

%patch0 -p1
%patch1 -p1

%build

export EXTRA_BAZEL_ARGS="--define=ABSOLUTE_JAVABASE=${JAVA_HOME} --jobs %{compiling_processes}"
export BAZEL_CXXOPTS="-Wno-error=deprecated:-std=c++%{cms_cxx_standard}"
${JAVA_HOME}/bin/java -version 2>&1 | grep -E -i 'openjdk version "[1-9]'
if [ $(${JAVA_HOME}/bin/java -version 2>&1 | grep -E -i 'openjdk version "[1-9]' | sed -E 's|.* "([0-9]+)[.].*|\1|') -ge 17 ] ; then
  export JNI_FLAGS="--add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED"
fi
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.
