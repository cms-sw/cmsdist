### RPM external rootjs 5.1.0
Source: https://github.com/root-project/jsroot/releases/download/%realversion/JsRoot510.tar.gz

%prep
%setup -c -n rootjs-%realversion
%build
%install
cp -rp * %i
%define drop_files %i/{docs,examples}
