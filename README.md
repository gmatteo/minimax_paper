## QP gaps with minimax meshes

Convergence of the QP direct gaps (eV) at Gamma and X with the number of points in the minimax mesh.
The color of each point is proportional to the duality error `Max_{ij} |CT CT^{-1} - I|`.

![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/Bn.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/C.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/GaAs.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/LiF.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/MgO.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/Si.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_GWR/SiC.png)


## RPA energy with minimax meshes

Convergence of the RPA energy (eV) with the number of points in the minimax mesh.
The color of each point is proportional to the duality error `Max_{ij} |CT CT^{-1} - I|`.
Note that the results obtained with ntau == 6 are not shown.

**FIXME**
Note that I'm rescaling the results obtained with the last 5 meshes (ntau 26-34) by
the infamous factor 4 (spin and integration range).
Very likely the weights for the last 5 meshes have been generated using a different convention.
This is what I get for LiF if I don't rescale

```
    ntau  rpa_ec_ev  ft_max_err_t2w_cos  ft_max_err_w2t_cos  ft_max_err_t2w_sin  cosft_duality_error
0      6 -14.499451        1.933901e-03        1.353624e-03        4.325153e-02         1.309390e-03
1      8 -14.499090        4.909689e-04        1.179800e-04        9.218434e-03         2.711183e-03
2     10 -14.499092        5.332045e-05        3.952615e-05        1.896179e-03         1.762042e-03
3     12 -14.499092        2.246161e-05        2.504123e-06        3.800066e-04         8.050877e-03
4     14 -14.499092        4.629865e-06        4.686459e-07        7.477280e-05         1.314336e-02
5     16 -14.499092        9.073634e-07        8.641273e-08        1.448701e-05         2.097865e-02
6     18 -14.499093        6.110221e-07        1.125080e-07        2.764762e-06         3.113177e+00
7     20 -14.499094        1.671891e-06        1.810501e-07        2.255550e-06         5.147856e-01
8     22 -14.499093        4.704446e-08        3.180201e-08        1.027178e-07         1.528265e+02
9     24 -14.499093        1.962311e-08        1.929468e-08        1.914650e-07         5.472928e+07
10    26  -3.624773        7.389984e-09        8.245343e-09        7.419598e-08         1.602566e+06
11    28  -3.624773        1.088852e-08        8.016416e-09        1.227601e-07         1.232216e+06
12    30  -3.624773        1.109270e-08        7.893361e-09        1.227774e-07         1.206735e+06
13    32  -3.624773        1.037138e-08        9.264811e-09        1.311225e-07         1.986793e+06
14    34  -3.624773        1.325711e-08        1.351992e-08        1.575436e-07         2.962972e+06
```


![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/Bn.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/C.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/GaAs.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/LiF.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/MgO.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/Si.png)
![alt text](https://github.com/gmatteo/minimax_paper/blob/main/DATA_RPA/SiC.png)
