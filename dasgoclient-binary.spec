### RPM cms dasgoclient-binary v02.02.03
Source0: git+https://github.com/dmwm/dasgoclient?obj=master/%{realversion}&export=dasgoclient&output=/dasgoclient.tar.gz
Source1: git+https://github.com/dmwm/cmsauth?obj=master/e9fca92e3335252a5f71d8e6d09c64012f7d3c0c&export=github.com/dmwm/cmsauth&output=/cmsauth.tar.gz
Source2: git+https://github.com/vkuznet/x509proxy?obj=master/c93f6cae85114060b3b65861ea8436e4e14c54a6&export=github.com/vkuznet/x509proxy&output=/x509proxy.tar.gz
Source3: git+https://github.com/buger/jsonparser?obj=master/6bd16707875b997f7a60327f888a28a3d28cf8c2&export=github.com/buger/jsonparser&output=/jsonparser.tar.gz
Source4: git+https://github.com/go-mgo/mgo?obj=v2/3f83fa5005286a7fe593b055f0d7771a7dce4655&export=gopkg.in/mgo.v2&output=/mgo.v2.tar.gz
Source5: git+https://github.com/pkg/profile?obj=master/3a8809bd8a80f8ecfe4ee1b34b3f37194968617c&export=github.com/pkg/profile&output=/profile.tar.gz
Source6: git+https://github.com/dmwm/das2go?obj=master/128b50f7262ca887f719d61393f7f5763d3d225a&export=github.com/dmwm/das2go&output=/das2go.tar.gz
Source7: git+https://github.com/sirupsen/logrus?obj=master/a3f95b5c423586578a4e099b11a46c2479628cac&export=github.com/sirupsen/logrus&output=/logrus.tar.gz
%prep

%setup -n dasgoclient
mkdir -p gopath/src
cd gopath/src
tar -xzf %{_sourcedir}/cmsauth.tar.gz
tar -xzf %{_sourcedir}/x509proxy.tar.gz
tar -xzf %{_sourcedir}/x509proxy.tar.gz
tar -xzf %{_sourcedir}/jsonparser.tar.gz
tar -xzf %{_sourcedir}/mgo.v2.tar.gz
tar -xzf %{_sourcedir}/profile.tar.gz
tar -xzf %{_sourcedir}/das2go.tar.gz
tar -xzf %{_sourcedir}/logrus.tar.gz

%build
export GOPATH=`pwd`/gopath
sed -i -e "s,TAG :=,#TAG :=,g" -e "s,\$(TAG),%{realversion},g" Makefile
make build_all

%install
mkdir -p %{i}/bin
cp dasgoclient_* %{i}/bin

