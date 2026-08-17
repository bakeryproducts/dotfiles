#!/usr/bin/env bash
# Auto keyboard backlight: bright on activity, off after idle timeout.
set -u

LED=/sys/class/leds/tpacpi::kbd_backlight/brightness
NAME=${NAME:-"keyd virtual keyboard"}   # input device to watch
IDLE=${IDLE:-15}           # seconds of inactivity before off
LEVEL=${LEVEL:-2}          # on brightness (max 2)

# Resolve event node by device name from /proc/bus/input/devices
find_dev() {
    awk -v want="$NAME" '
        /^N: Name=/ { name=$0; sub(/.*Name="/,"",name); sub(/".*/,"",name) }
        /^H: Handlers=/ && name==want {
            match($0, /event[0-9]+/); print "/dev/input/" substr($0,RSTART,RLENGTH); exit }
    ' /proc/bus/input/devices
}
DEV=$(find_dev)
[ -z "$DEV" ] && { echo "device not found: $NAME" >&2; exit 1; }
[ -r "$DEV" ] || { echo "cannot read $DEV (need 'input' group?)" >&2; exit 1; }

state=-1
set_led() {
    [ "$1" = "$state" ] && return   # only write on change
    echo "$1" > "$LED" && state="$1"
}

# evdev rejects reads smaller than one input_event struct (24B on 64-bit),
# so bash can't read the device directly. Stream it via dd into a pipe;
# pipes allow 1-byte reads. dd bs=24 = one event per read(), no buffering.
exec 3< <(dd if="$DEV" bs=24 2>/dev/null)
reader=$!
cleanup() { set_led 0; kill "$reader" 2>/dev/null; }
trap 'cleanup; exit 0' TERM INT
trap cleanup EXIT

set_led 0
# read exit status: 0 = byte read (activity), >128 = idle timeout,
# otherwise EOF/error (dd died) -> bail instead of spinning.
while :; do
    if IFS= read -r -N1 -t "$IDLE" -u 3 _; then
        set_led "$LEVEL"
    else
        rc=$?
        if [ "$rc" -le 128 ]; then
            echo "input stream ended (rc=$rc), exiting" >&2
            exit 1
        fi
        set_led 0
    fi
done
