import gzip
from collections import defaultdict

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

##################################popularity prediction################################
totalPurchases = 0
businessCount = defaultdict(int)
userCategories = {}
itemCategories = {}


for l in readGz("train.json.gz"):
    user, item, categories = l['reviewerID'], l['itemID'], l['categories']
    businessCount[item] += 1
    for i in categories:
        if user in userCategories:
            userCategories[user].add(tuple(i))
        else:
            userCategories[user] = set()
        if item in itemCategories:
            itemCategories[item].add(tuple(i))
        else:
            itemCategories[item] = set()
    totalPurchases += 1

mostPopular = [(businessCount[x], x) for x in businessCount]
mostPopular.sort()
mostPopular.reverse()

return1 = set()
count = 0
for ic, i in mostPopular:
  count += ic
  return1.add(i)
  if count > totalPurchases/4: break

popular = {}
for l in open("pairs_Purchase.txt"):
    u, i = l.strip().split('-')
    if i in return1:
        popular[(u,i)] = True
    else:
        popular[(u,i)] = False


predictions = open("predictions_similarss.txt", 'w')
for l in open("pairs_Purchase.txt"):
    if l.startswith("reviewerID"):
        predictions.write(l)
        continue
    u, i = l.strip().split('-')
    if i in itemCategories:
        c = itemCategories[i]
    else:
        c = set()
    if u in userCategories:
        d = userCategories[u]
    else:
        d = set()
    if len(c & d) != 0:
        predictions.write(u + '-' + i + ',' + str(1) + '\n')
    else:
        if popular[(u,i)]:
            predictions.write(u + '-' + i + ',' + str(1) + '\n')
        else:
            predictions.write(u + '-' + i + ',' + str(0) + '\n')
