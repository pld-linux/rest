#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
%define		apiver	0.7
#
Summary:	A library for access to RESTful web services
Summary(pl.UTF-8):	Biblioteka dostępu do REST-owych serwisów WWW
Name:		rest
Version:	0.7.90
Release:	1
License:	LGPL v2
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rest/0.7/%{name}-%{version}.tar.xz
# Source0-md5:	639d51e9e9276726db93b1b4c46887f2
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk-doc >= 1.13
BuildRequires:	libsoup-gnome-devel >= 2.26.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.22.0
Requires:	libsoup-gnome >= 2.26.0
Suggests:	ca-certificates
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library was designed to make it easier to access web services
that claim to be "RESTful". A RESTful service should have URLs that
represent remote objects, which methods can then be called on. The
majority of services don't actually adhere to this strict definition.
Instead, their RESTful end point usually has an API that is just
simpler to use compared to other types of APIs they may support
(XML-RPC, for instance). It is this kind of API that this library is
attempting to support.

%description -l pl.UTF-8
Ta biblioteka została zaprojektowana, aby ułatwić dostęp do serwisów
WWW, które uznają się za "REST-owe". Serwis REST-owy powinien mieć
URL-e reprezentujące zdalne obiekty, na których można wywoływać
metody. Większość serwisów nie jest w pełni zgodna z tą definicją, ale
ich REST-owy interfejs zwykle ma API prostsze od innych (np. XML-RPC).
Ten rodzaj API próbuje obsłużyć ta biblioteka.

%package devel
Summary:	Header files for rest library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rest
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.22.0
Requires:	libsoup-devel >= 2.26.0
Requires:	libxml2-devel

%description devel
Header files for rest library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki rest.

%package static
Summary:	Static rest library
Summary(pl.UTF-8):	Statyczna biblioteka rest
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rest library.

%description static -l pl.UTF-8
Statyczna biblioteka rest.

%package apidocs
Summary:	rest API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki rest
Group:		Documentation

%description apidocs
API documentation for rest library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki rest.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir} \
	--with-ca-certificates=/etc/certs/ca-certificates.crt
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{!?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_gtkdocdir}}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/librest-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librest-%{apiver}.so.0
%attr(755,root,root) %{_libdir}/librest-extras-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librest-extras-%{apiver}.so.0
%{_libdir}/girepository-1.0/Rest-0.7.typelib
%{_libdir}/girepository-1.0/RestExtras-0.7.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librest-%{apiver}.so
%attr(755,root,root) %{_libdir}/librest-extras-%{apiver}.so
%{_datadir}/gir-1.0/Rest-%{apiver}.gir
%{_datadir}/gir-1.0/RestExtras-%{apiver}.gir
%{_includedir}/rest-%{apiver}
%{_pkgconfigdir}/rest-%{apiver}.pc
%{_pkgconfigdir}/rest-extras-%{apiver}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librest-%{apiver}.a
%{_libdir}/librest-extras-%{apiver}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/rest-%{apiver}
%endif
