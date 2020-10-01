### RPM cms wmarchive v00.08.63

%define pkg WMArchive
Source0: git://github.com/dmwm/WMArchive?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: go

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -c

%build
cd WMArchive

# build go publisher tool
mkdir -p gopath
export GOPATH=$PWD/gopath
go get github.com/nats-io/go-nats-examples/tools/nats-pub
mkdir -p %i/bin
cp $GOPATH/bin/nats-pub %i/bin

# build WMArchvie Go server
go get github.com/go-stomp/stomp
go get github.com/google/uuid
go get github.com/lestrrat-go/file-rotatelogs
go get github.com/nats-io/nats.go
cd src/go
make
cp wmarchive %i/bin

%install
cd WMArchive

# install static files
mkdir -p %i/data/storage
cp -r src/{js,css,images,templates,maps,sass} %i/data

# generate current schema
mkdir -p %i/data/schemas

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
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

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc
