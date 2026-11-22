import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("homelab-ssh")
BLOCKED_PATTERNS = ["rm -rf /", "mkfs", "dd if=", ":(){", "shutdown", "reboot", "poweroff"]

@mcp.tool()
def ssh_run(host: str, command: str, timeout: int = 30) -> str:
    """Run a shell command on a remote homelab server via SSH."""
    lowered = command.lower()
    if any(bad in lowered for bad in BLOCKED_PATTERNS):
        return f"Blocked potentially destructive command: {command}"

    result = subprocess.run(
        [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=10",
            "-o", "StrictHostKeyChecking=accept-new",
            host,
            command,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = []
    if result.stdout:
        output.append(f"STDOUT:\n{result.stdout.strip()}")
    if result.stderr:
        output.append(f"STDERR:\n{result.stderr.strip()}")
    output.append(f"EXIT_CODE: {result.returncode}")
    return "\n\n".join(output)

@mcp.tool()
def ssh_read_file(host: str, remote_path: str, tail_lines: int = 200) -> str:
    """Read the last N lines of a log or configuration file on a remote server."""
    return ssh_run(host=host, command=f"tail -n {int(tail_lines)} -- {remote_path!r}")

if __name__ == "__main__":
    mcp.run(transport="stdio")
