
python -c "
import pickle
import numpy as np

sim = pickle.load(open('similar.pkl', 'rb'))
sim_compressed = sim.astype(np.float16)
pickle.dump(sim_compressed, open('similar.pkl', 'wb'))

import os
print('New size:', round(os.path.getsize('similar.pkl')/1024/1024, 2), 'MB')
"