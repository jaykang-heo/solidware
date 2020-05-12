import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tour_cap_nat.tsv', sep='\t')

for col in df.columns[1:]:
    if '2016' not in col:
        del df[col]

col = df.columns[0]
n_col = col.split(',')
df_cols = df[col].str.split(',')

df[n_col] = df[col].str.split(',', expand=True)
del df[df.columns[0]]
# include
df = df[df['accommod'].str.contains('BEDPL')]
df = df[df['nace_r2'].str.contains('I551')]
df = df[df['unit'].str.contains('NR')]
# exclude
df = df[~df['nace_r2'].str.contains('I553')]
df = df[~df[df.columns[0]].str.contains(':')]
df = df[~df[df.columns[-1]].str.contains('EA')]
df = df[~df[df.columns[-1]].str.contains('EU27_2007')]
df = df[~df[df.columns[-1]].str.contains('EU27_2020')]
df = df[~df[df.columns[-1]].str.contains('EU28')]

df1 = pd.read_csv('tin00083.tsv', sep='\t')
for col in df1.columns[1:]:
    if '2016' not in col:
        del df1[col]
col = df1.columns[0]
n_col = col.split(',')
df_cols = df1[col].str.split(',')

df1[n_col] = df1[col].str.split(',', expand=True)
del df1[df1.columns[0]]
# include
df1 = df1[df1[df1.columns[2]].str.contains('IND_TOTAL')]
# exclude
df1 = df1[~df1[df1.columns[0]].str.contains('u')]
df1 = df1[~df1[df1.columns[0]].str.contains('bu')]
df1 = df1[~df1[df1.columns[0]].str.contains(':')]
df1 = df1[~df1[df1.columns[-1]].str.contains('EA')]
df1 = df1[~df1[df1.columns[-1]].str.contains('EU27_2007')]
df1 = df1[~df1[df1.columns[-1]].str.contains('EU27_2020')]
df1 = df1[~df1[df1.columns[-1]].str.contains('EU28')]

temp = {}
for index, row in df1.iterrows():
    if row[-1] not in temp:
        if 'b' in row[0]:
            row[0] = row[0].strip('b')
        temp[row[-1]] = [row[0]]
for index, row in df.iterrows():
    if row[-1] in temp:
        temp[row[-1]].append(row[0])

res = pd.DataFrame({
    'Country Code': [],
    'Percentage of individuals online': [],
    'Number of Bed-places': []
})

country_code = []
online_percent = []
no_bed = []
for i in temp.keys():
    country_code.append(i)
    online_percent.append(int(temp[i][0]))
    no_bed.append(int(temp[i][1]))

res['Country Code'] = country_code
res['Percentage of individuals online'] = online_percent
res['Number of Bed-places'] = no_bed


print(res)
res.plot(x='Country Code', y='Percentage of individuals online', kind='bar')
res.plot(x='Country Code', y='Number of Bed-places', kind='bar')
plt.show()
