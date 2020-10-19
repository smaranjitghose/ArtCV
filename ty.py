from tqdm import tqdm 

pbar = tqdm(total=100)
for i in range(10):
    pbar.update(10)
pbar.close()
