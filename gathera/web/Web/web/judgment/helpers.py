from web.judgment.models import Judgment


def remove_judged_docs(document_ids, user, session):
    """
    Remove already judged documents for a list of document ids
    :param user:
    :param session:
    :param document_ids:
    :return: document_ids list of documents that are not judged, in the same given order.
    """

    judged_docs = Judgment.objects.filter(user=user,
                                          session=session,
                                          doc_id__in=document_ids,
                                          relevance__isnull=False
                                          ).values_list('doc_id', flat=True)

    document_ids = [elem for elem in document_ids if elem not in judged_docs]
    return document_ids
