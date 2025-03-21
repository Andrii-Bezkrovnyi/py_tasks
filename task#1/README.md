# Task about [Orderbook](https://docs.google.com/document/d/11pK8dFkLQiC8a-XR6GsW4lv0mAIZbsff/edit?usp=sharing&ouid=118366735974220802931&rtpof=true&sd=true)

### Wasted time: 2h 30m

#### Explaining my solution and classify it via big O notation

In the orderbook.py file, the code is implemented, 
where the complexity of adding for each order is O(n log n) due to the sorting of the list.
In the orderbook_optimized.py file, the code is implemented, 
where the complexity of adding and processing each order is O(log n) thanks to the use of heaps.
Thus, the second version (in orderbook_optimized.py) is more efficient in terms of execution time,
especially with a large number of orders, 
and its overall complexity can be expressed as O(log n) for adding an order and O(log n) 
for extracting orders.

Here are results of running  [orderbook.py](https://prnt.sc/RqaPQyVx7hQ3) and
[orderbook_optimized.py](https://prnt.sc/rsL19m38C-Ft)

## Code description

### Enter into task#1 directory

### Run the first implementation of Orderbook task (in Windows)
```bash
python orderbook.py
```
### Run the second implementation of Orderbook task (in Windows)
```bash
python orderbook_optimized.py
```
