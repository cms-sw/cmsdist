### RPM cms frontend 1.2
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rFRONTEND_CONF_1_2&output=/config.tar.gz
Source1: %cvsserver&module=COMP/WEBTOOLS/WelcomePages&export=htdocs&tag=-rFRONTEND_HTDOCS_1_0&output=/htdocs.tar.gz
Requires: apache2-conf
Obsoletes: cms+frontend+1.1e-cmp
Obsoletes: cms+frontend+1.1d-cmp
Obsoletes: cms+frontend+1.1c-cmp
Obsoletes: cms+frontend+1.1b-cmp
Obsoletes: cms+frontend+1.1-cmp
Obsoletes: cms+frontend+1.0-cmp11
Obsoletes: cms+frontend+1.0-cmp10
Obsoletes: cms+frontend+1.0-cmp9
Obsoletes: cms+frontend+1.0-cmp8
Obsoletes: cms+frontend+1.0-cmp7
Obsoletes: cms+frontend+1.0-cmp6
Obsoletes: cms+frontend+1.0-cmp5
Obsoletes: cms+frontend+1.0-cmp4
Obsoletes: cms+frontend+1.0-cmp3
Obsoletes: cms+frontend+1.0-cmp2
Obsoletes: cms+frontend+1.0-cmp

%prep
%setup -T -b 0 -n conf
%setup -D -T -b 1 -n htdocs

%build
%install
# Make directory for various resources of this package.
rm -fr %instroot/htdocs/*
rm -fr %instroot/apache2/*rewrites.d
rm -f %instroot/apache2/apps.d/*frontend.conf

mkdir -p %instroot/apache2/apps.d
mkdir -p %instroot/apache2/rewrites.d
mkdir -p %instroot/apache2/ssl_rewrites.d
mkdir -p %instroot/apache2/htdocs

# Replace template variables in configuration files with actual paths.
perl -p -i -e "s|\@SERVER_ROOT\@|%instroot/apache2|g;s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;" %_builddir/conf/*/*.conf

# Copy files to the server setup directory.
cp -p %_builddir/conf/apps.d/*frontend.conf %instroot/apache2/apps.d
cp -p %_builddir/conf/rewrites.d/*.conf %instroot/apache2/rewrites.d
cp -p %_builddir/conf/ssl_rewrites.d/*.conf %instroot/apache2/ssl_rewrites.d
cp -rp %_builddir/htdocs/* %instroot/apache2/htdocs

%post
# Relocate files.
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/apache2/*.d/*.conf

# Deter attempts to modify installed files locally.
chmod a-w $RPM_INSTALL_PREFIX/apache2/*.d/*.conf

%files
%i/
%dir %instroot/apache2/rewrites.d
%dir %instroot/apache2/ssl_rewrites.d
%attr(444,-,-) %instroot/apache2/apps.d/*frontend.conf
%attr(444,-,-) %instroot/apache2/rewrites.d/*.conf
%attr(444,-,-) %instroot/apache2/ssl_rewrites.d/*.conf
%instroot/apache2/htdocs/*
