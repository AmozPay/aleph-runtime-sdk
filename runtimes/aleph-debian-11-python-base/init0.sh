#!/bin/sh

set -euf

mount -t proc proc /proc -o nosuid,noexec,nodev

log() {
    echo "$(cat /proc/uptime | awk '{printf $1}')" '|S' "$@"
}
log "init0.sh is launching"

# Switch root from read-only ext4 to to read-write overlay
mkdir -p /overlay
/bin/mount -t tmpfs -o noatime,mode=0755 tmpfs /overlay
mkdir -p /overlay/root /overlay/work
/bin/mount -o noatime,lowerdir=/,upperdir=/overlay/root,workdir=/overlay/work -t overlay "overlayfs:/overlay/root" /mnt
mkdir -p /mnt/rom
pivot_root /mnt /mnt/rom

mount --move /rom/proc /proc
mount --move /rom/dev /dev

mkdir -p /dev/pts
mkdir -p /dev/shm

mount -t sysfs sys /sys -o nosuid,noexec,nodev
mount -t tmpfs run /run -o mode=0755,nosuid,nodev
#mount -t devtmpfs dev /dev -o mode=0755,nosuid
mount -t devpts devpts /dev/pts -o mode=0620,gid=5,nosuid,noexec
mount -t tmpfs shm /dev/shm -omode=1777,nosuid,nodev

# List block devices
lsblk

#cat /proc/sys/kernel/random/entropy_avail

# TODO: Move in init1
mkdir -p /run/sshd
/usr/sbin/sshd &
log "SSH UP"

log "Setup socat"
socat UNIX-LISTEN:/tmp/socat-socket,fork,reuseaddr VSOCK-CONNECT:2:53 &
log "Socat ready"

# executing user custom init sequence, if any
if [ -e /root/init0_plugin.sh ]
then
    log "Found init0_plugin.sh sequence, exectuting"
    /root/init0_plugin.sh
else
    log "No user defined init0_plugin.sh sequence, skipping"
fi


# this section is for testing plugins with 'aleph runtime test'
if [ -e /root/sdk_test ]
then
    log "Running runtime plugin testing init sequence instead of /root/init1.py"
    exec /root/init_test.py
fi

# Replace this script with the manager
exec /root/init1.py
