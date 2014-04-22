/**
 * Created with IntelliJ IDEA.
 * User: me
 * Date: 3/14/14
 * Time: 4:49 PM
 * To change this template use File | Settings | File Templates.
 */
function sync_url(content_type, object_pk){
    url = '/admin/cdn/syncqueue/' + content_type + "/" + object_pk + "/";
    return url;
}

function show_sync_reuslt(dom, data){
    if(data.code != 0 ){
        alert('同步出错!');
        return false;
    }
    self = jQuery(dom);
    self.siblings('.result').html('Processing');
    if(typeof console == 'object'){
        console.dir(data.result);
    }
    return true;
}

function sync_publish_file(dom, content_type, object_pk, filelevel){
    url = sync_url(content_type, object_pk);
    jQuery.getJSON(url, {op_name:'publish', filelevel:filelevel}, function(data){
        show_sync_reuslt(dom, data);
    });
}

function sync_update_file(dom, content_type, object_pk){
    url = sync_url(content_type, object_pk);
    jQuery.getJSON(url, {op_name:'update'}, function(data){
        show_sync_reuslt(dom, data);
    });
}

function sync_rename_file(dom, content_type, object_pk){
    url = sync_url(content_type, object_pk);
    jQuery.getJSON(url, {op_name:'rename'}, function(data){
        show_sync_reuslt(data);
    });
}

function sync_check_file(dom, content_type, object_pk, filelevel){
    url = sync_url(content_type, object_pk);
    jQuery.getJSON(url, {op_name:'check'}, function(data){
        show_sync_reuslt(dom, data);
    });
}
