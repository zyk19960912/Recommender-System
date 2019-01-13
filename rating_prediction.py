import gzip
from collections import defaultdict
import random
import math

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

def getMSE(a,b1,b2,train_set):
    sum = 0
    for u,b in train_set:
        sum += math.pow(a + b1[u] + b2[b] - train_set[(u,b)], 2)
    MSE = 1/100000*sum
    return MSE

allRatings = []
trainRatings = {}
validationRatings = {}
train_users = defaultdict(list)
train_items = defaultdict(list)
total = 0
for l in readGz("train.json.gz"):
  user,business = l['reviewerID'],l['itemID']
  if total < 100000:
      train_users[user].append(business)
      train_items[business].append(user)
      trainRatings[(user,business)] = l['rating']
      allRatings.append(l['rating'])
  else:
      validationRatings[(user,business)] = l['rating']
  total += 1

########################init##########################
alpha = sum(allRatings)/100000
new_alpha = 0
betta_u = {}
new_betta_u = {}
betta_i = {}
new_betta_i = {}
lamda = 1
for p in train_users:
    betta_u[p] = 0
for q in train_items:
    betta_i[q] = 0
MSE = 0
newMSE = 0

while True:
    MSE = getMSE(alpha, betta_u, betta_i, trainRatings)
    temp = 0
    for u,b in trainRatings:
        temp += trainRatings[(u,b)] - betta_u[u] - betta_i[b]
    new_alpha = temp / 100000
    for u in betta_u:
        temp = 0
        for b in train_users[u]:
            temp += trainRatings[(u,b)] - (alpha + betta_i[b])
        print(u,temp)
        new_betta_u[u] = temp/(lamda + len(train_users[u]))

    for b in betta_i:
        temp = 0
        for u in train_items[b]:
            temp += trainRatings[(u,b)] - (alpha + betta_u[u])
        new_betta_i[b] = temp/(lamda + len(train_items[b]))
    newMSE = getMSE(new_alpha, new_betta_u, new_betta_i, trainRatings)
    print(MSE,newMSE)
    if abs(MSE - newMSE) < 0.0001:
        break
    else:
        alpha = new_alpha
        betta_u = new_betta_u
        betta_i = new_betta_i

    # ##############################fix alpha and betta_i with your updated betta_u##################################
    # MSE = getMSE(alpha, betta_u, betta_i, trainRatings)
    # for u in betta_u:
    #     temp = 0
    #     for b in train_users[u]:
    #         temp += trainRatings[(u, b)] - (alpha + betta_i[b])
    #     new_betta_u[u] = temp / (lamda + len(train_users[u]))
    # temp = 0
    # for u, b in trainRatings:
    #     temp += trainRatings[(u, b)] - new_betta_u[u] - betta_i[b]
    # new_alpha = temp / 100000
    # for b in betta_i:
    #     temp = 0
    #     for u in train_items[b]:
    #         temp += trainRatings[(u, b)] - (alpha + new_betta_u[u])
    #     new_betta_i[b] = temp / (lamda + len(train_items[b]))
    #
    # newMSE = getMSE(new_alpha, new_betta_u, new_betta_i, trainRatings)
    # print(MSE, newMSE)
    # if MSE - newMSE < 0.0000001:
    #     break
    # else:
    #     alpha = new_alpha
    #     betta_u = new_betta_u
    #     betta_i = new_betta_i
    # ##############################fix alpha and betta_u in your updated betta_i##################################
    # MSE = getMSE(alpha, betta_u, betta_i, trainRatings)
    # for b in betta_i:
    #     temp = 0
    #     for u in train_items[b]:
    #         temp += trainRatings[(u, b)] - (alpha + betta_u[u])
    #     new_betta_i[b] = temp / (lamda + len(train_items[b]))
    # for u in betta_u:
    #     temp = 0
    #     for b in train_users[u]:
    #         temp += trainRatings[(u, b)] - (alpha + new_betta_i[b])
    #     new_betta_u[u] = temp / (lamda + len(train_users[u]))
    # temp = 0
    # for u, b in trainRatings:
    #     temp += trainRatings[(u, b)] - betta_u[u] - new_betta_i[b]
    # new_alpha = temp / 100000


    # newMSE = getMSE(new_alpha, new_betta_u, new_betta_i, trainRatings)
    # print(MSE, newMSE)
    # if MSE - newMSE < 0.0000001:
    #     break
    # else:
    #     alpha = new_alpha
    #     betta_u = new_betta_u
    #     betta_i = new_betta_i

# alpha = new_alpha
# betta_u = new_betta_u
# betta_i = new_betta_i


for u,b in validationRatings:
    if u not in train_users:
        betta_u[u] = 0
    if b not in train_items:
        betta_i[b] = 0
MSE_validation = getMSE(alpha,betta_u,betta_i,validationRatings)
print(MSE_validation)
