/**
 * Created with IntelliJ IDEA.
 * User: me
 * Date: 5/16/14
 * Time: 2:32 PM
 *
 */

(function(dom){
    function _show_reuslt(dom, data){
        if(data.code != 0 ){
            alert('同步出错!');
            return false;
        }
        self = jQuery(dom);
        self.siblings('.result').html(data.msg);
        if(typeof console == 'object'){
            console.dir(data.result);
        }
        return true;
    }
    function _request_action(url, dom){
        jQuery.getJSON(url, {}, function(data){
            _show_reuslt(dom, data);
        });
    }

    function _dw_url(id){
        url = '/admin/cdn/down_ios_resource/' + id + "/";
        return url;
    }
    dom.down_iosapp_resource = function(dom, id){
        _request_action(_dw_url(id), dom)
    };

    function _sync_url(id){
        url = '/admin/cdn/sync_resource_to_version/' + id + "/";
        return url;
    }
    dom.sync_resources_to_version = function(dom, id){
        _request_action(_sync_url(id), dom)
    };

})(this);

