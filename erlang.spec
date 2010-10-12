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

# Fix annoying problem with symbolic links
ln -sf ../erts-5.6.5/bin/epmd %i/lib/erlang/bin
ln -sf ../lib/erlang/bin/{dialyzer,epmd,erl,erlc,escript,run_erl,to_erl,typer} %i/bin

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
%{relocateConfig}lib/erlang/bin/{erl,start}
%{relocateConfig}lib/erlang/erts-5.6.5/bin/{erl,start}
