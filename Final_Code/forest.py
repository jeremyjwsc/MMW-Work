import matplotlib.pyplot as plt
import matplotlib.figure as fig
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random 

random.seed(None)
#%% function definition cell

#diferencia de alturas
def dh ( x, ii, jj):
    temp=0
    i=ii
    j=jj
    sp=(ii+1)%ntrees
    sm=(ii-1)%ntrees
    tp=(jj+1)%ntrees
    tm=(jj-1)%ntrees
    y=[]
    y.append(x[i][j]-x[sp][j])
    y.append(x[i][j]-x[sm][j])
    y.append(x[i][j]-x[i][tp])
    y.append(x[i][j]-x[i][tm])
    y.append(x[i][j]-x[sp][tp])
    y.append(x[i][j]-x[sm][tm])
    y.append(x[i][j]-x[sm][tp])
    y.append(x[i][j]-x[sp][tm])
    for i in y:
        temp=temp+np.absolute(i)+i*i*i
    return temp


def dh1(x ,ii ,jj ):
    temp=x[ii][jj]
    i=ii
    j=jj
    sp=(ii+1)%ntrees
    sm=(ii-1)%ntrees
    tp=(jj+1)%ntrees
    tm=(jj-1)%ntrees
    if temp < x[sp][j]:
        temp=x[sp][j]
    if temp < x[sm][j]:
        temp=x[sm][j]
    if temp < x[i][tp]:
        temp=x[i][tp]
    if temp < x[i][tm]:
        temp=x[i][tm]
    if temp < x[sp][tp]:
        temp=x[sp][tp]
    if temp < x[sm][tm]:
        temp= x[sm][tm]
    if temp < x[sm][tp]:
        temp= x[sm][tp]
    if temp < x[sp][tm]:
        temp= x[sp][tm]
    return ((x[i][j]-temp)**2-(temp-x[i][j])**3)/((x[i][j]-temp)**2+np.absolute((temp-x[i][j]))**3+1)
    

def distribution (x,n_dif_sizes,ntrees,max_size):
    #each position represents an interval of sizes that we will assume they're equal
    #it could be interpreted as a precision.
    y=np.linspace(0.0,max_size,num=n_dif_sizes+1) 
    z=np.zeros(n_dif_sizes+1)
    for i in range(ntrees):
        for j in range (ntrees):
            for s in range (n_dif_sizes):
                    if (x[i][j]>y[s])and(x[i][j]<y[s+1]):
                        z[s]=z[s]+1
            if x[i][j]>max_size:
                z[n_dif_sizes]=z[n_dif_sizes]+1
           # if x[i][j]==0:
               # z[0]=z[0]+1
    return z/(ntrees**2)

def lifetime (age):
     #probabildiad de morir una vez superada la esperanza de vida
     #x: age 
     return 1/age #x**2/(x**2+lifetime**2)
   
      
def newborn():
    
    #probabilidad de nacer. Depende de la cantidad de arboles circudnantes. LA calidad del suelo 
    #y no sé si hacerla acumulativa para asegurarnos que despues de MIN steps crezca un arbol nuevo.
    #no acumulativa. Siempre es igual 
    
    return 0.4

Rl=lambda l,beta: 1;#1-pow(l,beta);

Rq=lambda q, alpha: (q-0.1)*alpha;
    
def g_ij (x,p,q,l,apha,beta,i,j):
    
    return p*((1+( Rl(l,beta)+Rq(q,alpha) ))/3+dh1(x,i,j)*1/2)

#%%initializacion cell

# general tree parameters
max_age=100
max_size=100
min_size=0.000001
max_warning=4
life_time=100#esperanza de vida de un arbol en años 

#model parameters
l=0.5
alpha=0.5
beta=0.4
p=1
soil_coef=10

#simulation parameters
ntrees=100
iterations=201#lifetime of our forest
dif_sizes=10#how many differents sizes we accept
dead_counter=0
newborn_counter=0

#arrays initiallization
warnings=np.zeros((ntrees,ntrees))

forest=np.random.rand(ntrees,ntrees)*0.00001
nforest=forest

soil=np.random.rand(ntrees,ntrees)
nsoil=soil

#age=np.random.randint(0,max_age+1,(ntrees,ntrees))
age=np.zeros((ntrees,ntrees))
final_dist=[]

#%%loop cell

for z in range (iterations):
    for i in range(ntrees):
        for j in range(ntrees):
            
            if forest[i][j]==0:
                if random.uniform(0.0,1.0)< newborn():
                    nforest[i][j]=min_size
                    newborn_counter=newborn_counter+1
                    
            temp=g_ij(forest,p,soil[i][j],l,alpha,beta,i,j)
            if temp<0:
                warnings[i][j]=warnings[i][j]+1
                temp=0
            nforest[i][j]=forest[i][j]+temp*p
            nsoil[i][j]=(1-temp/soil_coef)*soil[i][j]
            
            if warnings[i][j]==max_warning:
                nforest[i][j]=0
                age[i][j]=0
                nsoil[i][j]=1
                dead_counter=dead_counter+1
                
            
            if nforest[i][j]>0: 
                age[i][j]=age[i][j]+1
                
            #if age[i][j]>life_time: 
            if random.uniform(0.0,1.0)< lifetime(life_time):
                nforest[i][j]=0
                age[i][j]=0
                nsoil[i][j]=1 #maxima calidad 
                dead_counter=dead_counter+1
                    
    forest=nforest
    soil=nsoil
    
    
final_dist=distribution(forest,dif_sizes,ntrees,max_size)
    

#%% single plot. method 1
    
fig = plt.figure(figsize=(5,5), dpi=100 )


ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,4) 
ax1.set_title('Forest simulation')
ax2.set_title('Relative size frequency')
ax2.set_xlabel('Size intervals')
ax2.set_ylabel('Frequency')
ax2.set_ylim((0.0,1.0))
a = np.zeros((ntrees,ntrees))
x=np.linspace(0,1,num=dif_sizes+1)

# cuenta las divisiones que hay y las caracteriza auqnque el valor
# no tiene ningun significado, simplemente tenemos dif_sizes valores. Sirve, pero, para espaciar 
#el eje y 
array = ax1.imshow(forest , animated=False, cmap='plasma', vmin=0,vmax=max_size,  
                   extent=[0,ntrees,ntrees,0], aspect=1, origin= 'upper')

hist = ax2.bar(x,final_dist, color='red', align='center' , width=0.05, bottom=0)

xdiv=np.linspace(0.0,max_size, num=dif_sizes+1)
for i in range(dif_sizes+1):
    xdiv[i]=round(xdiv[i],3)
xlabels=[]
for i in range (dif_sizes):
    temp=str(xdiv[i])+'-'+str(xdiv[i+1])
    xlabels.append(temp)
xlabels.append('>100')


plt.colorbar(array,ax=ax1)
plt.xticks(x,xlabels,rotation='vertical')



    
#%% method 2.initiallization cell


# general tree parameters
max_age=10
max_size=100
min_size=1
max_warning=3
life_time=57#esperanza de vida de un arbol en años 

#model parameters
l=0.5
alpha=3
beta=0.4
p=1
soil_coef=10
forest_coef=100#max size

# simulation parameters
ntrees=100
iterations=200#lifetime of our forest
dif_sizes=10#how many differents sizes we accept
dead_counter=np.zeros(iterations+2)
newborn_counter=np.zeros(iterations+2)

#arrays initiallization
warnings=np.zeros((ntrees,ntrees))

forest=np.random.rand(ntrees,ntrees)*min_size
nforest=forest
total_forest=np.zeros((iterations+1,ntrees,ntrees))

soil=np.random.rand(ntrees,ntrees)
nsoil=np.random.rand(ntrees,ntrees)
total_soil=np.zeros((iterations+1,ntrees,ntrees))

#age=np.random.randint(0,max_age+1,(ntrees,ntrees))
age=np.zeros((ntrees,ntrees))
total_dist=[]


#%% method 2. loop cell


total_forest[0]=forest
total_soil[0]=soil
total_dist.append(distribution(forest,dif_sizes,ntrees,max_size))

for z in range (iterations):
    for i in range(ntrees):
        for j in range(ntrees):
            if forest[i][j]==0:
                if random.uniform(0.0,1.0)< newborn():
                    nforest[i][j]=min_size
                    newborn_counter[z]=newborn_counter[z]+1
                    
            temp=g_ij(forest,p,soil[i][j],l,alpha,beta,i,j)
            if temp<0:
                warnings[i][j]=warnings[i][j]+1
                temp=0
                temp=temp+random.uniform(0.1,0.1)
            if forest[i][j]!=0:   
                nforest[i][j]=forest[i][j]+temp*p
                nsoil[i][j]=(1-temp/soil_coef-forest[i][j]/forest_coef)*soil[i][j]
                
            if warnings[i][j]==max_warning:
                nforest[i][j]=0
                age[i][j]=0
                nsoil[i][j]=1
                dead_counter[z]=dead_counter[z]+1
                
            if nforest[i][j]>0: 
                age[i][j]=age[i][j]+1
          
            if random.uniform(0.0,1.0)< lifetime(life_time):
                nforest[i][j]=0
                age[i][j]=0
                nsoil[i][j]=1 #maxima calidad 
                if z!=0:
                    dead_counter[z]=dead_counter[z]+1
    dead_counter[z+1]=dead_counter[z]
    newborn_counter[z+1]=newborn_counter[z]
    forest=nforest
    soil=nsoil
    total_forest[z+1]=forest
    total_soil[z+1]=soil
    total_dist.append(distribution(forest,dif_sizes,ntrees,max_size))



#%% animation 2

fig = plt.figure(figsize=(5,5), dpi=100 )


ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,4) 
ax1.set_title('Forest simulation')
ax2.set_title('Relative size frequency')
ax2.set_xlabel('Size intervals')
ax2.set_ylabel('Frequency')
a = np.zeros((ntrees,ntrees))
x=np.linspace(0,1,num=dif_sizes+1)
y=np.linspace(0,0.6,num=dif_sizes+1)

# cuenta las divisiones que hay y las caracteriza auqnque el valor
# no tiene ningun significado, simplemente tenemos dif_sizes valores. Sirve, pero, para espaciar 
#el eje y 
array = ax1.imshow(a , animated=True, cmap='plasma', vmin=0,vmax=max_size,  
                   extent=[0,ntrees,ntrees,0], aspect=1, origin= 'upper')

hist = ax2.bar(x,y, color='red', align='center' , width=0.05, bottom=0)

xdiv=np.linspace(0.0,max_size, num=dif_sizes+1)
for i in range(dif_sizes+1):
    xdiv[i]=round(xdiv[i],3)
xlabels=[]
for i in range (dif_sizes):
    temp=str(xdiv[i])+'-'+str(xdiv[i+1])
    xlabels.append(temp)
xlabels.append('>100')


plt.colorbar(array,ax=ax1)
plt.xticks(x,xlabels,rotation='vertical')
gen_count=ax2.text(0.1,1.4,'')#cada 100 años pongamos, es una generacion
time_count=ax2.text(0.1,1.3,'') # cada loop es una año/dia
dead_count=ax2.text(0.1,1.2,'')
newborn_count=ax2.text(0.1,1.1,'')

def init ():
    array.set_array(a)
    for i,b in enumerate(hist):
        b.set_height([])
    gen_count.set_text('')
    time_count.set_text('')
    dead_count.set_text('')
    newborn_count.set_text('')
 
    
def animation(s):
    time_count.set_text('Iteration (year):%d'%s)
    gen=(s / life_time)+1
    gen_count.set_text('Generation: %d' % gen)
    dead_count.set_text('Dead counter: %d' %dead_counter[s])
    newborn_count.set_text('Newborn counter:%d' %newborn_counter[s])
    array.set_array(total_forest[s])
    for i,b in enumerate (hist):
        b.set_height(total_dist[s][i])#s es la posicion en la lista, i es la posicion en el vector
    
    
    
anim = FuncAnimation(fig,animation,init_func=init, interval=75, frames=iterations+1) 

    
    

#anim.save('/Users/jeremy/Desktop/WMM/project/forest_simulation/forest_evolution.html', fps=15, extra_args=['-vcodec', 'libx264'])
    
    
    