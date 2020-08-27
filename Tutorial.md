# TUTORIAL - Using 'torque_drag'

## Index ##

* [1. Calculating drag force.](#1.-wellbores)
* [2. Calculating torque.](#2.-elevation)

Before any calculation, the wellbore trajectory and pipe properties need to be set. In the case you want to create a case but this data is not available, you should
create a new trajectory, otherwise just load your data using ```well_profile```

```
>>> import torque_drag
>>> import well_profile

>>> trajectory = well_profile.get(2000, profile='J', build_angle=45, kop=800, eob=1100)   # creating a new wellbore trajectory

# including pipe characteristics od_pipe: 4.5 in, id_pipe: 4 in, od_annular: 5 in and length_pipe: 1200 m
>>> well = torque_drag.create_well(well, 4.5, 4, 5, 1200)   
```

## 1. Drag Force

Force values are obtained in kN.

```
>>> result = torque_drag.calc(well2, case='all')    # case = "all", "lowering", "static" or "hoisting"

>>> result.plot()
```
![image](https://user-images.githubusercontent.com/52009346/91445832-ea206d00-e876-11ea-8825-cb41ad13a55c.png)

### 1.1. Lowering

```
>>> print(result.force['lowering'])   # print force profile for lowering case
[228.05418227295422, 217.41198807153359, 206.76979387011295, 196.1275996686923, 185.48540546727165, ...]
```

### 1.2. Static 

```
>>> print(result.force['static'])   # print force profile for static case
[242.85455301532767, 232.21235881390703, 221.57016461248637, 210.92797041106573, 200.2857762096451, ...]
```

### 1.3. Hoisting

```
>>> print(result.force['hoisting'])   # print force profile for hoisting case
[261.04100931233995, 250.39881511091932, 239.75662090949868, 229.11442670807804, 218.4722325066574, ...]
```


## 2. Torque

Torque values are obtained in kN*m

```
>>> result = torque_drag.calc(well2, case='all', torque_calc=True)    # case = "all", "lowering", "static" or "hoisting"

>>> result.plot(torque=True)
```
![image](https://user-images.githubusercontent.com/52009346/91445916-0c19ef80-e877-11ea-8b37-7f2a9a8dee13.png)

### 1.1. Lowering

```
>>> print(result.force['lowering'])   # print force profile for lowering case
[33.3008341703402, 33.3008341703402, 33.3008341703402, 33.3008341703402, ...]
```

### 1.2. Static 

```
>>> print(result.force['static'])   # print force profile for static case
[36.8943459227886, 36.8943459227886, 36.8943459227886, 36.8943459227886, ...]
```

### 1.3. Hoisting

```
>>> print(result.force['hoisting'])   # print force profile for hoisting case
[40.919526668277726, 40.919526668277726, 40.919526668277726, 40.919526668277726 ...]
```
