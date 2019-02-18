### RPM external tensorflow 1.13.0rc2
Provides: libtensorflow_cc.so(tensorflow)(64bit)
Source: none

BuildRequires: tensorflow-sources

%prep

%build

%install
tar xfz ${TENSORFLOW_SOURCES_ROOT}/libtensorflow.tar.gz -C %{i}
tar xfz ${TENSORFLOW_SOURCES_ROOT}/libtensorflow_cc.tar.gz -C %{i}

