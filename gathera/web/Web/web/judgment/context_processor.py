import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def judging_criteria_processor(request):
    context = {}
    try:
        # TODO: Validate format of settings.ADDITIONAL_JUDGING_CRITERIA
        #  (e.g. no duplicate variables, contains correct fields, etc)
        context["main_judging_criteria_name"] = settings.MAIN_JUDGING_CRITERIA_NAME
        context["additional_judging_criteria"] = settings.ADDITIONAL_JUDGING_CRITERIA

    except NameError:
        logger.error("Could not find judging criteria config variables in settings file.")
        return context

    return context
