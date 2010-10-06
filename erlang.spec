### RPM external erlang R12B_5
%define downloadv %(echo %realversion | tr _ -)
Source: http://erlang.org/download/otp_src_%{downloadv}.tar.gz
Requires: openssl

# 32-bit
Provides: libc.so.6(GLIBC_PRIVATE)
# 64-bit
Provides: libc.so.6(GLIBC_PRIVATE)(64bit)

%prep
%setup -n otp_src_%{downloadv}

%build
./configure --prefix=%i
make

%install
make install

export ERLANG_INSTALL_DIR=%i
cat %i/lib/erlang/bin/erl | sed "s,$ERLANG_INSTALL_DIR,\$ERLANG_ROOT,g" > %i/lib/erlang/bin/erl.new
mv %i/lib/erlang/bin/erl.new %i/lib/erlang/bin/erl
chmod a+x %i/lib/erlang/bin/erl

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

# setup approripate links and made post install procedure
. $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
rm -f $ERLANG_ROOT/bin/*
rm -f $ERLANG_ROOT/lib/erlang/bin/epmd
ln -s $ERLANG_ROOT/lib/erlang/erts-5.6.5/bin/epmd $ERLANG_ROOT/lib/erlang/bin/epmd
for pkg in dialyzer epmd erl erlc escript run_erl to_erl typer
do
    ln -s $ERLANG_ROOT/lib/erlang/bin/$pkg $ERLANG_ROOT/bin/$pkg
done

