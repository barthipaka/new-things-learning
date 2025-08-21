data=['kohli','dhoni','rohit','hardik','jadeja','kohli','kohli','kohli','dhoni']


my_dict = {}

for i in range(0, len(data)):
    temp=my_dict.get(data[i]) #value is not here in my_dict variable returns None
    if temp is None:
        my_dict[data[i]] = 1 #created the player and added the key value pairs
    else:
        my_dict[data[i]] = temp + 1 #incremented the value of the player by 1


for playerer_name,vote in my_dict.items():
    print(playerer_name, ":", vote)