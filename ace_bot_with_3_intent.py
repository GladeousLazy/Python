import os
import requests
from pprint import PrettyPrinter
import json
from virtassnt.nodes import *
from virtassnt.core import Node, Message
from virtassnt.graph import Graph


class CustomAction_show_chart(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_show_chart, self).__init__(name)


	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here

		results = {'for_response': results}
		outgoing_msg=Message.merge([incoming_msg, Message(results)])
		return super(CustomAction_show_chart, self).call(outgoing_msg)

class CustomAction_show_text(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_show_text, self).__init__(name)


	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here

		results = {'for_response': results}
		outgoing_msg=Message.merge([incoming_msg, Message(results)])
		return super(CustomAction_show_text, self).call(outgoing_msg)

class CustomAction_show_table(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_show_table, self).__init__(name)


	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here

		results = {'for_response': results}
		outgoing_msg=Message.merge([incoming_msg, Message(results)])
		return super(CustomAction_show_table, self).call(outgoing_msg)
def build_bot(user_id='navitesh.vaswani@saama.com'):

	graph=Graph(name='navitesh.vaswani@saama.com_ace_bot_with_3_intent', user_id=user_id)

	#Making the Nodes

	greet_user = Input('Hi, Welcome to ACE bot. How can I help you?', text_only=True, name='greet_user')
	graph.add_node(greet_user)

	ask_for_action = NLUParser(name='ask_for_action', model_path='./ask_for_action', config_path='./resources/config_spacy.json')
	graph.add_node(ask_for_action)

	chart_intent_master_validate = Validator(required_keys=[], name='chart_intent_master_validate')
	graph.add_node(chart_intent_master_validate)

	text_intent_master_validate = Validator(required_keys=[], name='text_intent_master_validate')
	graph.add_node(text_intent_master_validate)

	table_intent_master_validate = Validator(required_keys=[], name='table_intent_master_validate')
	graph.add_node(table_intent_master_validate)

	exit_master_validate = Validator(required_keys=[], name='exit_master_validate')
	graph.add_node(exit_master_validate)

	show_chart=CustomAction_show_chart('show_chart')
	graph.add_node(show_chart)
	show_text=CustomAction_show_text('show_text')
	graph.add_node(show_text)
	show_table=CustomAction_show_table('show_table')
	graph.add_node(show_table)
	exit_node = End()
	graph.add_node(exit_node)

	chart_response = Response(name='chart_response')
	chart_response.add_response_pattern('[results]')
	graph.add_node(chart_response)

	text_response = Response(name='text_response')
	text_response.add_response_pattern('[results]')
	graph.add_node(text_response)

	table_response = Response(name='table_response')
	table_response.add_response_pattern('[results]')
	graph.add_node(table_response)

	#Making the Connections

	greet_user.add_output(ask_for_action)
	ask_for_action.add_output('chart_intent', chart_intent_master_validate)
	ask_for_action.add_output('text_intent', text_intent_master_validate)
	ask_for_action.add_output('table_intent', table_intent_master_validate)
	ask_for_action.add_output('exit', exit_master_validate)
	chart_intent_master_validate.add_output(show_chart, True)
	chart_intent_master_validate.add_output(greet_user, False)
	text_intent_master_validate.add_output(show_text, True)
	text_intent_master_validate.add_output(greet_user, False)
	table_intent_master_validate.add_output(show_table, True)
	table_intent_master_validate.add_output(greet_user, False)
	exit_master_validate.add_output(exit_node, True)
	exit_master_validate.add_output(greet_user, False)
	show_chart.add_output(chart_response)
	show_text.add_output(text_response)
	show_table.add_output(table_response)
	chart_response.add_output(greet_user)
	text_response.add_output(greet_user)
	table_response.add_output(greet_user)

	#Complete the Build
	graph.build_completed()
	return graph