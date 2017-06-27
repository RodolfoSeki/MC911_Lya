#!/bin/bash

# Colors
ESC_SEQ="\x1b["
COL_RESET=$ESC_SEQ"39;49;00m"
COL_RED=$ESC_SEQ"31;01m"
COL_GREEN=$ESC_SEQ"32;01m"
COL_YELLOW=$ESC_SEQ"33;01m"
COL_BLUE=$ESC_SEQ"34;01m"
COL_MAGENTA=$ESC_SEQ"35;01m"
COL_CYAN=$ESC_SEQ"36;01m"
COL_BOLD=$ESC_SEQ";1m"


self="${0##*/}"

#if [ $# -lt 0 ]; then
#  printf "${COL_BOLD}%-8s${COL_RESET}: ./%s <entrada.lya>\n" "Uso" "$self"
#  printf "${COL_BOLD}%-8s${COL_RESET}: ./%s mc458abcd 01 projeto.pl\n" "Exemplo" "$self"
#  exit 1
#fi

pname="compiler.py"

echo "Executando os testes..."
erros=0
#mkdir -p dados$lab

FILES=./generate_examples/*.lya
for filename in $FILES; do
    file="${filename#./generate_examples/}"
    name="${file%.*}"
    
    res_file="./res/$name.txt"
    echo "$name"
    if [ -e "$res_file" ]
    then
        python3 "${pname}" "$filename" "--run" 2>&1 | diff -q - "$res_file" &>/dev/null
        if [ $? -eq 0 ]; then
            printf "${COL_GREEN}%-12s${COL_RESET}\n" "OK"
        else
            printf "${COL_RED}%-12s${COL_RESET}\n" "Error: output of $file doesn't match expected output"
            echo ">>> Saida esperada:"
            cat "$res_file"
            echo ">>> Saida do seu programa:"
            python3 "${pname}" "$filename" "--run" 2>&1
            echo
            erros=$(($erros+1))
        fi
    else
        printf "${COL_RED}%-12s${COL_RESET}\n" "Error: there is no output file for test $file"
        erros=$(($erros+1))
    fi
    echo
    #python3 "${pname}" "$filename" "--run" 2>&1 | diff -q - "$res_file" &>/dev/null
done






echo -e "\nTotal de erros encontrados: $erros"
