Summary:	I/O fencing system
Summary(pl):	System barier I/O
Name:		fence
Version:	1.02.00
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	131c34c8b66d8d7d74384839ed4091d0
URL:		http://sources.redhat.com/cluster/fence/
BuildRequires:	cman-devel
BuildRequires:	perl-base
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The Fence system does I/O fencing of cluster members. Any member may
join the default fence domain after which it will be fenced if it
fails without leaving the fence domain cleanly. The lock_dlm GFS lock
module will not permit GFS to be mounted until the node has joined a
fence domain.

The fence daemon, fenced, is usually started by running "fence_tool
join". Once started, fenced joins the default fence domain and the
node is subject to being fenced if it fails. A collection of fence
agents are used by fenced to interface with hardware devices (usually
to shut off its path to shared storage or cycle its power source.)

%description -l pl
System Fence odpowiada za bariery I/O dla cz³onków klastra. Ka¿dy z
cz³onków mo¿e do³±czyæ do domy¶lnej domeny barier, po czym bêdzie
odgrodzony je¶li zawiedzie nie opuszczaj±c czysto domeny barier. Modu³
blokuj±cy GFS-a lock_dlm nie pozwoli na podmontowanie GFS-a dopóki
wêze³ nie do³±czy do domeny barier.

Demon fence, fenced, jest zwykle uruchamiany przez fence_tool join. Po
uruchomieniu fenced do³±cza do domy¶lnej domeny barier, a wêze³ jest
przedmiotem odgrodzenia je¶li zawiedzie. fenced wykorzystuje zbiór
agentów fence do komunikacji z urz±dzeniami sprzêtowymi (zwykle do
odcinania drogi do dzielonej pamiêci lub wy³±czania i w³±czania
zasilania).

%prep
%setup -q -n cluster-%{version}
cd %{name}

%{__perl} -pi -e 's/-Wall/%{rpmcflags} -Wall/' make/defines.mk.input
%{__perl} -pi -e 's/-O2 //' fence_node/Makefile fence_tool/Makefile fenced/Makefile

%build
cd %{name}
./configure \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
#%attr(754,root,root) /etc/rc.d/init.d/fenced
%{_mandir}/man?/*
