#!/bin/bash

set -e

PATH=$PATH:/local/riscv-tools/bin
PATH=$PATH:~/poets-ecosystem/
PATH=$PATH:~/poets-ecosystem/pts-serve/
PATH=$PATH:/local/ecad/altera/17.0/quartus/bin

echo "Started at $(date)"

/usr/bin/time -f "%e" timeout 3600 pts-serve \
	--code code.v \
	--data data.v \
	--elf net.elf \
	--headless true \
	--v 3
