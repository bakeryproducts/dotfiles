import os
import subprocess
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


from Xlib import display
from Xlib.ext import randr

def get_screens():
    d = display.Display()
    return d.screen_count()
    #res = d.screen().root.xrandr_get_screen_resources()._data
    #num_screens = 0
    #for output in res['outputs']:
    #    mon = d.xrandr_get_output_info(output, res['config_timestamp'])._data
    #    if mon['preferred']: num_screens += 1
    #return num_screens

def init_keys():
    keys = [
        # Switch between windows
        #Key([mod], "Return", lazy.layout.left(), desc="Move focus to left"),
        #Key([mod], "Return", lazy.layout.right(), desc="Move focus to right"),
        Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
        Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
        Key([mod], "n", lazy.layout.next(), desc="Move window focus to other window"),

        # Move windows between left/right columns or move up/down in current stack.
        # Moving out of range in Columns layout will create new column.
        Key([mod], "n", lazy.layout.shuffle_left(), desc="Move window to the left"),
        Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

        # Grow windows. If current window is on the edge of screen and direction
        # will be to screen edge - window would shrink.
        Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
        Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
        Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
        Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes
        Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
        Key([mod], "space", lazy.spawn(terminal), desc="Launch terminal"),

        # Toggle between different layouts as defined below
        Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
        Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

        Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
        Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
        #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

        # CUSTOM
        Key([mod], "d", lazy.spawn("dmenu_run -p 'Run: '"), desc='Dmenu Run Launcher'),
        Key([mod], "h", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window (MonadTall), increase number in master pane (Tile)'),
        Key([mod], "l", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window (MonadTall), decrease number in master pane (Tile)'),
        Key([mod], "r", lazy.layout.reset(), desc='normalize window size ratios'),
        Key([mod], "m", lazy.layout.maximize(), desc='maximizse window size ratios'),
        Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
        Key([mod], 't', lazy.window.toggle_floating()),
    ]

    return keys

def init_groups():
    global num_screens
    global mod

    pinned_groups = ['1234567890'] if num_screens == 1 else  ['12345', '67890']
    all_groups = ''.join(pinned_groups)
    groups = [Group(i) for i in all_groups]
    group_keys = []

    for j, names in enumerate(pinned_groups):
        group_keys += [Key([mod], i, lazy.to_screen(j), lazy.group[i].toscreen()) for i in names]

    group_keys += [Key([mod, 'shift'], i, lazy.window.togroup(i)) for i in all_groups]

    return pinned_groups, groups, group_keys 

def init_layouts():
    global border_focus 
    layouts = [
        layout.MonadTall(new_at_current=False, border_focus=border_focus, border_width=1, margin=0, ratio=.6),
        layout.Stack(num_stacks=2),
        layout.Tile(shift_windows=True),
        #layout.Columns(border_focus_stack='#d75f5f'),
        #layout.Max(),
        # layout.Matrix(),
        # layout.MonadWide(),
        # layout.VerticalTile(),
    ]
    return layouts

def init_widgets():
    widget_defaults = dict(
        font='sans',
        fontsize=12,
        padding=3,
    )
    extension_defaults = widget_defaults.copy()
    return extension_defaults 

def get_bbar(pin_group):
    return bar.Bar(
            [
                widget.CurrentLayout(),
                widget.Sep(),
                widget.GroupBox(visible_groups=pin_group),
                widget.Prompt(),
                widget.Sep(),
                widget.WindowName(),
                widget.Sep(),
                #widget.Systray(),
                widget.Clock(format='%d-%m %a %I:%M %p'),
                widget.QuickExit(),
            ],
            24,
     )

def init_screens(pinned_groups):
    global num_screens
    screens = []
    for screen in range(0, num_screens):
        screens.append( Screen(bottom=get_bbar(pinned_groups[screen])) )
    return screens 

#def main():
num_screens = get_screens()
mod = "mod1"
terminal = "urxvt"
border_focus = '#E6C229'
keys = init_keys()
pinned_groups, groups , group_keys = init_groups()
layouts = init_layouts()
extension_defaults = init_widgets()
screens = init_screens(pinned_groups)
keys += group_keys

auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])

@hook.subscribe.startup_once 
def autostart():
    home = os.path.expanduser('~') 
    subprocess.call([home + '/.config/qtile/autostart.sh'])


#if __name__ == '__main__':
#    main()
