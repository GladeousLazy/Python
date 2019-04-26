import os
import requests
from pprint import PrettyPrinter
import json
from virtassnt.nodes import *
from virtassnt.core import Node, Message
from virtassnt.graph import Graph
import pandas as pd #Navitesh - This line was added to create custom dataframe for the Dalia bot

#Navitesh - Below is a sample data from for testing out the bot, the data contains year, month and sales value
df = pd.DataFrame([[2018,'jan',1000],[2019,'jan',2000],[2017,'jan',3000],[2018,'feb',4000]],columns = ['year','month','sales'])

class CustomAction_show_value(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_show_value, self).__init__(name)

#Navitesh - The below piece of code is updated to accomodate the custom response
	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here
		entities = data["entities"]
		year = entities["year"]
		month = entities["month"]

		def convert_res(row):
			return {"year" : row["year"], "month" : row["month"] , sales : row[sales]}

		res = products.apply(convert_res, axis=1)

		##Navitesh -  This is the original peice of code ##  results = {'for_response': results}

        #Navitesh - Below is the new piece of code that creates the desired response.
        results = {
			"for_response" : {
				"results" : {
				"type" : "text",
                "data" : "The year selected is " + year + " and the month selected is " +  month,
                "baseName" : "year"
                }
			}
		}
				
		outgoing_msg=Message.merge([incoming_msg, Message(results)])
		return super(CustomAction_show_value, self).call(outgoing_msg)
def build_bot(user_id='navitesh.vaswani@saama.com'):

	graph=Graph(name='navitesh.vaswani@saama.com_ACE_Bot', user_id=user_id)

	#Making the Nodes

	greet_user = Input('How are you', text_only=True, name='greet_user')
	graph.add_node(greet_user)

	ytd_sales = NLUParser(name='ytd_sales', model_path='./ytd_sales', config_path='./resources/config_spacy.json')
	graph.add_node(ytd_sales)

	check_for_yr_mth_master_validate = Validator(required_keys=['year', 'month'], name='check_for_yr_mth_master_validate')
	graph.add_node(check_for_yr_mth_master_validate)

	year_validate = Validator(required_keys=['year'], name='year_validate')
	graph.add_node(year_validate)

	year_input = Input('Enter year', text_only=True, name='year_input')
	graph.add_node(year_input)

	year_parse = NLUParser(name='year_parse', model_path='./year_parse', config_path='./resources/config_spacy.json')
	graph.add_node(year_parse)

	month_validate = Validator(required_keys=['month'], name='month_validate')
	graph.add_node(month_validate)

	month_input = Input('Enter month', text_only=True, name='month_input')
	graph.add_node(month_input)

	month_parse = NLUParser(name='month_parse', model_path='./month_parse', config_path='./resources/config_spacy.json')
	graph.add_node(month_parse)

	show_value=CustomAction_show_value('show_value')
	graph.add_node(show_value)
	end = End()
	graph.add_node(end)

	final_response = Response(name='final_response')
	final_response.add_response_pattern('[result]')
	graph.add_node(final_response)

	exitnode = Input('Do you have any other request?', text_only=True, name='exitnode')
	graph.add_node(exitnode)

	#Making the Connections

	greet_user.add_output(ytd_sales)
	ytd_sales.add_output('check_for_yr_mth', check_for_yr_mth_master_validate)
	check_for_yr_mth_master_validate.add_output(show_value, True)
	check_for_yr_mth_master_validate.add_output(year_validate, False)
	year_validate.add_output(month_validate, True)
	year_validate.add_output(year_input, False)
	year_input.add_output(year_parse)
	year_parse.add_output('year', year_validate)
	month_validate.add_output(month_input, True)
	month_validate.add_output(show_value, False)
	month_input.add_output(month_parse)
	month_parse.add_output('month', month_validate)
	show_value.add_output(final_response)
	final_response.add_output(exitnode)
	exitnode.add_output(end)

	#Complete the Build
	graph.build_completed()
	return graph