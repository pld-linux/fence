Summary:	I/O fencing system
Summary(pl):	System barier I/O
Name:		fence
%define	snap	20040625
Version:	0.0.0.%{snap}.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	%{name}.tar.gz
# Source0-md5:	f3f40096cf957c6825ae76cac153d698
URL:		http://sources.redhat.com/cluster/
BuildRequires:	awk
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
System Fence odpowiada za bariery I/O dla cz³onków klastra. K±¿dy z
cz³oników mo¿e do³±czyæ do domy¶lnej domeny barier, po czym bêdzie
odgrodzony je¶li zawiedzie nie opuszczaj±c czysto domeny barier.
Modu³ blokuj±cy GFS-a lock_dlm nie pozwoli na podmontowanie GFS-a
dopóki wêze³ nie do³±czy do domeny barier.

Demon fence, fenced, jest zwykle uruchamiany przez fence_tool join. Po
uruchomieniu fenced do³±cza do domy¶lnej domeny barier, a wêze³ jest
przedmiotem odgrodzenia je¶li zawiedzie. fenced wykorzystuje zbiór
agentów fence do komunikacji z urz±dzeniami sprzêtowymi (zwykle do
odcinania drogi do dzielonej pamiêci lub wy³±czania i w³±czania
zasilania).

%prep
%setup -q -n %{name}

%build
./configure \
	--incdir=%{_includedir} \
	--kernel_src=%{_kernelsrcdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
