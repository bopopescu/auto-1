CC?=cc
prefix=/usr/local
exec_prefix=/usr/local
bindir=/usr/local/bin
libdir=/usr/local/lib
includedir=/usr/local/include
sysconfdir=/usr/local/etc
NO_AS_NEEDED=
LDSO_SUFFIX=dylib
MAC_CFLAGS+=-DIS_MAC=1
LD_SET_SONAME=-Wl,-install_name,
