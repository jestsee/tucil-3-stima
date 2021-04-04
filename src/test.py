# Update, simplified sol thanks to @Aran-Fey's comments
import re
import math
xi =0.00044
x=0
# str
xs = str(xi)
print("xs=",xs,"\n")
# count zero
xz = len(re.search('\d+\.(0*)', xs).group(1))
print("xz=",xz)

if(xz>0):
    xi = xi * pow(10,xz)
else:
    x = str(xi)
    print("no")

print(xi)

def pengali(xi):
    xs = str(xi)
    xz = len(re.search('\d+\.(0*)', xs).group(1))
    if(xz>0):
        xi = xi * pow(10,xz+1)
    return str(xi)

print(pengali(0.0064))