#!/bin/bash
# ==============================================================
# Copyright(c) 2018-, Po-Jen Hsu (clusterga@gmail.com)
# See the README file in the top-level directory for license.
# ==============================================================
# Creation Time : 20180427 14:37:31
# ==============================================================
revert_run=0
TSCO_dir=~/git_projects/jlkiams/TSCO
matplotlib_dir=~/.config/matplotlib
test_julia_package=JSON
command -v julia > /dev/null && { julia_path=`which julia`; has_julia_exe=1; } || { julia_path=""; has_julia_exe=0; }
run_name="run.py"
if [[ $has_julia_exe -eq 1 ]]; then
    if [[ "$JULIA_DEPOT_PATH" != "" ]]; then
        julia_dep_path=`echo -e $JULIA_DEPOT_PATH | awk -F":" '{print $1}'`
        if [[ -d "$julia_dep_path/packages/$test_julia_package" ]]; then
            run_name="run_jl.py"
        fi
    elif [[ -d "$HOME/.julia/packages/JSON" ]]; then
        run_name="run_jl.py"
    fi
fi
args=$#
while :
do
case $1 in
    #start $opt_help
    -h|--help)
        echo -n "Print help information"
        prog=`basename $0`
        echo -e "\n\033[1;32m$prog\033[0m - GNU GPL3 \033[1;36m`date +%Y` \033[1;32mPo-Jen Hsu\033[0m"
        echo -e "Contact: \033[1;34mclusterga@gmail.com\033[0m"
        echo -e "Last modification:\033[1;36m `date +"%F %T" -r $0`\033[0m"
        echo -e "\nUsage:"
        echo -e "\033[1;32m$prog \033[1;31m[options]\033[0m"
        echo -e "\nOptions:"
        awk '/#start \$opt_help/,/#end \$opt_help/' $0 | grep -v "(\|reset_expansion\|awk\|Example" | grep ")" -A 1 --no-group-separator | awk '{gsub(/\\033/,""); gsub(/    /,"\033[1;31m"); gsub(/\|/,"\033[1;33m, \033[1;31m"); gsub(/""/,"no option"); gsub(/echo -e -n "/,"\t\033[0m"); gsub(/echo -n -e "/,"\t\033[0m"); gsub(/echo -e "/,"\t\033[0m"); gsub(/echo -n "/,"\t\033[0m");gsub(/.$/,""); print}'
        echo -e "\033[0m\nExamples:"
        echo -e "\033[1;32m$prog \033[1;31m-r \033[0m(revert to previous version if it exists)"
        echo -e "\033[1;32m$prog \033[1;31m-i \033[1;34m~/git_projects/jlkiams/TSCO\033[0m"
        echo -e "\033[1;32m$prog \033[1;31m-m \033[1;34m~/.config/matplotlib\033[0m"
        exit 0;;
    -i)
        echo -n "Assign TSCO path"
        TSCO_dir=$2
        echo -e "= $TSCO_dir"
        shift 2;;
    -m)
        echo -n "Assign matplotlib config path"
        matplotlib_dir=$2
        echo -e "= $matplotlib_dir"
        shift 2;;
    -r)
        echo -e "Revert to previous version"
        revert_run=1
        shift ;;
    #end $opt_help
    "")
        if [[ $args -eq 0 ]]; then
            echo -e "Use \033[1;31m-h \033[0mor \033[1;31m--help \033[0mfor more information"
        fi
        break;;
    *)
        #echo -e "Other argument: $1"
        shift;;
    esac
done

if [[ $revert_run -eq 1 ]]; then
    if [[ -f "$matplotlib_dir/run.previous" ]] && [[ -d "$TSCO_dir" ]]; then
        read -p "(y/n): " yn
        if [[ "$yn" == "y" ]]; then
            cp -rf $matplotlib_dir/run.previous $matplotlib_dir/run.latest
            cp -rf $TSCO_dir/run.py $matplotlib_dir/run.previous
            cp -rf $TSCO_dir/run_jl.py $matplotlib_dir/run_jl.previous
            cp -rf $matplotlib_dir/run.latest $TSCO_dir/run.py
            cp -rf $matplotlib_dir/run_jl.latest $TSCO_dir/run_jl.py
            echo -e "\033[1;32mDone!\033[0m"
            exit 0;
        else
            echo -e "\n\033[1;31mAbort!\033[0m\n"
            exit 1;
        fi
    else
        echo -e "\n\033[1;31mPrevious or current $run_name is not exist! Abort!\n\033[0m"
    fi
fi
if [[ ! -d "$TSCO_dir" ]]; then
    mkdir -p $TSCO_dir
    cd $TSCO_dir
    cd ../
    git clone http://140.109.113.226:30000/jlkiams/TSCO.git
    mkdir -p $matplotlib_dir > /dev/null
    rsync --progress -hauv $TSCO_dir/.config/matplotlib/ $matplotlib_dir > /dev/null
    mkdir -p ~/bin
    rm -rf ~/bin/run.py
    rm -rf ~/bin/run_jl.py
    rm -rf ~/bin/update_run.sh
    #rm -rf ~/bin/env_python.sh
    cd ~/bin
    ln -s $TSCO_dir/run.py
    ln -s $TSCO_dir/run_jl.py
    ln -s $TSCO_dir/update_run.sh
    #ln -s $TSCO_dir/env_python.sh
    #grep_bashrc=`grep "source \$HOME/bin/env_python.sh" ~/.bashrc`
    #if [[ "$grep_bashrc" == "" ]]; then
        #echo -e "source \$HOME/bin/env_python.sh" >> ~/.bashrc
    #fi
fi

if [[ -d "$TSCO_dir" ]]; then
    cd $TSCO_dir
    cp run.py $matplotlib_dir/run.previous
    cp run_jl.py $matplotlib_dir/run_jl.previous
    #git pull
    git fetch
    git reset --hard origin/master
    cp run.py $matplotlib_dir/run.latest
    cp run_jl.py $matplotlib_dir/run_jl.latest
    ./$run_name --init
fi

echo -e "\nPlease \033[1;31mlog in again \033[0mor '\033[1;32msource ~/.bashrc\033[0m'\n"
