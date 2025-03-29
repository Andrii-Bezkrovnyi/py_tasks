# Task about [Pinatas](https://docs.google.com/document/d/11pK8dFkLQiC8a-XR6GsW4lv0mAIZbsff/edit?usp=drive_link&ouid=118366735974220802931&rtpof=true&sd=true)

### Wasted time: 3h 20m

#### Explaining my code

This application calculates the maximum number of candies that can be obtained by smashing pinatas 
in an optimal order. Each pinata has a value, and when a pinata is smashed, 
the number of candies dropped is determined by multiplying the values of the adjacent pinatas. 
If there is no adjacent pinata (out of bounds), it is treated as 1.
Given an array of pinatas with values representing the number of candies inside each pinata, 
the task is to find the maximum amount of candies you can collect by smashing the pinatas 
in the optimal order.


## How this code works:
- The program uses dynamic programming with memoization to solve the problem.

- A recursive function simulates smashing each pinata and calculates the number of candies 
dropped, considering the boundaries and previously smashed pinatas.

- Memoization is used to store the results of subproblems to avoid redundant calculations 
and improve efficiency.


## How to run this code:
- Enter into task#7 directory

- Run the script via: (in Windows)
```bash
python pinatas.py <list_of_pinata_values>
```
### Exemple of running the code
```bash
python pinatas.py 12 1 12 2
```
``` Output is: 468 ```
