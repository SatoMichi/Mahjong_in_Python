import yaml
import os

def get_yaml_data(yaml_file):
    #open the file
    print("***getiing the yaml data***")
    file = open(yaml_file,'r',encoding="utf-8")
    file_data = file.read()
    file.close()

    #print(file_data)
    #print("type: ", type(file_data))

    print("***convert yaml data to dictionary or list")
    data = yaml.load(file_data,Loader=yaml.FullLoader)
    print(data['point'][0]['fanshu2'][0]['fushu50'][0]['defen'])
    #['point'][0]['fanshu2'][0]['fushu50'][0]['defen']
    print("type：", type(data))
    #return data




get_yaml_data("roncalculate.yml")    