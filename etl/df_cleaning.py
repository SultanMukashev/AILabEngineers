from elt_df import data1

df = data1()
#print(df)
df_dub = df.duplicated().sum()
print(df_dub) 

df = df.drop_duplicates()   #drop dublicates
nullval = df.isnull().sum()
print(nullval)     #
df = df.drop(columns=['capital.gain', 'capital.loss', 'fnlwgt', 'education', 'native.country'])

print(df)
df.to_csv("C:/Users/ersul/datatrain/raw/clean_.csv", index=False)
