/* Mousetraps keyboard shortcuts */
Mousetrap.bind(['h', 's', 'r', 'u'], function(e, key) {
    var current_doc_id = $('#cal-document').data("doc-id");
    var doc_title = $('#docViewDocTitle').text();
    var doc_snippet = $('#docViewDocSnippet').html();
    if(key == 'h') {
        send_judgment(current_doc_id, doc_title, doc_snippet, 2, 'keyboard');
    } else if(key == 'r') {
        send_judgment(current_doc_id, doc_title, doc_snippet, 1, 'keyboard');
    } else if(key == 's') {
        send_judgment(current_doc_id, doc_title, doc_snippet, 0, 'keyboard');
    } else if(key == 'u') {
        $('#reviewDocsModal').modal('toggle');
    }
    document.body.click();
    //if(queue.getLength() == 0){
    //    console.log("Getting the next patch of documents to judge");
    //    update_documents_to_judge_list();
    //}
});

Mousetrap.bind(['ctrl+f', 'command+f'], function(e) {
    e.preventDefault();
    $( "#search_content" ).focus();
    document.body.click();
    return false;
});

var search_content_form = document.getElementById('search_content');
var search_content_form_mousetrap = new Mousetrap(search_content_form);
search_content_form_mousetrap.bind(['ctrl+f', 'command+f'], function(e) {
    $( "#search_content" ).focus();
    document.body.click();
    return false;
});


function document_isEmpty(){
    var current_doc_id = $('#docView').data("doc-id");
    if(current_doc_id == '' || current_doc_id == 'None'){
        return true;
    }
    return false;
}



