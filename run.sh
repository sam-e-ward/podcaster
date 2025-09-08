#!/usr/bin/env bash

docker build -t feed-updater .

RepoRoot="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run --rm -v "${RepoRoot}:/app" feed-updater
