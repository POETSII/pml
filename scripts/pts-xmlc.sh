#!/bin/bash

set -e

PATH=$PATH:/local/riscv-tools/bin
PATH=$PATH:~/poets-ecosystem/
PATH=$PATH:~/poets-ecosystem/pts-serve/
PATH=$PATH:/local/ecad/altera/17.0/quartus/bin

pts-xmlc output.xml \
	--vcode=code.v \
	--vdata=data.v \
	-o net.elf \
	--hardware-handler-log-level=0 \
	> /dev/null
