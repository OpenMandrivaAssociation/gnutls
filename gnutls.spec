%define major 28
%define sslmajor 27
%define xsslmajor 0
%define libname %mklibname %{name} %{major}
%define libssl %mklibname %{name}-ssl %{sslmajor}
%define libxssl %mklibname %{name}-xssl %{xsslmajor}
%define devname %mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	3.1.9.1
Release:	2
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://www.gnutls.org
Source0:	http://ftp.gnu.org/pub/gnu/gnutls/%{name}-%{version}.tar.xz
BuildRequires:	liblzo-devel
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(nettle)
%ifnarch %{arm} %{mips}
BuildRequires:	valgrind
%endif

%description
GnuTLS is a project that aims to develop a library which provides 
a secure layer, over a reliable transport layer.

%package -n	%{libname}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
%if "%{_lib}" == "lib64"
Conflicts:	lib%{name}%{major} < %{version}
%endif
Obsoletes:	%{mklibname gnutls 26} <= 2.12.14
Requires:	%{name}-locales = %{version}-%{release}

%description -n	%{libname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n	%{libssl}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries

%description -n	%{libssl}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n	%{libxssl}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Requires:	%{libname} = %{version}

%description -n	%{libxssl}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libssl} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 13 -d

%description -n	%{devname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%package locales
Summary:	Locale files for GnuTLS
Group:		System/Internationalization 
Requires:	%{libname} = %{version}
BuildArch:	noarch
# (tpg) conflict older libname
Conflicts:	%{mklibname gnutls 28} <= 3.1.9.1-1

%description
Locale files for GnuTLS main library.

%prep
%setup -q -n %{name}-3.1.9

%build
%configure2_5x \
	--disable-static \
	--with-included-libtasn1=no \
	--with-included-libcfg=yes \
	--with-lzo \
	--with-libz-prefix=%{_prefix} \
	--with-libgcrypt \
	--with-libgcrypt-prefix=%{_prefix} \
	--with-libtasn1-prefix=%{_prefix} \
%ifnarch %{arm} %{mips}
	--enable-valgrind-tests \
%endif
	--disable-rpath \
	--disable-guile

%make

%check
make check

%install
%makeinstall_std

%find_lang gnutls

%files
%doc NEWS README
%{_bindir}/[cgs]*
%{_bindir}/danetool
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/ocsptool
%{_mandir}/man?/*
%{_infodir}/*

%files locales -f gnutls.lang

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{libssl}
%{_libdir}/lib*.so.%{sslmajor}*

%files -n %{libxssl}
%{_libdir}/lib*.so.%{xsslmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnutls

