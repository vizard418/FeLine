_feline_completions() {
    local cur prev opts models config_file
    COMPREPLY=()

    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="-h --help --model --model-config --interactive --purge --show-models --show-chats --resume-chat --show-chat"
    
    # Ruta al models.ini (busca primero en el directorio de config del script o usa el fallback del proyecto)
    config_file="$(dirname "${BASH_SOURCE[0]}")/config/models.ini"
    
    if [ -f "$config_file" ]; then
        # Extrae las keys de la seccion [availables] de forma dinamica
        models=$(awk '/^\[availables\]/{flag=1; next} /^\[/{flag=0} flag && /=/ {print $1}' "$config_file")
    else
        # Fallback por si acaso si no encuentra el archivo estático
        models="gemini-lite gemini-flash gemini-pro gpt-oss-120b gpt-oss-20b"
    fi

    case "${prev}" in
        --model|--model-config)
            COMPREPLY=( $(compgen -W "${models}" -- "${cur}") )
            return 0
            ;;
        --resume-chat|--show-chat)
            return 0
            ;;
    esac

    if [[ "${cur}" == -* ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
        return 0
    fi
}

complete -F _feline_completions feline
