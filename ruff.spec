### RPM external ruff 0.5.6
Source: https://github.com/astral-sh/ruff/releases/download/%{realversion}/ruff-x86_64-unknown-linux-gnu.tar.gz

%prep

%setup -n ruff-x86_64-unknown-linux-gnu
mkdir -p %{i}/bin
cp ruff %{i}/bin

%build
