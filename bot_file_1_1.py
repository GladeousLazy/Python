#This is a bot file with 2 intents
#1: where we filter data from a data frame
#2: We write back to a database

import os
import requests
from pprint import PrettyPrinter
import json
from virtassnt.nodes import *
from virtassnt.core import Node, Message
from virtassnt.graph import Graph
import pandas as pd #Navitesh - imported this library to create data frame
import pymysql as mdb #This library is used to import data from mysql database instance. This is applicable for python version 3.6 and above

import sys
import mysql.connector #This is a lbrary e need to connect to the databases. I need to research on this one later.

#Navitesh - Created a multidimension array to be treated as a table.

#df = pd.DataFrame([[2019,"jan","email","florida",626895],[2018,"jan","email","florida",843389],[2019,"feb","email","florida",272553],[2018,"feb","email","florida",259378],[2019,"mar","email","florida",454539],[2018,"mar","email","florida",938111],[2019,"apr","email","florida",47283],[2018,"apr","email","florida",65196],[2019,"may","email","florida",897444],[2018,"may","email","florida",695585],[2019,"jun","email","florida",737076],[2018,"jun","email","florida",28187],[2019,"jul","email","florida",810185],[2018,"jul","email","florida",923495],[2019,"aug","email","florida",427067],[2018,"aug","email","florida",774426],[2019,"sep","email","florida",252908],[2018,"sep","email","florida",86198],[2019,"oct","email","florida",58166],[2018,"oct","email","florida",373691],[2019,"nov","email","florida",325952],[2018,"nov","email","florida",306977],[2019,"dec","email","florida",273710],[2018,"dec","email","florida",525628]], columns = ["year","month","type","account","sales"])


################----------------------DB Code-----------------------################

try:
        con = mdb.connect ('localhost','root','root','trial')
        cur = con.cursor()
        cur.execute('use trial')
        cur.execute('Select * from trial')

        ver = cur.fetchall()
        df = pd.DataFrame(list(ver))
finally:
        if con:
                con.close()

################------------------End of DB Code--------------------################


################---------------------------Note---------------------################
"""
1 - The way this works is, a dataframe containing source data will be created at the start
2 - Then the data will be filterd inside function within the intent class,
3 - A good practice would be to have aggregated results in the dataframe and not the whole data
"""
################-----------------------End of Code------------------################
class CustomAction_a_p_r_actions(Node):

        def __init__(self, name):
                self.pprint = PrettyPrinter(indent=4)
                super(CustomAction_a_p_r_actions, self).__init__(name)
				
        def call(self, incoming_msg):
                data=incoming_msg.data
                #Put API Logic Here
                entities = data["entities"]
                year = entities["year"]
                account  = entities["account"]
                #This intents only contain Year and account details 
                #type1 = entities["type"]
                #comments = entities["comments"]
                #sales = entities["sales"]
				apr_data = df[(df["year"] == year) & (df["account"] == account)]
				
                def convert_res(row):
                        return {"year" : row["year"], "month" : row["month"] , "sales" : row["sales"]}

                res = apr_data.apply(convert_res, axis=1)
                       
                results = {           
                        "for_response" : {                     
                                "results" : {
                                        "type" : "graph",
                                        "title" : "The trend of sales for "+account,
                                        "data" : res.values.tolist(),#Code to be added here
                                        "axis" : ["year","month"],
										
                                        "charts" : ["bar","table"]
                                }               
                        }						
                }
				
                results = {'for_response': results}                                                                                                                            
                outgoing_msg=Message.merge([incoming_msg, Message(results)])                                                                                                   
                return super(CustomAction_a_p_r_actions, self).call(outgoing_msg)                                                                                              
                                                                                                                                                                               
class CustomAction_l_a_c_actions(Node):
        def __init__(self, name):                                                                                                                                              
                self.pprint = PrettyPrinter(indent=4)                                                                                                                          
                super(CustomAction_l_a_c_actions, self).__init__(name)                                                                                                         
                                                                                                                                                                               
                                                                                                                                                                               
        def call(self, incoming_msg):                                                                                                                                          
                data=incoming_msg.data                                                                                                                                         
                #Put API Logic Here                                                                                                                                            
                                                                                                                                                                               
                results = {'for_response': results}                                                                                                                            
                outgoing_msg=Message.merge([incoming_msg, Message(results)])                                                                                                   
                return super(CustomAction_l_a_c_actions, self).call(outgoing_msg)                                                                                              
def build_bot(user_id='navitesh.vaswani@saama.com'):                                                                                                                           
                                                                                                                                                                               
        graph=Graph(name='navitesh.vaswani@saama.com_ace_bot_with_2_intent', user_id=user_id)                                                                                  
                                                                                                                                                                               
        #Making the Nodes                                                                                                                                                      
                                                                                                                                                                               
        greet_user = Input('Hello, What do you have in mind!', text_only=True, name='greet_user')                                                                              
        graph.add_node(greet_user)                                                                                                                                             
                                                                                                                                                                               
        ask_for_action = NLUParser(name='ask_for_action', model_path='./ask_for_action', config_path='./resources/config_spacy.json')                                          
        graph.add_node(ask_for_action)                                                                                                                                         
                                                                                                                                                                               
        a_p_r_master_validate = Validator(required_keys=['account', 'year'], name='a_p_r_master_validate')                                                                     
        graph.add_node(a_p_r_master_validate)                                                                                                                                  
                                                                                                                                                                               
        a_p_r_account_validate = Validator(required_keys=['account'], name='a_p_r_account_validate')                                                                           
        graph.add_node(a_p_r_account_validate)                                                                                                                                 
                                                                                                                                                                               
        a_p_r_account_input = Input('Enter account', text_only=True, name='a_p_r_account_input')                                                                               
        graph.add_node(a_p_r_account_input)                                                                                                                                    
                                                                                                                                                                               
        a_p_r_account_parse = NLUParser(name='a_p_r_account_parse', model_path='./a_p_r_account_parse', config_path='./resources/config_spacy.json')                           
        graph.add_node(a_p_r_account_parse)                                                                                                                                    
                                                                                                                                                                               
        a_p_r_year_validate = Validator(required_keys=['year'], name='a_p_r_year_validate')                                                                                    
        graph.add_node(a_p_r_year_validate)                                                                                                                                    
                                                                                                                                                                               
        a_p_r_year_input = Input('Enter year', text_only=True, name='a_p_r_year_input')                                                                                        
        graph.add_node(a_p_r_year_input)                                                                                                                                       
                                                                                                                                                                               
        a_p_r_year_parse = NLUParser(name='a_p_r_year_parse', model_path='./a_p_r_year_parse', config_path='./resources/config_spacy.json')                                    
        graph.add_node(a_p_r_year_parse)                                                                                                                                       
                                                                                                                                                                               
        l_a_c_master_validate = Validator(required_keys=['account', 'type', 'comments'], name='l_a_c_master_validate')                                                         
        graph.add_node(l_a_c_master_validate)
		
		                                                                                                                                                                               
        l_a_c_account_input = Input('Enter account', text_only=True, name='l_a_c_account_input')                                                                               
        graph.add_node(l_a_c_account_input)                                                                                                                                    
                                                                                                                                                                               
        l_a_c_account_parse = NLUParser(name='l_a_c_account_parse', model_path='./l_a_c_account_parse', config_path='./resources/config_spacy.json')                           
        graph.add_node(l_a_c_account_parse)                                                                                                                                    
                                                                                                                                                                               
        l_a_c_type_validate = Validator(required_keys=['type'], name='l_a_c_type_validate')                                                                                    
        graph.add_node(l_a_c_type_validate)                                                                                                                                    
                                                                                                                                                                               
        l_a_c_type_input = Input('Enter type', text_only=True, name='l_a_c_type_input')                                                                                        
        graph.add_node(l_a_c_type_input)                                                                                                                                       
                                                                                                                                                                               
        l_a_c_type_parse = NLUParser(name='l_a_c_type_parse', model_path='./l_a_c_type_parse', config_path='./resources/config_spacy.json')                                    
        graph.add_node(l_a_c_type_parse)                                                                                                                                       
                                                                                                                                                                               
        l_a_c_comments_validate = Validator(required_keys=['comments'], name='l_a_c_comments_validate')                                                                        
        graph.add_node(l_a_c_comments_validate)                                                                                                                                
                                                                                                                                                                               
        l_a_c_comments_input = Input('Enter comments', text_only=True, name='l_a_c_comments_input')                                                                            
        graph.add_node(l_a_c_comments_input)                                                                                                                                   
                                                                                                                                                                               
        l_a_c_comments_parse = NLUParser(name='l_a_c_comments_parse', model_path='./l_a_c_comments_parse', config_path='./resources/config_spacy.json')                        
        graph.add_node(l_a_c_comments_parse)                                                                                                                                   
                                                                                                                                                                               
        a_p_r_actions=CustomAction_a_p_r_actions('a_p_r_actions')                                                                                                              
        graph.add_node(a_p_r_actions)                                                                                                                                          
        l_a_c_actions=CustomAction_l_a_c_actions('l_a_c_actions')                                                                                                              
        graph.add_node(l_a_c_actions)                                                                                                                                          
        a_p_r_response = Response(name='a_p_r_response')                                                                                                                       
        a_p_r_response.add_response_pattern('[results]')                                                                                                                       
        graph.add_node(a_p_r_response)                                                                                                                                         
                                                                                                                                                                               
        l_a_c_response = Response(name='l_a_c_response')                                                                                                                       
        l_a_c_response.add_response_pattern('[results]')                                                                                                                       
        graph.add_node(l_a_c_response)                                                                                                                                         
                                                                                                                                                                               
        exit_master_validate = Validator(required_keys=[], name='exit_master_validate')                                                                                        
        graph.add_node(exit_master_validate)                                                                                                                                   
                                                                                                                                                                               
        end = End()                                                                                                                                                            
        graph.add_node(end)                                                                                                                                                    
                                                                                                                                                                               
        #Making the Connections                                                                                                                                                
                                                                                                                                                                               
        greet_user.add_output(ask_for_action)                                                                                                                                  
        ask_for_action.add_output('a_p_r', a_p_r_master_validate)    
		
		
		        ask_for_action.add_output('l_a_c', l_a_c_master_validate)                                                                                                              
        ask_for_action.add_output('exit', exit_master_validate)                                                                                                                
        a_p_r_master_validate.add_output(a_p_r_actions, True)                                                                                                                  
        a_p_r_master_validate.add_output(a_p_r_account_validate, False)                                                                                                        
        a_p_r_account_validate.add_output(a_p_r_year_validate, True)                                                                                                           
        a_p_r_account_validate.add_output(a_p_r_account_input, False)                                                                                                          
        a_p_r_account_input.add_output(a_p_r_account_parse)                                                                                                                    
        a_p_r_account_parse.add_output('account', a_p_r_account_validate)                                                                                                      
        a_p_r_year_validate.add_output(a_p_r_actions, True)                                                                                                                    
        a_p_r_year_validate.add_output(a_p_r_year_input, False)                                                                                                                
        a_p_r_year_input.add_output(a_p_r_year_parse)                                                                                                                          
        a_p_r_year_parse.add_output('year', a_p_r_year_validate)                                                                                                               
        l_a_c_master_validate.add_output(l_a_c_actions, True)                                                                                                                  
        l_a_c_master_validate.add_output(l_a_c_account_validate, False)                                                                                                        
        l_a_c_account_validate.add_output(l_a_c_type_validate, True)                                                                                                           
        l_a_c_account_validate.add_output(l_a_c_account_input, False)                                                                                                          
        l_a_c_account_input.add_output(l_a_c_account_parse)                                                                                                                    
        l_a_c_account_parse.add_output('account', l_a_c_account_validate)                                                                                                      
        l_a_c_type_validate.add_output(l_a_c_comments_validate, True)                                                                                                          
        l_a_c_type_validate.add_output(l_a_c_type_input, False)                                                                                                                
        l_a_c_type_input.add_output(l_a_c_type_parse)                                                                                                                          
        l_a_c_type_parse.add_output('type', l_a_c_type_validate)                                                                                                               
        l_a_c_comments_validate.add_output(l_a_c_actions, True)                                                                                                                
        l_a_c_comments_validate.add_output(l_a_c_comments_input, False)                                                                                                        
        l_a_c_comments_input.add_output(l_a_c_comments_parse)                                                                                                                  
        l_a_c_comments_parse.add_output('comments', l_a_c_comments_validate)                                                                                                   
        a_p_r_actions.add_output(a_p_r_response)                                                                                                                               
        l_a_c_actions.add_output(l_a_c_response)                                                                                                                               
        a_p_r_response.add_output(ask_for_action)                                                                                                                              
        l_a_c_response.add_output(ask_for_action)                                                                                                                              
        exit_master_validate.add_output(end, True)                                                                                                                             
        exit_master_validate.add_output(ask_for_action, False)                                                                                                                 
                                                                                                                                                                               
        #Complete the Build                                                                                                                                                    
        graph.build_completed()                                                                                                                                                
        return graph          