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

	graph=Graph(name='navitesh.vaswani@saama.com_bot_with_2_intent_v2', user_id=user_id)

	#Making the Nodes

	greet_user = Input('How can I help!', text_only=True, name='greet_user')
	graph.add_node(greet_user)

	ask_for_action = NLUParser(name='ask_for_action', model_path='./ask_for_action', config_path='./resources/config_spacy.json')
	graph.add_node(ask_for_action)

	a_p_r_master_validate = Validator(required_keys=[], name='a_p_r_master_validate')
	graph.add_node(a_p_r_master_validate)

	l_a_c_master_validate = Validator(required_keys=[], name='l_a_c_master_validate')
	graph.add_node(l_a_c_master_validate)

	exit_master_validate = Validator(required_keys=[], name='exit_master_validate')
	graph.add_node(exit_master_validate)

	a_p_r_actions=CustomAction_a_p_r_actions('a_p_r_actions')
	graph.add_node(a_p_r_actions)
	l_a_c_actions=CustomAction_l_a_c_actions('l_a_c_actions')
	graph.add_node(l_a_c_actions)
	end = End()
	graph.add_node(end)

	a_p_r_response = Response(name='a_p_r_response')
	a_p_r_response.add_response_pattern('[results]')
	graph.add_node(a_p_r_response)

	l_a_c_response = Response(name='l_a_c_response')
	l_a_c_response.add_response_pattern('[results]')
	graph.add_node(l_a_c_response)

	#Making the Connections

	greet_user.add_output(ask_for_action)
	ask_for_action.add_output('a_p_r', a_p_r_master_validate)
	ask_for_action.add_output('l_a_c', l_a_c_master_validate)
	ask_for_action.add_output('exit', exit_master_validate)
	a_p_r_master_validate.add_output(a_p_r_actions, True)
	a_p_r_master_validate.add_output(greet_user, False)
	l_a_c_master_validate.add_output(l_a_c_actions, True)
	l_a_c_master_validate.add_output(greet_user, False)
	exit_master_validate.add_output(end, True)
	exit_master_validate.add_output(greet_user, False)
	a_p_r_actions.add_output(a_p_r_response)
	l_a_c_actions.add_output(l_a_c_response)
	a_p_r_response.add_output(greet_user)
	l_a_c_response.add_output(greet_user)

	#Complete the Build
	graph.build_completed()
	return graph