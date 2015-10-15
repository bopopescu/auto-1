#!/bin/sh
yum clean all
yum makecache

yum -y update




yum -y install gcc-fortran

