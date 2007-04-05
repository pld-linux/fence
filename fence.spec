Summary:	I/O fencing system
Summary(pl.UTF-8):	System barier I/O
Name:		fence
Version:	2.00.00
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	2ef3f4ba9d3c87b50adfc9b406171085
Patch0:		%{name}-antistatic.patch
URL:		http://sources.redhat.com/cluster/fence/
BuildRequires:	cman-devel
BuildRequires:	ccs-devel
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

%description -l pl.UTF-8
System Fence odpowiada za bariery I/O dla członków klastra. Każdy z
członków może dołączyć do domyślnej domeny barier, po czym będzie
odgrodzony jeśli zawiedzie nie opuszczając czysto domeny barier. Moduł
blokujący GFS-a lock_dlm nie pozwoli na podmontowanie GFS-a dopóki
węzeł nie dołączy do domeny barier.

Demon fence, fenced, jest zwykle uruchamiany przez fence_tool join. Po
uruchomieniu fenced dołącza do domyślnej domeny barier, a węzeł jest
przedmiotem odgrodzenia jeśli zawiedzie. fenced wykorzystuje zbiór
agentów fence do komunikacji z urządzeniami sprzętowymi (zwykle do
odcinania drogi do dzielonej pamięci lub wyłączania i włączania
zasilania).

%prep
%setup -q -n cluster-%{version}
%patch0 -p1
cd %{name}

%{__perl} -pi -e 's/-Wall/%{rpmcflags} -Wall/' make/defines.mk.input
%{__perl} -pi -e 's/-O2 //' fence_node/Makefile fence_tool/Makefile fenced/Makefile
%{__perl} -pi -e 's@${top_srcdir}/../group/lib/libgroup.a@@'  fence/fence_tool/Makefile

%build
# libgroup.a is not packaged in group.spec, we must build it here
%{__make} -C group/lib
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
