import xalpha as xa

# zzhli = xa.indexinfo("159875")
zzhli = xa.fundinfo("000968")
print(zzhli.info())


zzyli = xa.indexinfo('SZ399812')

print(zzyli.price[zzyli.price['date']=='2018-08-01'])