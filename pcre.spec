### RPM external pcre 7.9
Source: http://downloads.sourceforge.net/%n/%n-%{realversion}.tar.bz2
Requires: bz2lib

%prep
%setup -n %n-%{realversion}
%build
CPPFLAGS="-I${BZ2LIB_ROOT}/include"
LDFLAGS="-L${BZ2LIB_ROOT}/lib"
./configure --enable-unicode-properties --enable-pcregrep-libz --enable-pcregrep-libbz2 --prefix=%i \
  CPPFLAGS="${CPPFLAGS}" LDFLAGS="${LDFLAGS}"
make %{makeprocesses}

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.pcre.org"></info>
<lib name=pcre>
<Client>
 <Environment name=PCRE_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$PCRE_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$PCRE_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries.
%define strip_files %i/lib

# Do not need to keep the archives.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
%define drop_files %i/share

%post
%{relocateConfig}bin/pcre-config
%{relocateConfig}etc/scram.d/%n

# The relocation is also needed because of dependencies
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
