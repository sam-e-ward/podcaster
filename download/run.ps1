
$ErrorActionPreference = "Stop"

docker build -t feed-downloader .

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$ArgsString = $Args -join " "

docker run --rm -v "${RepoRoot}:/app" feed-downloader ./download.sh $ArgsString
