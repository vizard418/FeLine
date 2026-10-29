_feline_completions() {
    local cur prev opts models schemes config_file
    COMPREPLY=()

    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="-h --help --model --model-config --scheme-config --interactive --purge --show-models --show-chats --resume-chat --show-chat --delete-chat --rename-chat"

    config_file="$(dirname "${BASH_SOURCE[0]}")/config/models.ini"

    if [ -f "$config_file" ]; then
        models=$(awk '/^\[availables\]/{flag=1; next} /^\[/{flag=0} flag && /=/ {print $1}' "$config_file")
    else
        models="gemini-lite gemini-flash gemini-pro gpt-oss-120b gpt-oss-20b qwen-coder"
    fi

    schemes="gruvbox nord"

    case "${prev}" in
        --model|--model-config)
            COMPREPLY=( $(compgen -W "${models}" -- "${cur}") )
            return 0
            ;;
        --scheme-config)
            COMPREPLY=( $(compgen -W "${schemes}" -- "${cur}") )
            return 0
            ;;
        --resume-chat|--show-chat|--delete-chat|--rename-chat)
            return 0
            ;;
    esac

    if [[ "${cur}" == -* ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
        return 0
    fi

    if [[ "${COMP_WORDS[COMP_CWORD-2]}" == "--rename-chat" ]]; then
        return 0
    fi
}

complete -F _feline_completions feline
