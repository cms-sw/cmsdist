### RPM external swig 3.0.10
## INITENV SET SWIG_HOME %{i}
## INITENV SET SWIG_LIB %{i}/share/swig/%{realversion}

Source: http://prdownloads.sourceforge.net/swig/swig-%{realversion}.tar.gz

%prep
%setup -n swig-%{realversion}

%build
./configure \
  --prefix=%{i} \
  --without-pcre

make %{makeprocesses}

%define strip_files %{i}/bin/{swig,ccache-swig}
# bla bla
