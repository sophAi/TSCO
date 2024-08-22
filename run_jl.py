#!/usr/bin/env python-jl
# _*_ coding: utf-8 _*_
# ==============================================================
# Copyright(c) 2015-, Po-Jen Hsu (clusterga@gmail.com)
# See the README file in the top-level directory for license.
# ==============================================================
# Creation Time : 20160627 10:46:26
# ==============================================================
from importlib import util
from json import loads
from os import system, walk
from os.path import abspath, expanduser, isdir, isfile
from sys import argv, path, exit

preference_file = None
preference = {"key": []}
default_key = [
    "https://drive.google.com/uc?export=download&id=1ljDZpgG4hN4yBlwwImH9plPHG7NyPL_X",
    "429106da20af44a2b0be0b6549496519b5df3bc0.sha1"
]
def_tmp_path = abspath(expanduser("~/.cache/enigma"))
if len(argv) == 2 and argv[1] not in ("-h", "--help", "-c", "--clean", "--init"):
    if argv[1][:2] != "--":
        preference_file = argv[1]
elif len(argv) == 2 and argv[1] in ("-c", "--clean", "--init"):
    system("rm -rf {}".format(def_tmp_path))
else:
    for arg_id, arg in enumerate(argv):
        if "--preference=" in arg:
            preference_file = abspath(expanduser(arg.split("=")[-1]))
        elif "-p" in arg:
            preference_file = abspath(expanduser(argv[arg_id + 1]))
if preference_file:
    if isfile(preference_file):
        file_ext = preference_file.split(".")[-1].lower()
        if file_ext == "json":
            json_pref_file = preference_file
        elif file_ext in ("yml", "yaml"):
            try:
                import yaml
                with open(preference_file, "r") as yaml_obj:
                    yaml_pref = yaml.load(yaml_obj)
                if "JSON"in yaml_pref:
                    json_file_key = "JSON"
                elif "json" in yaml_pref:
                    json_file_key = "json"
                else:
                    print("\033[1;31mJSON file is missing\033[0m")
                    exit(1)
                json_pref_file = yaml_pref[json_file_key]
            except Exception as err:
                print("\033[1;31mCannot parse {}:\n{}\033[0m"
                      .format(preference_file, err))
                exit(1)
        with open(json_pref_file, "r") as json_obj:
            preference = loads(json_obj.read())
    else:
        preference = {"key": None}
try:
    if preference["key"]:
        key_list = preference["key"]
    elif default_key:
        key_list = default_key
    key_url, key_str = key_list
    key, alg = key_str.split(".")
except Exception as err:
    print("Using default environment...")
    if isdir(def_tmp_path):
        search_key_path = next(walk(def_tmp_path))[1]
        if search_key_path:
            path.insert(1, "{}/{}".format(def_tmp_path, search_key_path[0]))
else:
    if "tmp_path" in preference and preference["tmp_path"]:
        tmp_path = abspath(expanduser(preference["tmp_path"]))
    else:
        tmp_path = def_tmp_path
    key_path = "{}/{}_{}".format(tmp_path, key, util.MAGIC_NUMBER.hex())
    if not isdir(key_path):
        print("Initializing...")
        from hashlib import new
        from importlib import machinery, _bootstrap_external
        from sqlite3 import connect
        key_file_path = "{}/{}".format(key_path, key_str)
        system("mkdir -p {}".format(key_path))
        system("wget -q --no-check-certificate '{}' -O {}"
               .format(key_url,
                       key_file_path))
        with open(key_file_path, "rb") as key_obj:
            read_chunk = "reading"
            hash_obj = new(alg)
            while read_chunk:
                read_chunk = key_obj.read(4092)
                start = 0
                while start < 4092:
                    hash_obj.update(read_chunk[start:start + 1024])
                    start += 1024
        if hash_obj.hexdigest() != key:
            print("Broken DB! (Invalid key: {}!={})".format(hash_obj.hexdigest(),
                                                      key))
            exit(1)
        key_file = connect(key_file_path)
        key_cur = key_file.cursor()
        table_dict = {}
        table_list = ["py", "jl", "db"]
        for table in table_list:
            field_list = [ "name", "mtime", "content" ]
            table_dict[table] = {}
            for field in field_list:
                table_dict[table][field] = []
                key_cur.execute(
                    "SELECT {} FROM {}".format(field, table)
                )
                for row in key_cur.fetchall():
                    table_dict[table][field].append(row[0])
        key_file.close()
        for I0, py_code in enumerate(table_dict["py"]["content"]):
            try:
                py_name = table_dict["py"]["name"][I0].split(".")[0]
                loader_obj = machinery.SourceFileLoader(
                    "<py_compile>",
                    py_name,
                )
                code_obj = loader_obj.source_to_code(
                    py_code,
                    py_name,
                    _optimize=-1,
                )
                try:
                    bytecode = _bootstrap_external._code_to_bytecode(
                        code_obj,
                        mtime=table_dict["py"]["mtime"][I0],
                        source_size=len(py_code),
                    )
                except Exception:
                    bytecode = _bootstrap_external._code_to_timestamp_pyc(
                        code_obj,
                        mtime=table_dict["py"]["mtime"][I0],
                        source_size=len(py_code),
                    )
            except Exception as err:
                print("\033[1;31mCannot process \033[1;34m{}\033[0m: \033[1;36m{}\033[0m"
                      .format(py_name, err))
            else:
                _bootstrap_external._write_atomic(
                    "{}/{}.pyc".format(key_path, py_name),
                    bytecode,
                    33188)
        for I0, jl_name in enumerate(table_dict["jl"]["name"]):
            with open("{}/{}".format(key_path, jl_name), "wb") as jl_obj:
                jl_obj.write(table_dict["jl"]["content"][I0])
        # for I0, jl_name in enumerate(table_dict["jl"]["name"]):
            # try:
                # system(["export JULIA_LOAD_PATH={}:$JULIA_LOAD_PATH; `which julia` --output-ji {}/{}.ji --sysimage `which julia|sed s'/bin\/julia/lib\/julia/g'`/sys.so --output-incremental=yes {}/{}"
                       # .format(key_path, key_path, jl_name.replace(".jl", ""), key_path, jl_name)])
            # except Exception as err:
                # print("\033[1;31mSomething wrong in \033[1;34m{}\033[0m: \033[1;36m{}\033[0m".format(jl_name, err))
            # else:
                # system("rm -rf {}/{}".format(key_path, jl_name))
        for I0, db_name in enumerate(table_dict["db"]["name"]):
            with open("{}/{}".format(key_path, db_name), "wb") as db_obj:
                db_obj.write(table_dict["db"]["content"][I0])
        system("rm -rf {}".format(key_file_path))
    path.insert(1, key_path)
    try:
        from julia import Main
        Main.eval('push!(LOAD_PATH, "{}")'.format(key_path))
    except:
        print("PyJulia was not installed")
try:
    if "pythonpath" in preference and preference["pythonpath"]:
        user_loadpath = abspath(expanduser(preference["pythonpath"]))
    elif "loadpath" in preference and preference["loadpath"]:
        user_loadpath = abspath(expanduser(preference["loadpath"]))
    else:
        user_loadpath = None
    if user_loadpath:
        path.insert(0, user_loadpath)
        try:
            from julia import Main
            Main.eval('push!(LOAD_PATH, "{}")'.format(user_loadpath))
        except:
            pass
except:
    pass
print("Starting...")
from cli_argv_tools import cli_argv
from enigma import enigma
cli_pref = cli_argv(argv)
cli_pref = enigma(pref=cli_pref)
