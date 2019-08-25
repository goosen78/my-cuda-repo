#!/bin/sh
set -e

# Source function library.
. /etc/init.d/functions.sh

pkg=cuda
major_version=10.1
version=10.1.243
tarball=${pkg}-${version}-x86_64
dl_site=https://developer.nvidia.com/compute/cuda/$major_version/Prod/local_installers
run_file=cuda_${version}_418.87.00_linux.run

unpack_installer() {
	sh $run_file --extract=`pwd` --override
}

remove_binaries_included_in_system_packages() {
    rm -fr cuda-toolkit/jre
    rm -f cuda-toolkit/targets/x86_64-linux/lib/libOpenCL.so*
    rm -fr cuda-samples/common/lib
}

remove_stubs() {
	rm -fr cuda-toolkit/targets/x86_64-linux/lib/stubs
}

remove_installers() {
	rm -fr cuda-toolkit/bin/cuda-uninstaller \
    	cuda-samples/bin
}

move_out_gdb_sources() { 
	mv cuda-toolkit/extras/${pkg}-gdb-*.src.tar.gz .
}

create_tarball() {
	mkdir ${tarball}
	mv cuda-toolkit cuda-samples ${tarball}
	tar --remove-files -cJf ${tarball}.tar.xz ${tarball}
	echo "OK\n"
}

main() {
    # Verify CPU features needed to run Clear exist
    ebegin Unpack installer
    unpack_installer
    eend $?
    ebegin Creating tarball cuda-10.1.243-x86_64 ... 
    remove_binaries_included_in_system_packages
    eend $?
    ebegin Remove Stubs
    remove_stubs
    eend $?
    ebegin Remove Installers
    remove_installers
    eend $?
    ebegin Move out gdb sources
    move_out_gdb_sources
    eend $?
    ebegin Create tarball
    create_tarball
    eend $?
}

main
