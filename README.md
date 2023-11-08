TSCO (Two-stage Clustering Optimization)
========================================

Copyright(c) 2016-, Po-Jen Hsu (clusterga@gmail.com)                           

Published under GNU General Public License Version 3, 29 June 2007

Author: Po-Jen Hsu


Requirements
------------

* Linux, Python(>=3.5), and numpy.


Installation
------------

Either execute `update_run.sh` to install or use the following steps:

1. `mkdir -p ~/git_projects/jlkiams/; mkdir -p ~/bin`

2. `cd ~/git_projects/jlkiams; git clone http://140.109.113.226:30000/jlkiams/TSCO.git`

3. `cd ~/bin`

4. `ln -s ~/git_projects/jlkiams/TSCO/run.py` 

5. `ln -s ~/git_projects/jlkiams/TSCO/update_run.sh` 

6. `ln -s ~/git_projects/jlkiams/TSCO/env_python.sh` 

7. Add `source ~/bin/env_python.sh` to your `~/.bashrc`


Usage
-----

* `run.py --init` after you update run.py.

* `run.py -p *.json` to perform tasks listed in the *.json file.

* `run.py -t *.json` to create template json file.

* The json files can be found in [sugar_tools](http://140.109.113.226:30000/jlkiams/sugar_tools)
