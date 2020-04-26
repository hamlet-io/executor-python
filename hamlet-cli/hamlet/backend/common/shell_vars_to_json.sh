function read(){
  local filename=$1; shift;
  declare -a args=("$@")

  cat <<END
function read(){
  source $filename
  printf "{\n"
END

for (( arg_index=0; arg_index < "${#args[@]}"; arg_index++ ))
do
  local variable_name="${args[$arg_index]}"
  local variable_type="${args[$arg_index+1]}"
  let "arg_index++"
  case $variable_type in
    l)
      cat <<END
  printf "  \"$variable_name\":[\n"
  local index=0
  for value in "\${$variable_name[@]}"; do
    let "index++"
    if [[ "\${#$variable_name[@]}" == "\${index}" ]]; then
      printf "    \"\${value}\"\n"
    else
      printf "    \"\${value}\",\n"
    fi
  done
  printf "  ]"
END
    ;;
    d)
      cat <<END
  printf "  \"$variable_name\":{\n"
  local index=0
  for key in "\${!$variable_name[@]}"; do
    let "index++"
    if [[ "\${#$variable_name[@]}" == "\${index}" ]]; then
      printf "    \"\${key}\":\"\${$variable_name[\$key]}\"\n"
    else
      printf "    \"\${key}\":\"\${$variable_name[\$key]}\",\n"
    fi
  done
  printf "  }"
END
    ;;
    s)
    cat <<END
  printf "  \"$variable_name\":\"\$$variable_name\""
END
    ;;
  esac
  if (( "$arg_index" < "${#args[@]}-1" )); then
    cat <<END
  printf ",\n"
END
  else
    cat <<END
  printf "\n"
END
  fi

done
  cat <<END
  printf "}\n"
}
read
END
}


read $@ | bash
