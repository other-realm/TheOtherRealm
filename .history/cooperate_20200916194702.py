#%%
import numpy as np
from numpy.lib import recfunctions as rfn
import sympy as sym
import scipy as sp
import scipy.linalg as la
import scipy.stats as sts
import pandas as pd
import matplotlib.pyplot as plt
import os
from pprint import pprint
import uuid
import nbformat
import copy
import tensorflow as tf
from nbconvert.preprocessors import ExecutePreprocessor
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
# dmo_auto(status=True)
sym.init_printing(use_latex='mathjax', latex_mode='equation*')
# init_printing(pretty_print=True)
x, y, z, k, w=sym.symbols('x, y, z, k, w')
np.random.default_rng()
np.set_printoptions(suppress=True)
#%%
#Number of Invester Members
numOfInvest=5
#Number of Operative Members
numOfOper=5
#Number of Associate Members
numOfAssoc=5
#Number of Partner Members
numOfPart=5
#Total number of Members
numOfM=numOfAssoc+numOfInvest+numOfOper+numOfPart
numOfM
z=np.zeros(numOfM)
def calMemberVal(vals):
	totalV=0
	for sum in [v['value'] for v in vals.values()]:
		totalV+=sum
	return totalV
#People function
def popPeo(p,v,valCalculated=True,isAssoc=False):
	mem={}
	for id in range(p):
		mem[id]={
			#1 - people's value
			'value':np.array([sts.lognorm.rvs(.5)*v]) if valCalculated else np.array([v]),
			#2 - people's ability
			'ability':np.array([(1/(sts.lognorm.rvs(.99)*100))]),
			#3 - help needed
			'helpNeeded':np.array([(1/(sts.lognorm.rvs(.99)+1))*100]),
			#4 - people helped
			'bufIndex':0,
			'isAssoc':isAssoc
		}
	return mem
invest=popPeo(numOfInvest,200000)
oper=popPeo(numOfOper,75000)
assoc=popPeo(numOfAssoc,2500.0,False,True)
part=popPeo(numOfPart,75000)
members=[assoc,oper,part,invest]
def calTotalVal(mem):
	tV=0
	for i in range(len(mem)):
		tV+=calMemberVal(mem[i])
	return tV
totalValue=calTotalVal(members)
bufferFund=0
[v['value'] for v in invest.values()]
[v['value'] for v in oper.values()]
[v['isAssoc'] for v in assoc.values()]
[v['value'] for v in part.values()]
#%%
def calBuffer(mems,bf):
	for mem in mems:
		for p in mem:
			# pprint(mem[p]['isAssoc'])
			if(mem[p]['isAssoc']==False):
				bf=bf-mem[p]['bufIndex']
				mem[p]['bufIndex']=mem[p]['value']*.2
				mem[p]['value']-=mem[p]['bufIndex']
				mem[p]['value']+=bf/(len(mem)*len(mems))
				bf+=mem[p]['bufIndex']
			elif(mem[p]['value']<2500):
				mem[p]['value']+=bf-(2500-mem[p]['value'])
	# pprint(bf/(len(mem)*len(mems)))
	return bf
bufferFund=calBuffer(members,bufferFund)
bufferFund
# [v['value'] for v in invest.values()]
# [v['value'] for v in oper.values()]
# [v['value'] for v in assoc.values()]
# [v['value'] for v in part.values()]
#%%
# history[0]=peo
def runSim(t,p):
	cnt=0
	i=0
	j=1
	while j<t:
		calBuffer(p,bufferFund)
		# while i<len(p):
		# 	poorest=min(p, key=lambda v: p[v]['value'])
		# 	lowestW=p[poorest]['value']
		# 	# needMostHelp=max(p, key=lambda v: p[v]['helpNeeded'])
		# 	# print(poorest,lowest)
		# 	amountToTransfer=((p[i]['value']-lowestW)-(p[poorest]['helpNeeded']))
		# 	amountToTransfer-=((sts.lognorm.rvs(.99))*100)
		# 	p[poorest]['value']+=amountToTransfer
		# 	p[i]['value']-=amountToTransfer-(p[i]['ability'])
		# 	p[poorest]['helpIn'][i]+=1
		# 	p[i]['helpOut'][poorest]+=1
		# 	cnt+=1
		# 	i+=1;
		j+=1
		i=0
		# history[j]=peo
		cnt=0
	return calBuffer(p,bufferFund)
runSim(1000,members)
pprint(bufferFund)
[v['value'] for v in invest.values()]
[v['value'] for v in oper.values()]
[v['value'] for v in assoc.values()]
[v['value'] for v in part.values()]
#%%
[v['value'] for v in invest.values()]
# invest
# print(history)
# print('~~~~~~~~~~~~~~~~~~~~~~~~')
# print(history[999:1000])
# %%
history['value']
# %%
'''
			entropy=(1/(sts.lognorm.rvs(.99)+1))*.1
			if(p['value'][(cnt+1)%numOfM]<p['value'][(cnt)%numOfM]):
				p['value'][(cnt+1)%numOfM]+=(value*abs(ability))
				p['value'][cnt]-=(value*abs(ability))
			elif(p['value'][(cnt-1)%numOfM]<p['value'][(cnt)%numOfM]):
				p['value'][(cnt-1)%numOfM]+=(value*abs(ability))
				p['value'][cnt]-=(value*abs(ability))
			elif(p['value'][(cnt-2)%numOfM]<p['value'][(cnt)%numOfM]):
				p['value'][(cnt-1)%numOfM]+=abs(value*(ability))
				p['value'][cnt]-=(value*abs(ability))
			elif(p['value'][(cnt+2)%numOfM]<p['value'][(cnt)%numOfM]):
				p['value'][(cnt-1)%numOfM]+=(value*abs(ability))
				p['value'][cnt]-=(value*abs(ability))
			# print(p['value'][cnt],(value*(ability)))
			# print(p['value'][cnt],(value*(ability)))
'''
#%%
plt.hist(peo['value']*((sts.lognorm.rvs(.99)+1)*100),bins=200,  density=True)
# %%
plt.plot(history[990:1000][1][0][1])

# %%
historyA[999:1000]
# %%
s=pd.Series(history)
s #['value']
# plt.plot(x,s[x]['value'])
# %%
