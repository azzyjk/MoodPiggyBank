import matplotlib.pyplot as plt
import pymysql
import time
rasDb = pymysql.connect(

    user = 'h2',
    passwd = 'Rjstw750',
    host = '218.144.108.84',
    database = 'NLP'

)

cursor = rasDb.cursor(pymysql.cursors.DictCursor)

sql = "SELECT * FROM feeling where print = 1;"
cursor.execute(sql)
result = cursor.fetchall()

y = [result[0]['mon'],result[0]['tue'],result[0]['wed'],result[0]['thr'],result[0]['fri'],result[0]['sat'],result[0]['sun']]
x=['mon','tue','wed','thr','fri','sat','sun']
plt.plot(x,y, marker = 'o')
plt.draw()
fig = plt.gcf()
fileName = './graph/' + str(time.time())[0:10] + result[0]['id'] + '.png'
fig.savefig(fileName, dpi=fig.dpi)
sql2 = "UPDATE feeling SET mon = 0, tue = 0, wed = 0, thr = 0, fri = 0, sat = 0, sun =0 where print = 1;"
cursor.execute(sql2)
rasDb.commit()
result = cursor.fetchall()
print(fileName[8:])
rasDb.close()
