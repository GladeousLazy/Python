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

class CustomAction_save_to_database(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_save_to_database, self).__init__(name)


	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here

		results = {'for_response': results}
		outgoing_msg=Message.merge([incoming_msg, Message(results)])
		return super(CustomAction_save_to_database, self).call(outgoing_msg)
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

	exit_node = End()
	graph.add_node(exit_node)

	chart_response = Response(name='chart_response')
	chart_response.add_response_pattern('[results]')
	graph.add_node(chart_response)

	text_response = Response(name='text_response')
	text_response.add_response_pattern('[results_1]')
	graph.add_node(text_response)

	table_response = Response(name='table_response')
	table_response.add_response_pattern('[results_2]')
	graph.add_node(table_response)

	back_to_ask_for_actions = Input('What else can I do for you?', text_only=True, name='back_to_ask_for_actions')
	graph.add_node(back_to_ask_for_actions)

	add_comments_master_validate = Validator(required_keys=[], name='add_comments_master_validate')
	graph.add_node(add_comments_master_validate)

	enter_comment_string = Input('Please share your comment or feedback with us', text_only=True, name='enter_comment_string')
	graph.add_node(enter_comment_string)

	show_the_entered_comment = Response(name='show_the_entered_comment')
	show_the_entered_comment.add_response_pattern('[results]')
	graph.add_node(show_the_entered_comment)

	show_chart=CustomAction_show_chart('show_chart')
	graph.add_node(show_chart)
	show_text=CustomAction_show_text('show_text')
	graph.add_node(show_text)
	show_table=CustomAction_show_table('show_table')
	graph.add_node(show_table)
	save_to_database=CustomAction_save_to_database('save_to_database')
	graph.add_node(save_to_database)
	#Making the Connections

	greet_user.add_output(ask_for_action)
	ask_for_action.add_output('chart_intent', chart_intent_master_validate)
	ask_for_action.add_output('text_intent', text_intent_master_validate)
	ask_for_action.add_output('table_intent', table_intent_master_validate)
	ask_for_action.add_output('exit', exit_master_validate)
	ask_for_action.add_output('add_comments', add_comments_master_validate)
	chart_intent_master_validate.add_output(show_chart, True)
	chart_intent_master_validate.add_output(greet_user, False)
	text_intent_master_validate.add_output(show_text, True)
	text_intent_master_validate.add_output(greet_user, False)
	table_intent_master_validate.add_output(show_table, True)
	table_intent_master_validate.add_output(greet_user, False)
	exit_master_validate.add_output(exit_node, True)
	exit_master_validate.add_output(ask_for_action, False)
	chart_response.add_output(back_to_ask_for_actions)
	text_response.add_output(back_to_ask_for_actions)
	table_response.add_output(back_to_ask_for_actions)
	back_to_ask_for_actions.add_output(ask_for_action)
	add_comments_master_validate.add_output(enter_comment_string, True)
	add_comments_master_validate.add_output(back_to_ask_for_actions, False)
	enter_comment_string.add_output(save_to_database)
	show_the_entered_comment.add_output(back_to_ask_for_actions)
	show_chart.add_output(chart_response)
	show_text.add_output(text_response)
	show_table.add_output(table_response)
	save_to_database.add_output(show_the_entered_comment)

	#Complete the Build
	graph.build_completed()
	return graph