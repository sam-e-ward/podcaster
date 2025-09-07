$ErrorActionPreference = "Stop"

docker build -t feed-updater .

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

docker run --rm -v "${RepoRoot}:/app" feed-updater
