# A surrogate model approach to optimal portfolios with heavy-tailed losses
A python implementation of my Master thesis with additional features. concerning surrogate modelling for optimizing heavy-tailed portfolios with general dependence structures.

This code is known to run with Python 3.5.2, if any of the dependencies or something else breaks with a version too old, let me know or feel free to fix it.


## Background
At the end of 2016 I finished my Master thesis in Mathematics and started writing a paper about my findings. The MATLAB code I used was not how I liked it to be, the features were quite narrow, the performance could be better, the numerical stability wasn't too great and I generally disliked the overall structure at the end. So to improve my Python and out of sheer interest for the topic I decided to do a rewrite.

The result is a faster, more stable and more extensive verison of my project. Features are added every now and then. If you're interested in the topic and want to work on the project let me know, I'm very open to that, let it be from an implementation point-of-view or if your research is related to heavy-tailed portfolio optimization and you see a benefit in working on it together. A reference implementation is given in 'samples/thesis.py'.


## Requirements
This code was tested on Ubuntu 16.04 with Python 3.5.2, I think in general Linux derivatives or older versions of Python 3 shouldn't be a problem. On Windows there might be an issue with the parallel execution, in that case check profiles one-by-one. If not, let me know.

## Usage
The project contains a make file, for convenience you can start there.
Use 
```
make install
```
to pull all dependencies via pip. For a reference run you can try
```
make run
```
Tests are not included yet.
