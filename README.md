# PBEasy (ppb, for PivatePasteBin) - PrivateBin Terminal Helper Script

**Mirrors:**
- https://git.envs.net/dan/pbeasy
- https://github.com/dan-envs/pbeasy

PBEasy (`ppb`) is a Bash script that streamlines the process of creating,
uploading, and commenting on [PrivateBin](https://privatebin.info/)
pastes directly from your terminal. It provides an interactive interface
for replying to comments, supports attachments, and integrates with your
preferred text editor.

---

## Features

- **Create new PrivateBin pastes** from files or stdin.
- **Upload attachments** (images, files) with optional comments.
- **Interactive comment/reply selection** using `dialog`.
- **Reply to nested comments** with preview and editing.
- **Clipboard integration**: Automatically copies resulting URLs using `xclip`.
- **Uses your `$EDITOR`** for editing comments and replies.
- **Customizable defaults** via a config file.

---

## Dependencies

Make sure the following tools are installed (it seems all of them are available
on envs):

- [`pbcli`](https://github.com/Mydayyy/pbcli) (PrivateBin CLI client written in rust, installed on envs)
- [`jq`](https://jqlang.org/) (JSON processor)
- [`dialog`](https://invisible-island.net/dialog/) (terminal UI)
- [`xclip`](https://github.com/astrand/xclip) (clipboard utility)
- `fold`, `mktemp`, `diff`, `cat`, `tee` (coreutils)
- A text editor set in your `$EDITOR` environment variable (e.g., `nvim`, `vim`, `nano`)

---

## Installation

1. **Download the script:**

   Save the `ppb` script to a directory in your `$PATH`, for example:

   ```sh
   mkdir -p ~/bin
   cp ppb ~/bin/
   chmod +x ~/bin/ppb
   ```

   Ensure `~/bin` is in your `$PATH` (add `export PATH="$HOME/bin:$PATH"` to
   your shell config if needed).

2. **Create initial configuration:**

   Run:

   ```sh
   ppb -i
   ```

   This creates a config file at `$XDG_CONFIG_HOME/pbeasy/config.sh` (defaults
   to `~/.config/pbeasy/config.sh`). Edit this file to change default server,
   format, or discussion settings.

---

## Usage

```sh
ppb [-i] | [ -u <FILE> | -c <URL> ] [-d] [-f <FORMAT> ] [-s <HOST URL>] | [-h]
```

### Options

- `-i`  
  Create a default config file at `$XDG_CONFIG_HOME/pbeasy/config.sh`.

- `-c <URL>`  
  Comment or reply to a comment on a PrivateBin paste. If a URL is provided,
  fetches comments and allows replying by choosing a comment/reply from a list
  (with preview). Uses your `$EDITOR` for editing.

- `-u <FILE>`  
  Upload a file as an attachment. If piped with text, the text is used as a
  comment.

- `-s <HOST URL>`  
  Specify the PrivateBin server. Defaults to `https://pb.envs.net/`.

- `-d`  
  Enable discussion/comments for the paste (off by default).

- `-f <FORMAT>`  
  Specify the paste format: `markdown`, `plaintext`, or `syntax`.
  Default is `plaintext`.

- `-h`
  Show help message.

---

## Examples

- **Send a file as a markdown paste:**

  ```sh
  ppb -f markdown < file.md
  ```

- **Comment or reply to a comment:**

  ```sh
  ppb -c "https://pb.envs.net/<paste>#<key>"
  ```

- **Send a new paste with comments enabled:**

  ```sh
  cat message.txt | ppb -d -f plaintext
  ```

- **Send an image with a comment:**

  ```sh
  echo "My nice picture" | ppb -u image.png
  ```

---

## Configuration

Edit `$XDG_CONFIG_HOME/pbeasy/config.sh` to set:

- `HOST` (default PrivateBin server)
- `FORMAT` (default paste format)
- `DISCUSSION` (enable/disable comments by default)

Other options (like `--comment-as=<name>`) are read from your `pbcli` config file.

---

## Use Issue Tracker

If you have any problems with `ppb`, use one of the Issue trackers:

- https://git.envs.net/dan/pbeasy/issues
- https://github.com/dan-envs/pbeasy/issues

---

## License

This script is licensed under the **GPL-3.0-only** license. See [LICENSE](LICENSE) for details.
