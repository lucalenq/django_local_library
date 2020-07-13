import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from django.conf import settings

import os

class  DataTool():
    @staticmethod    
    def concatDataFrame(lstFiles):
        """
        Based on a LIST of filenames, it will concatenate all the datasets
        and return a single dataframe.
        """
        df_out = pd.DataFrame()
        for file in lstFiles:
            df = pd.read_csv(os.path.join(settings.STATICFILES_DIRS[0],file),float_precision=4)
            df_out = pd.concat([df_out,df], sort=True)

        df_out = df_out.reset_index()

        # Shuffle the examples
        df_out = df_out.reindex(np.random.permutation(df_out.index))

        return df_out 