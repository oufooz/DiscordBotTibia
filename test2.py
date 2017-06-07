hunted_list = ['mark','zak','tim']
try:
    file_object = open("hunted.txt",'w')
except FileNotFoundError:
        msg = 'couldnt find the file'
        print(msg)
else:
    for i in hunted_list:
        print(i , file= file_object)

