import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
file_read=pd.read_excel("carlinregs.xlsx")
#print(file_read)
#print(file_read.columns)
#feature engineering
clean_file=file_read.dropna()
print(clean_file)
age_cols=clean_file["age"].tolist()
speed_cols=clean_file["speed"].tolist()
print(age_cols)
print(speed_cols)
#visualizing data before appling algo
#plt.scatter(age_cols,speed_cols)
#plt.show()
from scipy import stats
slope,intercept,r,p,std_error=stats.linregress(age_cols,speed_cols)
def myfile(x):
    return slope*x+intercept
#num=[age_cols]
model=list(map(myfile,age_cols))
#print(model)
#visualization after appling algo
plt.plot(model,age_cols)
plt.scatter(age_cols,speed_cols)
plt.show()






