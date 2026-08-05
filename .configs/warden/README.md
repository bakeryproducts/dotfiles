# warden

Self-hosted Vaultwarden, reachable only inside a private tailnet.
Single-active-host design: exactly one machine runs the stack at a time,
state travels between machines through an encrypted cloud remote.

## Layout

- `warden` — the CLI, symlink it somewhere on `PATH`
- `docker-compose.yml` — vaultwarden + tailscale sidecar sharing one netns
- `serve.json` — tailscale serve config, terminates TLS, proxies to the app
- `.env.example` — template for the secrets file

Secrets and state live outside this repository.

## Usage

    warden up [--steal]   pull state, start, take lock
    warden down           stop, push state, release lock
    warden status         url, lock holder, containers, reachability
    warden logs [n]       follow container logs
    warden backups        list timestamped state backups on the remote
    warden url            print the vault url

## Prerequisites

- docker with the compose plugin
- tailscale on the host, MagicDNS and HTTPS certificates enabled in the tailnet
- rclone

## Rolling out on a machine

1. Copy `.env.example` to `~/.config/warden/env`, fill it in, `chmod 600`.
   Override the location with `WARDEN_ENV` if you prefer.
   The tailscale auth key must be **reusable**, not ephemeral — the node
   identity is part of the synced state.

2. Symlink the CLI onto `PATH`:

       ln -s "$PWD/warden" ~/.local/bin/warden

3. Configure the cloud remote, then wrap it in an rclone `crypt` remote.
   On every additional machine the crypt password and salt must be
   **identical** to the first machine, otherwise the state cannot be
   decrypted. Reuse the values stored in the secrets file rather than
   generating new ones.

4. `warden up`. First boot on a fresh tailnet registers the node and issues a
   certificate; expect a delay of a minute or so.

## Switching machines

    warden down     # on the machine currently running it
    warden up       # on the other machine

`warden down` pushes state and releases the lock. `warden up` refuses to start
if the lock is held elsewhere; overwritten files are moved into timestamped
backup folders on the remote rather than discarded.

If a machine died without releasing the lock, `warden up --steal` overrides it.
Only use this when that machine is genuinely gone — two live instances will
silently diverge.

## Notes

- Registration is disabled after the first account is created.
- The admin token is an argon2 PHC string, not plain text.
- State files are created by root inside the container; the CLI reclaims
  ownership before pushing.
- Switching takes a minute or two, dominated by tailscaled registration and
  cloud API round-trips. It is a per-switch cost, not a per-use one.
- Losing the master password means losing the data. There is no recovery path.
