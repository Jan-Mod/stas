#!/usr/bin/env bash

# scripts/utils.sh
parse_app_option() {
    for arg in "$@"; do
        case $arg in
            --app)
            next_arg="${2:-}"
                echo "$next_arg"
                return
            ;;
        esac
    done
    echo "requirements.txt"
}