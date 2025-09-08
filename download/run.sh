#!/usr/bin/env bash

docker build -t feed-downloader .

RepoRoot="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ArgsString="$*"

docker run --rm -v "${RepoRoot}:/app" feed-downloader ./download.sh ${ArgsString}
