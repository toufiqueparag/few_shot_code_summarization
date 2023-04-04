#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:40:18 2022

@author: toufiqueahmed
"""

import os
import openai
from time import sleep
import json
import argparse



def process(data_folder, key):

    openai.api_key = key
    data = []
    for line in open(data_folder+'/test.jsonl', 'r',encoding="utf-8"):
        data.append(json.loads(line))
    
    
    with open(data_folder+"/train_10.txt","r",encoding="utf-8") as f:
        inputs=f.read()
    
    
    fx=open(data_folder+"/result_10.output","w",encoding="utf-8")
    
    
    for i in range(0,len(data)):
        print(i)
        p=data[i]["code_tokens"] 
        x=""
        y=""
        for w in p:
            x=x+w+" " 
        y="<s>"   
        
        inputs1=inputs+x+"\t"+y
        tokens=inputs1.split()
        
        if len(tokens)>3000:
            tokens=tokens[200:]
        
        inputs1=""   
        for w in tokens:
            inputs1=inputs1+w+" "
             
        print("\n\n####################################\n\n")
        response = openai.Completion.create(
          engine="code-davinci-002",
          prompt=inputs1,
          temperature=0,
          max_tokens=250,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        print(response.choices[0].text)
        mout=response.choices[0].text
        mout=mout.split("</s>")[0].strip()
        fx.write(str(i)+"\t"+mout+"\n")
        print("\n\n####################################\n\n")
        print("going_sleep")
        sleep(10)
        print("wakeup")
    fx.close()    
    
    
def main():
    parser = argparse.ArgumentParser()
    ## Required parameters  
    parser.add_argument("--open_key", default=None, type=str, required=True,
                        help="Enter API key")
    parser.add_argument("--data_folder", default=None, type=str, required=True,
                        help="data folder path ")     
   
    args = parser.parse_args()
    process(args.data_folder,args.open_key)
    
main()    
