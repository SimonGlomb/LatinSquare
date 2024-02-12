int: n;
array[1..n,1..n] of var 1..n: a;
include "alldifferent.mzn";
constraint forall(i in 1..n) (
    alldifferent(j in 1..n) (a[i,j]) /\
    alldifferent(j in 1..n) (a[j,i])    
);
solve satisfy;
