@echo off
echo source "I,J/*" > %1_ncont_parameters.txt
echo target "A,B,C/**" >> %1_ncont_parameters.txt
echo mindist 0.0  >> %1_ncont_parameters.txt
echo maxdist 4.01 >> %1_ncont_parameters.txt
echo cells OFF >> %1_ncont_parameters.txt
echo END >> %1_ncont_parameters.txt

ncont XYZIN "%1" < %1_ncont_parameters.txt
ncont XYZIN "%1" < %1_ncont_parameters.txt > %1_ncont_output.txt

del %1_ncont_parameters.txt

python v0.1.py %1_ncont_output.txt