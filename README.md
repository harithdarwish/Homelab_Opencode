# Homelab Opencode

Setup for self-hosting **OpenCode** with a lightweight Python MCP server (`server.py`) instead of Docker inside a Proxmox LXC or a fresh Linux machine.

## Prerequisites
- SSH key access and host aliases configured in `~/.ssh/config` (`chmod 600 ~/.ssh/config`) for any target homelab servers you plan to manage over SSH.

---

Step:

1. Install System Packages and Create Project Folder.
```bash
apt update && apt install -y python3-venv python3-pip openssh-client curl ca-certificates
mkdir -p ~/projects/Opencode && cd ~/projects/Opencode
```
Verification: pwd prints /root/projects/Opencode (or your home path) and python3 -m venv --help succeeds.

2) Create Virtual Environment, Install MCP Dependency, and Write server.py. Set up .venv, install a consistent version of mcp[cli], and create server.py:
```bash
python3 -m venv .venv
/root/projects/Opencode/.venv/bin/pip install "mcp[cli]>=1.0.0,<2"
nano server.py
```
Verification: /root/projects/Opencode/.venv/bin/python -c "import mcp; print('MCP OK')" prints MCP OK and server.py exists in ~/projects/Opencode.

3) Install OpenCode and Verify PATH. run the OpenCode installer, reload ~/.bashrc, and verify the binary and version:
```bash
curl -fsSL https://opencode.ai/install | bash
source ~/.bashrc
ls -la ~/.opencode/bin/opencode
which opencode && opencode --version
```
Verification: which opencode prints a path (such as /root/.opencode/bin/opencode) and opencode --version outputs the installed version.

4) Configure ~/.config/opencode/opencode.json and Verify MCP. Create ~/.config/opencode/opencode.json pointing homelab-ssh to your .venv Python executable and server.py:
mkdir -p ~/.config/opencode
```
Verification: python3 -m json.tool exits with 0 (valid JSON) and opencode mcp list lists homelab-ssh.

  
