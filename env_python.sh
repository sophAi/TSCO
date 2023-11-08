#!/bin/bash
anaconda_version=3.7
module load anaconda${anaconda_version}
#export PATH="$HOME/anaconda3:$PATH"
export PATH="$HOME/bin:$PATH"
if [[ -e "$HOME/.cache" ]]; then
    tmp_dir=`/bin/ls -d $HOME/.cache/* | grep gma --color=never`
    if [[ "$tmp_dir" != "" ]]; then
        export PYTHONPATH="./":"$tmp_dir/`/bin/ls -tr $tmp_dir/ |tail -n 1`:$PYTHONPATH"
    fi
fi
alias ipy="ipython3"
alias jl="julia"
alias ju="julia"
