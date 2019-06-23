#!/bin/bash
# Short script for pairing headphones

# Headphones: 28:11:A5:D9:84:B0

# start connection
coproc bluetoothctl
# echo -e 'info 28:11:A5:D9:84:B0\nexit' >&${COPROC[1]}
echo -e 'scan on\n' >&${COPROC[1]}
echo -e 'connect 28:11:A5:D9:84:B0\n' >&${COPROC[1]}
echo -e 'exit\n' >&${COPROC[1]}


# get audio source id
echo $(pamixer --list-sources)
id=$(pamixer --list-sources | tail -n 1 | cut -d " " -f 1)
echo "Pairing with $id"

# switch audio source
pamixer --source $id
echo "Done switching to $id"

