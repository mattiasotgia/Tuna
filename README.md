# TUNA: Training for Understanding Neutrino events in Argon

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

The executable is the `tuna.run` python script. However the suggested usage is to add the alias `tuna` to the `.bashrc/zshenv` file, by running (inside the base directory of the repository)
```sh
echo alias tuna=python3 $PWD/tuna.run >> ~/.bashrc
```

> For `zsh` users the command should be 
> ```sh
> echo alias tuna=python3 $PWD/tuna.run >> ~/.zshenv
> ```

This way the executable can be run by the `tuna` command

## Note about usage

The project, intended for use in LArSoft training for any  BDT is made of a set of python modules that can be controlled just by editing the `json` configuration file passed to the cli command `tuna`, is indipendent from any `LArSoft` external module. The data has to be passed as a `.txt` file format (common file format for BDT training) containing the values of the variables used to perform the cuts, for each event. The ouput model is passed as a `.xml` common in TMVA modeling and in `.pkl` common to store serialized machine learning models. 