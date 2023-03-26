[Spanish Version](https://github.com/fbarriosr/LHS/blob/master/README.ES.md)

## LHS

The program generates .cub files that can be viewed with the GaussView program or any other program capable of reading .cub files from the Gaussian Software. They correspond to the scalar fields of the local hypersoftness as well as its two components. For each molecular system, 5 files with the ".log" extension of said molecular system with N, N+1, N+2, N-1, N-2 electrons and .fchk files with N, are required as input files. N+p and N-q electrons, where p and q are the degree of degeneracy in LUMO and HOMO frontier orbitals, respectively. As with the Dualdescriptor and DDP programs, all such systems must have the same molecular geometry as the system with N electrons. This program can only be used on servers with the Linux operating system and always have the Gaussian programs and its complementary cubegen and cubman installed and running.

## Limitations

The program was developed using base python without any package, because the gaussian program was in a cluster without internet connection. Therefore, data structures such as lists, stacks, and trees, among others, were used.

## Requirements

Requires server with Gaussian cubegen and cubeman software.

## Installation

Copy the LHS folder to your server account.

```
$ scp LHS.tar user@server:/home/user/
```
Unzip the tar file.
```
$ tar -xvf LHS.tar
```
You can also create an alias in $ .bashrc. Use a some text editor.
```
$ vi ~.bashrc
```
Then add this last line:
```
alias lhs='python /home/user/LHS/lhs.py'
```

## Execution

You need to create a N+p.cub file, all 5 .log files and have all 3 .fchk files (Gaussian project), then run the program via python command

Command Line Version:
```
$ python /home/user/LHS/lhs.py
```
or just used the alias lhs:
```
$lhs
```
