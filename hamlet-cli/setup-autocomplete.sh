#!/usr/bin/env bash
if [[ $(basename $SHELL) = 'bash' ]];
then
    if [ -f ~/.bashrc ];
    then
        echo "Installing bash autocompletion..."
        grep -q 'hamlet-autocompletion' ~/.bashrc
        if [[ $? -ne 0 ]]; then
            echo "" >> ~/.bashrc
            echo 'eval "$(_HAMLET_COMPLETE=source hamlet)"' >> ~/.hamlet-autocompletion.sh
            echo "source ~/.hamlet-autocompletion.sh" >> ~/.bashrc
        fi
    fi
elif [[ $(basename $SHELL) = 'zsh' ]];
then
    if [ -f ~/.zshrc ];
    then
        echo "Installing zsh autocompletion..."
        grep -q 'hamlet-autocompletion' ~/.zshrc
        if [[ $? -ne 0 ]]; then
            echo "" >> ~/.zshrc
            echo "autoload bashcompinit" >> ~/.zshrc
            echo "bashcompinit" >> ~/.zshrc
            echo 'eval "$(_HAMLET_COMPLETE=source hamlet)"' >> ~/.hamlet-autocompletion.sh
            echo "source ~/.hamlet-autocompletion.sh" >> ~/.zshrc
        fi
    fi
fi
