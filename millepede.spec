### RPM external millepede V04-00-02
Source: svn://svnsrv.desy.de/public/MillepedeII/tags/%{realversion}/?scheme=http&module=%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: zlib

%prep
%setup -n %{realversion}

%build
make %{makeprocesses} \
  ZLIB_INCLUDES_DIR="${ZLIB_ROOT}/include" \
  ZLIB_LIBS_DIR="${ZLIB_ROOT}/lib"

%install
make install PREFIX=%{i}
