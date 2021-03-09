import json
import logging

from braces import views
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from interfaces.DocumentSnippetEngine import functions as DocEngine

from web.CAL.exceptions import CALError
from web.CAL.exceptions import CALServerSessionNotFoundError
from web.core.mixin import RetrievalMethodPermissionMixin
from web.interfaces.CAL import functions as CALFunctions
from web.judgment.models import Judgment
from web.CAL.models import Stratum

logger = logging.getLogger(__name__)


class CALHomePageView(views.LoginRequiredMixin,
                      RetrievalMethodPermissionMixin,
                      generic.TemplateView):
    template_name = 'CAL/CAL.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.current_session:
            return HttpResponseRedirect(reverse_lazy('core:home'))
        return super(CALHomePageView, self).get(self, request, *args, **kwargs)


class CALMessageAJAXView(views.CsrfExemptMixin,
                         views.LoginRequiredMixin,
                         RetrievalMethodPermissionMixin,
                         views.JsonRequestResponseMixin,
                         generic.View):
    """
    Generic view to capture specific log messages from browser
    """
    require_json = False

    def post(self, request, *args, **kwargs):
        try:
            client_time = self.request_json.get(u"client_time")
            message = self.request_json.get(u"message")
            action = self.request_json.get(u"action")
            page_title = self.request_json.get(u"page_title")
            doc_CAL_snippet = self.request_json.get(u'doc_CAL_snippet')
            doc_id = self.request_json.get(u'doc_id')
            extra_context = self.request_json.get(u'extra_context')
        except KeyError:
            error_dict = {u"message": u"your input must include client_time, "
                                      u"message, ... etc"}
            return self.render_bad_request_response(error_dict)

        context = {u"message": u"Your log message with action '{}' and of "
                               u"document '{}' has been logged.".format(action, doc_id)}
        return self.render_json_response(context)


class DocAJAXView(views.CsrfExemptMixin,
                  RetrievalMethodPermissionMixin,
                  views.LoginRequiredMixin,
                  views.JsonRequestResponseMixin,
                  views.AjaxResponseMixin, generic.View):
    """
    View to get a list of documents (with their content) to judge from CAL
    """
    require_json = False

    def render_timeout_request_response(self, error_dict=None):
        if error_dict is None:
            error_dict = self.error_response_dict
        json_context = json.dumps(
            error_dict,
            cls=self.json_encoder_class,
            **self.get_json_dumps_kwargs()
        ).encode('utf-8')
        return HttpResponse(
            json_context, content_type=self.get_content_type(), status=502)

    def get_ajax(self, request, *args, **kwargs):
        session = self.request.user.current_session
        seed_query = self.request.user.current_session.topic.seed_query
        try:
            docids_to_judge, top_terms = CALFunctions.get_documents(str(session.uuid), 10)
            if not docids_to_judge:
                return self.render_json_response([])

            ret = {}
            next_patch_ids = []
            for docid_score_pair in docids_to_judge:
                doc_id, doc_score = docid_score_pair.rsplit(':', 1)
                ret[doc_id] = doc_score
                next_patch_ids.append(doc_id)

            doc_ids_hack = []
            for doc_id in next_patch_ids:
                doc = {'doc_id': doc_id}
                if '.' in doc_id:
                    doc['doc_id'], doc['para_id'] = doc_id.split('.')
                doc_ids_hack.append(doc)

            if 'doc' in self.request.user.current_session.strategy:
                documents = DocEngine.get_documents(next_patch_ids,
                                                    seed_query,
                                                    top_terms)
            else:
                documents = DocEngine.get_documents_with_snippet(doc_ids_hack,
                                                                 seed_query,
                                                                 top_terms)

            return self.render_json_response(documents)
        except TimeoutError:
            error_dict = {u"message": u"Timeout error. Please check status of servers."}
            return self.render_timeout_request_response(error_dict)
        except CALServerSessionNotFoundError:
            message = "Ops! Session is not found in CAL. "
            if "scal" not in self.request.user.current_session.strategy:
                seed_judgments = Judgment.objects.filter(user=self.request.user,
                                                         session=session
                                                         ).filter(relevance__isnull=False)
                strategy = self.request.user.current_session.strategy
                CALFunctions.restore_session(session.uuid,
                                             seed_query,
                                             seed_judgments,
                                             strategy)
                message += "Restoring.. Please try in few minutes."
            return JsonResponse({"message": message}, status=404)
        except CALError as e:
            return JsonResponse({"message": "Ops! CALError."}, status=404)


class SCALInfoView(views.CsrfExemptMixin,
                   RetrievalMethodPermissionMixin,
                   views.LoginRequiredMixin,
                   views.JsonRequestResponseMixin,
                   views.AjaxResponseMixin, generic.View):
    """
    View to get stratum information from the CAL engine
    """
    require_json = False

    def render_timeout_request_response(self, error_dict=None):
        if error_dict is None:
            error_dict = self.error_response_dict
        json_context = json.dumps(
            error_dict,
            cls=self.json_encoder_class,
            **self.get_json_dumps_kwargs()
        ).encode('utf-8')
        return HttpResponse(
            json_context, content_type=self.get_content_type(), status=502)

    def get_ajax(self, request, *args, **kwargs):
        session = self.request.user.current_session.uuid
        try:
            info = CALFunctions.get_scal_info(str(session))

            return self.render_json_response(info)
        except TimeoutError:
            error_dict = {u"message": u"Timeout error. Please check status of servers."}
            return self.render_timeout_request_response(error_dict)
        except CALError as e:
            return JsonResponse({"message": "Oops! CALError."}, status=404)


class DocIDsAJAXView(views.CsrfExemptMixin,
                     RetrievalMethodPermissionMixin,
                     views.LoginRequiredMixin,
                     views.JsonRequestResponseMixin,
                     views.AjaxResponseMixin, generic.View):
    """
    View to get ids of documents to judge from CAL
    """
    require_json = False

    def render_timeout_request_response(self, error_dict=None):
        if error_dict is None:
            error_dict = self.error_response_dict
        json_context = json.dumps(
            error_dict,
            cls=self.json_encoder_class,
            **self.get_json_dumps_kwargs()
        ).encode('utf-8')
        return HttpResponse(
            json_context, content_type=self.get_content_type(), status=502)

    def get_ajax(self, request, *args, **kwargs):
        session = self.request.user.current_session.uuid
        try:
            docs_ids_to_judge = CALFunctions.get_documents(str(session), 5)
            return self.render_json_response(docs_ids_to_judge)
        except TimeoutError:
            error_dict = {u"message": u"Timeout error. Please check status of servers."}
            return self.render_timeout_request_response(error_dict)
        except CALError as e:
            # TODO: add proper http response for CAL errors
            return JsonResponse({"message": "Ops! CALError."}, status=404)


class DSLoggingView(views.CsrfExemptMixin,
                    views.LoginRequiredMixin,
                    RetrievalMethodPermissionMixin,
                    views.JsonRequestResponseMixin,
                    generic.View):
    """
    View to log stratum information in the dynamic sampling method
    """
    require_json = False

    def post(self, request, *args, **kwargs):
        session = self.request.user.current_session.uuid

        try:
            stratum_num = self.request_json.get(u"stratum_number")
            stratum_size = self.request_json.get(u"stratum_size")
            T = self.request_json.get(u"T")
            N = self.request_json.get(u"N")
            R = self.request_json.get(u"R")
            current_sample_size = self.request_json.get(u"n")

            # Get docs in current stratum
            docs, sampled_docs = CALFunctions.get_stratum_documents(str(session), stratum_num, include_sampled=1)

        except KeyError:
            error_dict = {u"message": u"Errors when getting DS info."}
            return self.render_bad_request_response(error_dict)

        if not docs:
            return self.render_bad_request_response({u"message": u"Empty set for stratum {}".format(stratum_num)})

        if not sampled_docs:
            return self.render_bad_request_response({u"message": u"Empty sample for stratum {}".format(stratum_num)})

        if int(stratum_num) == 1:
            current_sample_size = 1

        docs_list = {}
        for docid_score_pair in docs:
            doc_id, score = docid_score_pair.rsplit(':', 1)
            docs_list[doc_id] = float(score)

        sampled_docs_list = []
        for docid_score_pair in sampled_docs:
            doc_id, score = docid_score_pair.rsplit(':', 1)
            sampled_docs_list.append(doc_id)

        exists = Stratum.objects.filter(user=self.request.user,
                                        stratum_num=stratum_num,
                                        session=self.request.user.current_session)

        if exists:
            return self.render_bad_request_response(
                {u"message": u"Duplicate record for stratum {}".format(stratum_num)})
        else:
            Stratum.objects.create(user=self.request.user,
                                   session=self.request.user.current_session,
                                   stratum_size=int(stratum_size),
                                   stratum_num=int(stratum_num),
                                   sample_size=int(current_sample_size),
                                   T=int(T),
                                   N=int(N),
                                   R=int(R),
                                   stratum_docs=docs_list,
                                   sampled_docs=sampled_docs_list)

        context = {u"message": u"Information of stratum '{}' has been logged.".format(stratum_num)}
        return self.render_json_response(context)
