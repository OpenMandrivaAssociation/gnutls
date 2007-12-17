# older opencdk forgot to bundle m4 file
%define opencdk_version 0.5.4-2mdk
%define libgcrypt_version 1.1.94

%define major 13
%define libname %mklibname %{name} %{major}
%define libname_orig lib%{name}
%define develname %mklibname %{name} -d

Summary:	Library providing a secure layer (SSL)
Name:		gnutls
Version:	2.0.4
Release:	%mkrel 1
URL:		http://www.gnutls.org
License:	GPLv2+/LGPLv2.1+
Group:		System/Libraries
Source0:	http://www.gnu.org/software/gnutls/releases/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
BuildRequires:	opencdk-devel >= %{opencdk_version}
BuildRequires:	liblzo-devel
BuildRequires:	libgcrypt-devel >= %{libgcrypt_version}

%description
GnuTLS is a project that aims to develop a library which provides 
a secure layer, over a reliable transport layer.

%package -n	%{libname}
Summary:	Library providing a secure layer (SSL)
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n	%{libname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	opencdk-devel >= %{opencdk_version}
Requires:	libgcrypt-devel >= %{libgcrypt_version}
Obsoletes:	%mklibname %{name} 13 -d

%description -n	%{develname}
GnuTLS is a project that aims to develop a library which provides
a secure layer, over a reliable transport layer.

This package contains all necessary files to compile or develop
programs/libraries that use %{name}.

%prep
%setup -q
autoreconf

%build
export CPPFLAGS="-I%{_includedir}/lzo"
%configure2_5x \
	--with-included-libtasn1=yes \
	--with-included-libcfg=yes \
	--disable-srp-authentication \
	--with-libz-prefix=%{_prefix} \
	--with-libgcrypt \
	--with-libgcrypt-prefix=%{_prefix} \
	--disable-rpath

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%{find_lang} %{name}
%multiarch_binaries %{buildroot}%{_bindir}/libgnutls-config %{buildroot}%{_bindir}/libgnutls-extra-config

%clean
rm -rf %{buildroot}

%post
%_install_info gnutls.info

%post -p /sbin/ldconfig -n %{libname}

%postun
%_remove_install_info gnutls.info

%postun -p /sbin/ldconfig -n %{libname}

%files -f %{name}.lang 
%defattr(-,root,root)
%doc ChangeLog NEWS README COPYING
%{_bindir}/[cgs]*
%{_bindir}/psktool
%{_mandir}/man?/*
%{_infodir}/gnutls*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_bindir}/libgnutls*
%{_includedir}/gnutls
%{_datadir}/aclocal/*

%multiarch
%{multiarch_bindir}/libgnutls-config 
%{multiarch_bindir}/libgnutls-extra-config 
