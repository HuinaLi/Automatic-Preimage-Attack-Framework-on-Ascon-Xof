# Automatic-Preimage-Attack-Framework-on-Ascon-Using-a-Linearize-and-Guess-Approach

Contents of the files:
1. structure_search: the code to generate SAT models searching for n-1 round structure used in n-round preimage attack on Ascon-Xof.


Note that please first set up your SageMath environment and then run our python file.


How to set up SageMath environment?

First step: [conda setup]
1. install miniconda: https://docs.conda.io/en/latest/miniconda.html
```bash Miniconda3-latest-Linux-x86_64.sh```
Note: if you have error "UnicodeDecodeError: ‘ascii‘ codec can‘t decode byte", just type command:
```export LC_ALL=C.UTF-8```
```source ~/.bashrc```
delete previous environment: </br>
```conda env remove -n name```

Second Step: [sagemath install](https://doc.sagemath.org/html/en/installation/conda.html)
1. set conda-forge: </br>```conda config --add channels conda-forge```
2. change to restrict mode: </br>```conda config --set channel_priority strict```
3. create a conda environment named `sage`: </br>```conda create -n sage sage python=3.9```
4. note: you can change the environment name as you like</br>```conda create -n {name} sage python=3.9```
