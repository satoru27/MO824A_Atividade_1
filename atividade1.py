#import gurobipy as gp
#from gurobipy import GRB
import random
import numpy as np
from gurobipy import Model,GRB

#J = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
J = 50 # nº clientes
F = random.randrange(J, 2*J +1) # nº fabricas produtoras de papel
L = random.randrange(5, 10+1) # nº maquinas
M = random.randrange(5, 10+1) # nº de tipos de materias primas
P = random.randrange(5, 10+1) # nº de tipos de papel

print("-"*30)
print(f"J={J}\nF={F}\nL={L}\nM={M}\nP={P}")


D = np.zeros((J,P)) # D[j,p] = demanda do cliente j em unidades de papel do tipo p

r = np.zeros((M,P,L)) # r[m,p,l] = unidades de matéria-prima m necessárias para produzir
                      # uma unidade de papel do tipo p na máquina l

R = np.zeros((M,F)) # R[m,f] = unidades de matéria-prima m disponíveis na fábrica f

C = np.zeros((L,F)) # C[l,f] = capacidade disponível de produção, em unidades de papel, 
                    # da máquina l na fábrica f

p = np.zeros((P,L,F)) # p[p,l,f] = custo unitário de produção do papel tipo p utilizando
                      # a máquina l na fábrica f

t = np.zeros((P,F,J)) # t[p,f,j] = custo unitário de transporte do papel tipo p partindo
                      # da fábrica f até o cliente j
print("-"*30)
print(f"D={D.shape}\nr={r.shape}\nR={R.shape}\nC={C.shape}\np={p.shape}\nt={t.shape}")

for j in range(J):
    for k in range(P):
        #D[j,k] = random.randrange(10, 100+1)
        D[j,k] = random.randrange(10, 20+1)

for m in range(M):
    for k in range(P):
        for l in range(L):
            #r[m,k,l] = random.randrange(1, 10+1)
            r[m,k,l] = random.randrange(1, 5+1)

for m in range(M):
    for f in range(F):
        #R[m,f] = random.randrange(100, 1000+1)
        R[m,f] = random.randrange(800, 1000+1)

for l in range(L):
    for f in range(F):
            #C[l,f]= random.randrange(10, 100+1)
            C[l,f]= random.randrange(80, 100+1)

for k in range(P):
    for l in range(L):
        for f in range(F):
            p[k,l,f]= random.randrange(10, 100+1)

for k in range(P):
    for f in range(F):
        for j in range(J):
            t[k,f,j] = random.randrange(10, 20+1)


#print("-"*30)
#print(f"D={D}\nr={r}\nR={R}\nC={C}\np={p}\nt={t}")


#inicio modelagem

mdl = Model('papel')
x = mdl.addMVar(p.shape, vtype=GRB.INTEGER)
y = mdl.addMVar(t.shape, vtype=GRB.INTEGER)
mdl.modelSense = GRB.MINIMIZE
mdl.setParam('TimeLimit', 30*60)


mdl.setObjective(sum(p[k,l,f] * x[k,l,f]
                         for k in range(P) for l in range(L) for f in range(F))
                + sum(t[k,f,j] * y[k,f,j]
                          for k in range(P) for l in range(L) for j in range(J)))

mdl.addConstrs(sum(x[k,l,f] for l in range(L) for f in range(F)) >= sum(D[j,k] for j in range(J)) for k in range(P))

mdl.addConstrs(sum(y[k,f,j] for f in range(F)) >= D[j,k] for k in range(P) for j in range(J))

mdl.addConstrs(sum(x[k,l,f] for k in range(P)) <= C[l,f] for l in range(L) for f in range(F))

mdl.addConstrs(sum(x[k,l,f] * r[m,k,l] for k in range(P) for l in range(L)) <= R[m,f] for f in range(F) for m in range(M))

mdl.optimize()