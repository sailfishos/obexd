Name:       obexd
Summary:    D-Bus service for Obex Client access
Version:    0.42
Release:    1
Group:      System/Daemons
License:    GPLv2+
URL:        http://www.bluez.org/
Source0:    http://www.kernel.org/pub/linux/bluetooth/obexd-%{version}.tar.gz
Source1:    obexd-wrapper
Source2:    obexd.conf
BuildRequires:  automake, libtool
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(bluez) < 5.0
BuildRequires:  pkgconfig(libical)
Requires:       obex-capability
Requires:       bluez-libs
Conflicts:      bluez5-libs

%description
obexd contains obex-client, a D-Bus service to allow sending files
using the Obex Push protocol, common on mobile phones and
other Bluetooth-equipped devices.


%package server
Summary:    a server for incoming OBEX connections
Group:      System/Daemons
Requires:   %{name} = %{version}-%{release}
Requires:   bluez-libs
Conflicts:  bluez5-libs

%description server
obexd-server contains a server for receiving OBEX operations.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q -n %{name}-%{version}/obexd

%build
./bootstrap
sed -i 's/ovi_suite/pc_suite/' plugins/usb.c
%reconfigure --disable-static \
    --enable-usb --enable-pcsuite \
    --enable-jolla-blacklist \
    --with-phonebook=sailfish \
    --with-contentfilter=helperapp

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
install -m755 -D %{SOURCE1} %{buildroot}/%{_libexecdir}/obexd-wrapper
install -m644 -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/obexd.conf
sed -i 's,/usr/libexec/obexd,/usr/libexec/obexd-wrapper,' \
    %{buildroot}/%{_datadir}/dbus-1/services/obexd.service
mkdir -p %{buildroot}/%{_sysconfdir}/obexd/{plugins,noplugins}


%files
%defattr(-,root,root,-)
%doc README doc/client-api.txt COPYING AUTHORS
%{_libexecdir}/obex-client
%{_datadir}/dbus-1/services/obex-client.service


%files server
%defattr(-,root,root,-)
%config %{_sysconfdir}/obexd.conf
%dir %{_sysconfdir}/obexd/
%dir %{_sysconfdir}/obexd/plugins/
%dir %{_sysconfdir}/obexd/noplugins/
%attr(2755,root,privileged) %{_libexecdir}/obexd
%{_libexecdir}/obexd-wrapper
%{_datadir}/dbus-1/services/obexd.service


%files devel
%defattr(-,root,root,-)
%doc  doc/client-api.txt
