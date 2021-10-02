#!/usr/bin/env bash
echo "Updating default hamlet engine"

if which "hamlet"; then
    hamlet engine install-engine --update
fi
