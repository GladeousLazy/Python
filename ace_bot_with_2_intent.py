import os
import requests
from pprint import PrettyPrinter
import json
from virtassnt.nodes import *
from virtassnt.core import Node, Message
from virtassnt.graph import Graph


class CustomAction_a_p_r_actions(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_a_p_r_actions, self).__init__(name)


	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here

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

	l_a_c_account_validate = Validator(required_keys=['account'], name='l_a_c_account_validate')
	graph.add_node(l_a_c_account_validate)

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