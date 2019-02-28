### RPM cms PHEDEX-webapp 1.5.0pre4
## INITENV +PATH PERL5LIB %i/perl_lib

%define downloadn %(echo %n | cut -f1 -d-)
%define downloadp %(echo %n | cut -f2 -d- | tr '[a-z]' '[A-Z]')
%define downloadt %(echo %realversion | tr '.' '_')
%define setupdir  %{downloadn}-%{downloadp}_%{downloadt}
Source: https://github.com/dmwm/PHEDEX/archive/%{downloadp}_%{downloadt}.tar.gz

%define yuicompressorversion 2.4.6
Source1: http://yui.zenfs.com/releases/yuicompressor/yuicompressor-%{yuicompressorversion}.zip
Requires: protovis yui
#BuildRequires: java-jdk

%prep
%setup -T -b 1 -n yuicompressor-%{yuicompressorversion}
%setup -D -T -b 0 -n %{setupdir}
rm -rf Build Custom Documentation perl_lib README.txt Testbed Utilities
rm -rf Contrib Deployment Migration Schema Toolkit VERSION

%build
export YUICOMPRESSOR_PATH=%_builddir/yuicompressor-%{yuicompressorversion}/build/yuicompressor-%{yuicompressorversion}.jar
cd %_builddir
sh %_builddir/%{setupdir}/PhEDExWeb/ApplicationServer/util/phedex-minify.sh
rm -rf %_builddir/%{setupdir}/PhEDExWeb/{ApplicationServer/{js,css,util},yuicompressor*}
mv %_builddir/%{setupdir}/PhEDExWeb/ApplicationServer/{build/*,}
rmdir %_builddir/%{setupdir}/PhEDExWeb/ApplicationServer/build

%install
mkdir -p %i/etc/{env,profile}.d
tar -cf - * | (cd %i && tar -xf -)
rm -r %i/PhEDExWeb/ApplicationServer/conf
echo 'manifest of installation'
find %i -type f

cp %i/PhEDExWeb/ApplicationServer/html/phedex{,-debug}.html

# Replace the base and loader files with the rollup, and switch everything to minified files.
# Also explicitly turn off combo-serving, for now.
perl -p -i -e 's|phedex-base.js|phedex-base-loader.js|; \
	      s|^.*phedex-loader.js.*||; \
	      s|phedex([a-z,-]+).js|phedex\1-min.js|g;' \
  %i/PhEDExWeb/ApplicationServer/html/phedex.html

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
ln -sf ../profile.d/init.sh %i/etc/env.d/12-webapp.sh
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
