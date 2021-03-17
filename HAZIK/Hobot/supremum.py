def calculate_diff_series(lambda_parameter, RANGE):
    lam=[]
    import pandas as pd
    import numpy as np
    for i in RANGE:
        df=pd.DataFrame()
        df["poi"]=np.random.poisson(lambda_parameter,i)
        df["binom"]=np.random.binomial(10,(lambda_parameter/10),i)
        x=df["binom"].value_counts(normalize=True).sort_index()
        y=df["poi"].value_counts(normalize=True).sort_index()
        lam.append(max(abs(y-x)))
    return lam
