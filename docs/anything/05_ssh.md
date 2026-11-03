# SSH

<div class="dedication">
I want to dedicate this page to Prof. R Sekar!
</div>

## Quick Description (QD)

**SSH (Secure Shell)** is a protocol for securely connecting to remote systems over a network. It provides encrypted communication and is commonly used for remote login, command execution, and file transfer.

## Installation

Most Linux and macOS systems ship with the OpenSSH client. To install the server on Debian/Ubuntu (see also [What to Install on a Fresh VM?](02_vm.md)):

```shell
sudo apt update && sudo apt install openssh-server
```

## Useful Tips/Commands (UToC)

### Basic SSH Usage

- **Connect to a remote server:**

  ```shell
  ssh user@hostname
  ```

  - `user`: Username on the remote system.
  - `hostname`: IP address or domain name.

- **Specify a port:**

  ```shell
  ssh -p 2222 user@hostname
  ```

- **Run a command remotely:**

  ```shell
  ssh user@hostname 'ls -l /var/log'
  ```

### SSH Key Authentication

1. **Generate an SSH key pair:**

   ```shell
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

   - Default location: `~/.ssh/id_ed25519` and `~/.ssh/id_ed25519.pub`

2. **Copy the public key to the remote server:**

   ```shell
   ssh-copy-id user@hostname
   ```

   - Or manually append `~/.ssh/id_ed25519.pub` to `~/.ssh/authorized_keys` on the server.

3. **Connect using the key:**

   ```shell
   ssh user@hostname
   ```

### SSH Agent

- **Start the agent and add your key:**

  ```shell
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
  ```

### SSH Config File

Customize connections in `~/.ssh/config`:

```text
Host myserver
    HostName example.com
    User alice
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

Connect with:

```shell
ssh myserver
```

### Port Forwarding

- **Local port forwarding** (access remote port 80 via local port 8080):

  ```shell
  ssh -L 8080:localhost:80 user@hostname
  ```

- **Remote port forwarding** (expose local port 3000 on remote port 9090):

  ```shell
  ssh -R 9090:localhost:3000 user@hostname
  ```

### Copying Files

- **Using scp:**

  ```shell
  scp file.txt user@hostname:/path/to/dest/
  scp user@hostname:/path/to/file.txt .
  ```

- **Using rsync:**

  ```shell
  rsync -avz file.txt user@hostname:/path/to/dest/
  ```

### Other Useful SSH Commands

- **Check the SSH version:**

  ```shell
  ssh -V
  ```

- **Verbose/debug connection:**

  ```shell
  ssh -v user@hostname
  ```

- **Kill a hung SSH session:** Press Enter, then `~.` (tilde, then dot) in the SSH terminal. `~?` lists all escape sequences.

### Server-Side Configuration

- **Config file:** `/etc/ssh/sshd_config`
- **Test the config, then restart the SSH service (the unit is `ssh` on Debian/Ubuntu and `sshd` on RHEL-based systems):**

  ```shell
  sudo sshd -t
  sudo systemctl restart sshd
  ```

- **Common options:**

  ```text
  PermitRootLogin no
  PasswordAuthentication no
  PubkeyAuthentication yes
  AllowUsers alice bob
  ```

### Security Tips

- Use SSH keys, not passwords.
- Disable root login (`PermitRootLogin no`).
- Change the default port (optional).
- Use strong passphrases.
- Regularly update OpenSSH.

## Examples (e.g.,)

_Nothing here yet._

## References

- [ssh(1) manual](https://man.openbsd.org/ssh)
- [ssh_config(5) manual](https://man.openbsd.org/ssh_config)
- [sshd_config(5) manual](https://man.openbsd.org/sshd_config)
- [ssh-keygen(1) manual](https://man.openbsd.org/ssh-keygen)
- [ssh-agent(1) manual](https://man.openbsd.org/ssh-agent)
- [scp(1) manual](https://man.openbsd.org/scp)
