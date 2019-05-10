# -*- coding: utf-8 -*-

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import boto3
from boto3.dynamodb.conditions import Key, Attr

from datetime import datetime

WELCOME_MESSAGE = "Welcome to Eric's Red Flag Deals."
WELCOME_REPROMPT = "Ready to save money?"
GET_SINGLE_DEAL_MESSAGE = "Here's your deal!"
GET_SINGLE_DEAL_REPROMPT = "Say next deal to get next available deal."
GET_ALL_DEALS_MESSAGE = "Deal number"
SPEECH_BREAK = "<break time=\"1s\"/>"
GET_ALL_DEALS_REPROMPT = "Thats it, no more deals for today."
NO_DEALS = "Sorry, there are no deals for today."
HELP_MESSAGE = "You can say tell me a deal, or list all deals, or you can say good bye... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Happy shopping! Good bye."
FALLBACK_MESSAGE = "I could not understand that... What can I help you with?"
FALLBACK_REPROMPT = "You can say send help, I will list you some commands to use."
EXCEPTION_MESSAGE = "Internal Exception raised. I cannot help you with that."

# Scan dynamoDB for all deals
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
rdf_table = dynamodb.Table("rdf_dynamo_table")

try:
    table_response = rdf_table.scan()

    current_day = datetime.now().strftime("%Y-%m-%d")
    deals = []
    # Get only the titles as Alexa will speak them out
    for deal in table_response["Items"]:
        if deal['insert_day'] == current_day:
            deals.append(deal['title'])

except ClientError as e:
    print(e.response['Error']['Message'])

# Initialze the Alexa Skill
sb = SkillBuilder()

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# User invokes the initial skill: "Alexa, open eric's red flag deals"
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak(WELCOME_MESSAGE).ask(
            WELCOME_REPROMPT)
        return handler_input.response_builder.response


# Get one rdf deal: "tell me a deal"
class GetRdfDealHandler(AbstractRequestHandler):
    """Handler for GetRdfDeal Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("GetRdfDealIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In GetRdfDealHandler")

        if not deals:
            speech_text = NO_DEALS
        else:
            deal = random.choice(deals)
            speech_text = GET_SINGLE_DEAL_MESSAGE + deal

        handler_input.response_builder.speak(speech_text).ask(GET_SINGLE_DEAL_REPROMPT)
        return handler_input.response_builder.response


# List all rdf deals for the day: "list all deals"
class GetAllRdfDealsHandler(AbstractRequestHandler):
    """Handler for GetAllRdfDeal Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("GetAllRdfDealsIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In GetAllRdfDealsHandler")

        if not deals:
            speech_text = NO_DEALS
        else:
            speech_text = ""
            i = 0
            for deal in deals:
                i += 1
                speech_text = speech_text + GET_ALL_DEALS_MESSAGE + \
                              str(i) + SPEECH_BREAK + deal + SPEECH_BREAK

        handler_input.response_builder.speak(speech_text).ask(GET_ALL_DEALS_REPROMPT)
        return handler_input.response_builder.response


# Help option: "help me"
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT)
        return handler_input.response_builder.response


# Cancels the alexa skill: "Good bye!"
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


# Fallback prompt if alexa did not understand your command
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.info("In CatchAllExceptionHandler")
        logger.info(deals)
        logger.info(table_response)
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetRdfDealHandler())
sb.add_request_handler(GetAllRdfDealsHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()