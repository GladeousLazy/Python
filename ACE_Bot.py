import os
import requests
from pprint import PrettyPrinter
import json
from virtassnt.nodes import *
from virtassnt.core import Node, Message
from virtassnt.graph import Graph


class CustomAction_generate_trend(Node):

	def __init__(self, name):
		self.pprint = PrettyPrinter(indent=4)
		super(CustomAction_generate_trend, self).__init__(name)


	def call(self, incoming_msg):
		data=incoming_msg.data
		#Put API Logic Here

		results = {'for_response': results}
		outgoing_msg=Message.merge([incoming_msg, Message(results)])
		return super(CustomAction_generate_trend, self).call(outgoing_msg)
def build_bot(user_id='navitesh.vaswani@saama.com'):

	graph=Graph(name='navitesh.vaswani@saama.com_ACE_Bot', user_id=user_id)

	#Making the Nodes

	greet_user = Input('How are you', text_only=True, name='greet_user')
	graph.add_node(greet_user)

	ask_for_option = NLUParser(name='ask_for_option', model_path='./ask_for_option', config_path='./resources/config_spacy.json')
	graph.add_node(ask_for_option)

	trend_chart_master_validate = Validator(required_keys=['duration', 'year', 'month', 'measure'], name='trend_chart_master_validate')
	graph.add_node(trend_chart_master_validate)

	trend_chart_duration_validate = Validator(required_keys=['duration'], name='trend_chart_duration_validate')
	graph.add_node(trend_chart_duration_validate)

	trend_chart_duration_input = Input('Enter duration', text_only=True, name='trend_chart_duration_input')
	graph.add_node(trend_chart_duration_input)

	trend_chart_duration_parse = NLUParser(name='trend_chart_duration_parse', model_path='./trend_chart_duration_parse', config_path='./resources/config_spacy.json')
	graph.add_node(trend_chart_duration_parse)

	trend_chart_year_validate = Validator(required_keys=['year'], name='trend_chart_year_validate')
	graph.add_node(trend_chart_year_validate)

	trend_chart_year_input = Input('Enter year', text_only=True, name='trend_chart_year_input')
	graph.add_node(trend_chart_year_input)

	trend_chart_year_parse = NLUParser(name='trend_chart_year_parse', model_path='./trend_chart_year_parse', config_path='./resources/config_spacy.json')
	graph.add_node(trend_chart_year_parse)

	trend_chart_month_validate = Validator(required_keys=['month'], name='trend_chart_month_validate')
	graph.add_node(trend_chart_month_validate)

	trend_chart_month_input = Input('Enter month', text_only=True, name='trend_chart_month_input')
	graph.add_node(trend_chart_month_input)

	trend_chart_month_parse = NLUParser(name='trend_chart_month_parse', model_path='./trend_chart_month_parse', config_path='./resources/config_spacy.json')
	graph.add_node(trend_chart_month_parse)

	trend_chart_measure_validate = Validator(required_keys=['measure'], name='trend_chart_measure_validate')
	graph.add_node(trend_chart_measure_validate)

	trend_chart_measure_input = Input('Enter measure', text_only=True, name='trend_chart_measure_input')
	graph.add_node(trend_chart_measure_input)

	trend_chart_measure_parse = NLUParser(name='trend_chart_measure_parse', model_path='./trend_chart_measure_parse', config_path='./resources/config_spacy.json')
	graph.add_node(trend_chart_measure_parse)

	generate_trend=CustomAction_generate_trend('generate_trend')
	graph.add_node(generate_trend)
	show_trend = Response(name='show_trend')
	show_trend.add_response_pattern('[results]')
	graph.add_node(show_trend)

	exit = End()
	graph.add_node(exit)

	#Making the Connections

	greet_user.add_output(ask_for_option)
	ask_for_option.add_output('trend_chart', trend_chart_master_validate)
	trend_chart_master_validate.add_output(generate_trend, True)
	trend_chart_master_validate.add_output(trend_chart_duration_validate, False)
	trend_chart_duration_validate.add_output(trend_chart_year_validate, True)
	trend_chart_duration_validate.add_output(trend_chart_duration_input, False)
	trend_chart_duration_input.add_output(trend_chart_duration_parse)
	trend_chart_duration_parse.add_output('duration', trend_chart_duration_validate)
	trend_chart_year_validate.add_output(trend_chart_month_validate, True)
	trend_chart_year_validate.add_output(trend_chart_year_input, False)
	trend_chart_year_input.add_output(trend_chart_year_parse)
	trend_chart_year_parse.add_output('year', trend_chart_year_validate)
	trend_chart_month_validate.add_output(trend_chart_measure_validate, True)
	trend_chart_month_validate.add_output(trend_chart_month_input, False)
	trend_chart_month_input.add_output(trend_chart_month_parse)
	trend_chart_month_parse.add_output('month', trend_chart_month_validate)
	trend_chart_measure_validate.add_output(generate_trend, True)
	trend_chart_measure_validate.add_output(trend_chart_measure_input, False)
	trend_chart_measure_input.add_output(trend_chart_measure_parse)
	trend_chart_measure_parse.add_output('measure', trend_chart_measure_validate)
	generate_trend.add_output(show_trend)
	show_trend.add_output(exit)

	#Complete the Build
	graph.build_completed()
	return graph