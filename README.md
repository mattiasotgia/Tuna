# TUNA: Training for Understanding Neutrino events in Argon :fishing_pole_and_fish:

```markdown
                  ><(((º>  .... ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░
      ><(((º>              ....    ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
               ><(((º>     ....    ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
   ><(((º>                 ....    ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░
           ><(((º>         ....    ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
             ><(((º>       ....    ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
 ><(((º>                   ....    ░▒▓█▓▒░    ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░

TUNA: Training for Understanding Neutrino events in Argon
```

# Installation and usage

To install this package and its relative cli app `tuna` the easiest way is to clone this repository and then once in the repository top directory run the command 

```bash
pip install -e .
```
This ensure both the `tuna` cli and the `tuna` module are installed in the system. It is suggested that the installation happens inside a python virtual environment. One very basic environment can be created by running 

```bash
python3 -m venv tuna_env
source tuna_env/bin/activate
```

## Note
The modules make use of the `$TUNA_PATH` environment variable, so it is suggested this is added to either the `.bashrc` or `.zshenv` by running 

```bash 
echo export TUNA_PATH=${cwd} >> .bashrc
```

<!--# Installation and usage

The executable is the `tuna.run` python script. However the suggested usage is to add the alias `tuna` to the `.bashrc/zshenv` file, by running (inside the base directory of the repository)
```bash
echo alias tuna="'python3 $PWD/tuna.py'" >> ~/.bashrc
```

> For `zsh` users the command should be
> ```bash
> echo alias tuna="'python3 $PWD/tuna.py'" >> ~/.zshenv
> ```

This way the executable can be run by the `tuna` command-->

## Note about usage

The project, intended for use in LArSoft training for any  BDT is made of a set of python modules that can be controlled just by editing the `json` configuration file passed to the cli command `tuna`, is indipendent from any `LArSoft` external module. The data has to be passed as a `.txt` file format (common file format for BDT training) containing the values of the variables used to perform the cuts, for each event. The ouput model is passed as a `.xml` common in TMVA modeling and in `.pkl` common to store serialized machine learning models.

# Wiki and documentation

A _sort-of-detailed_ __how-to__ guide is presented in [`doc/documentation.md`](doc/documentation.md). However, as most say[^1], perfect documentation is not that useful, so the best way to understand the code is actually to look inside.

The guide is basically a list of all the current possible configurations of the different modules. Some possible tests are in the [`configurations/`](configurations/) folder.



[^1]: Rule 1 of writing software for nontechnical users is this: if they have to read documentation to use it you designed it wrong.   -- Eric S. Raymond, programmer and advocate of open source software
