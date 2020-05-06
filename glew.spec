### RPM external glew 2.1.0
## INITENV SETV GLEW_SOURCE %{source0}
## INITENV SETV GLEW_STRIP_PREFIX %{source_prefix}

%define source0 https://github.com/nigels-com/glew/releases/download/%{n}-%{realversion}/%{n}-%{realversion}.tgz
%define source_prefix %{n}-%{realversion}
Source: %{source0}

BuildRequires: gmake

%prep
%setup -n %{source_prefix}
sed -i -e 's|GLEW_DEST)/lib64|GLEW_DEST)/lib|' ./config/Makefile.linux

%build

make -C auto
make %{makeprocesses}

%install

make install GLEW_DEST=%{i}

