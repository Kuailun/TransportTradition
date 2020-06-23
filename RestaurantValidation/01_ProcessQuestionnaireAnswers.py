# -*- coding: utf-8 -*-
# @File       : 01_ProcessQuestionnaireAnswers.py
# @Author     : Yuchen Chai
# @Date       : 2020-05-26 22:28
# @Description:

import pandas as pd
import os
df_restaurant = pd.read_csv("Zhengzhou_POIs.csv")

def search_restaurant(p_keyword):
    try:
        df_ret = df_restaurant[df_restaurant.shopName.str.contains(p_keyword)]
    except:
        return 0
    return len(df_ret)

def process_potential_restaurant_names():
    dirs = os.listdir("restaurant_name")
    restaurant_names = []
    for item in dirs:
        df = pd.read_csv("restaurant_name/" + item)
        df = df[df.rest_name!="(空)"]
        df = df[df.rest_name!="(跳过)"]
        for i, d in df.iterrows():
            if d['rest_name'] not in restaurant_names:
                restaurant_names.append(d['rest_name'])
                pass
            pass
        pass
    return restaurant_names

def fetch_potential_restaurant_numbers(p_list):
    restaurant_info = []
    index = 0
    for item in p_list:
        print(index)
        index += 1
        restaurant_info.append({"origin_name":item,"result_nums":search_restaurant(item),"final_name":""})
        pass
    return restaurant_info

if __name__ == "__main__":
    # Step01 process potential restaurant names
    restaurant_names = process_potential_restaurant_names()

    # Step02 find the result number for each restaurant name
    restaurant_info = fetch_potential_restaurant_numbers(restaurant_names)

    df = pd.DataFrame(restaurant_info,columns=['origin_name','result_nums','final_name'])
    df.to_csv("restaurant_dict.csv")