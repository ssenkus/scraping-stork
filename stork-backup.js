(function(factory) {
    if (typeof define === 'function' && define.amd) {
// AMD. Register as anonymous module.
        define(['jquery'], factory);
    } else {
// Browser globals.
        factory(jQuery);
    }
}(function($) {

    var pluses = /\+/g;
    function encode(s) {
        return config.raw
            ? s
            : encodeURIComponent(s);
    }

    function decode(s) {
        return config.raw
            ? s
            : decodeURIComponent(s);
    }

    function stringifyCookieValue(value) {
        return encode(config.json
            ? JSON.stringify(value)
            : String(value));
    }

    function parseCookieValue(s) {
        if (s.indexOf('"') === 0) {
// This is a quoted cookie as according to RFC2068, unescape...
            s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
        }

        try {
// Replace server-side written pluses with spaces.
// If we can't decode the cookie, ignore it, it's unusable.
// If we can't parse the cookie, ignore it, it's unusable.
            s = decodeURIComponent(s.replace(pluses, ' '));
            return config.json
                ? JSON.parse(s)
                : s;
        } catch (e) {
        }
    }

    function read(s, converter) {
        var value = config.raw
            ? s
            : parseCookieValue(s);
        return $.isFunction(converter)
            ? converter(value)
            : value;
    }

    var config = $.cookie = function(key, value, options) {

// Write
        if (value !== undefined && !$.isFunction(value)) {
            options = $.extend({}, config.defaults, options);
            if (typeof options.expires === 'number') {
                var days = options.expires, t = options.expires = new Date();
                t.setDate(t.getDate() + days);
            }

            return (document.cookie = [
                encode(key), '=', stringifyCookieValue(value),
                options.expires
                    ? '; expires=' + options.expires.toUTCString()
                    : '', // use expires attribute, max-age is not supported by IE
                options.path
                    ? '; path=' + options.path
                    : '',
                options.domain
                    ? '; domain=' + options.domain
                    : '',
                options.secure
                    ? '; secure'
                    : ''
            ].join(''));
        }

// Read

        var result = key
            ? undefined
            : {};
        // To prevent the for loop in the first place assign an empty array
        // in case there are no cookies at all. Also prevents odd result when
        // calling $.cookie().
        var cookies = document.cookie
            ? document.cookie.split('; ')
            : [];
        for (var i = 0, l = cookies.length; i < l; i++) {
            var parts = cookies[i].split('=');
            var name = decode(parts.shift());
            var cookie = parts.join('=');
            if (key && key === name) {
// If second argument (value) is a function it's a converter...
                result = read(cookie, value);
                break;
            }

// Prevent storing a cookie that we couldn't decode.
            if (!key && (cookie = read(cookie)) !== undefined) {
                result[name] = cookie;
            }
        }

        return result;
    };
    config.defaults = {};
    $.removeCookie = function(key, options) {
        if ($.cookie(key) === undefined) {
            return false;
        }

// Must not alter options, thus extending a fresh object...
        $.cookie(key, '', $.extend({}, options, {expires: -1}));
        return !$.cookie(key);
    };
}));

(function($) {

    $(document).ready(function() {

        //console.log('#####################START SCRIPT###########');

        var bctMgmt = (function() {

            var bcPresence = false;
            var productPage = ($('form[name="orderform"]').length > 0) ? true : false;
            var bcs = $('.breadcrumbs');

            /* Cookie functions */
            function setCookieVal(value) {  // value is an array of objects that represent the browser history
                //console.log('before setting Cookie:', $.cookie('bcHistory'));
                $.cookie('bcHistory', value);
                //console.log('after setting Cookie:', $.cookie('bcHistory'));
            }

            function getCookieVal() {
                var cv = $.cookie('bcHistory');
                //console.log('cookie value', cv);
                return cv;
            }

            function deleteCookieVal() {
                //console.log('not product page!, delete cookie...');
                $.removeCookie('bcHistory');
            }


            /* Breadcrumb Trail functions */
            function getBreadCrumbs() {
                //console.log('################');
                //console.log('getBreadCrumbs()');
                //console.log('################');
                // set the cookie based on current breadcrumb

                var currentBcArray = [];
                var currentBcLinks = $('.breadcrumbs:visible').find('a');
                var bcLast = $('.breadcrumbs:visible').find('span');

                // add links
                for (var i = 0, len = currentBcLinks.length; i < len; i++) {
                    currentBcArray.push({
                        title: currentBcLinks[i].text,
                        href: currentBcLinks[i].href
                    });
                }

                // add current page
                currentBcArray.push({
                    title: bcLast.text(),
                    href: window.location.href
                });

                // is page a product page?  then don't set cookie
                (productPage) ? '' : setCookieVal(currentBcArray);


            }

            function matchBreadCrumbs() {
                if (!bcPresence) {
                    getBreadcrumbs();
                    return;
                }
                //console.log('###################');
                //console.log(' matchBreadCrumb() ');
                //console.log('###################');

                var bcTrailAll = $('.breadcrumbs');

                //console.log('# of breadcrumb trails', bcTrailAll.length);
                // if there is only one cookie trail, grab it and exit this function
                if (bcTrailAll.length === 1) {
                    //console.log('only one breadcrumb trail, so grab it!');
                    getBreadCrumbs();

                } else {

                    // loop through all .breadcrumb <div>s and find <a>s
                    // then compare titles
                    var currentCookieVal = getCookieVal();
                    bcTrailAll.each(function(i) {
                        var linkEls = $(this).find('a');
                        var match = false;

                        //console.log(".breadcrumbs #" + i);
                        //console.log("##### TEST BREADCRUMB #####");

                        for (var j = 0, len = linkEls.length; j < len; j++) {
                            //console.log('found:' + linkEls[j].text + ", looking for: " + currentCookieVal[j].title);
                            if (linkEls[j].text === currentCookieVal[j].title) {
                                match = true;
                                //console.log('match', linkEls[j].text);
                            } else {
                                //console.log("##### FAIL!!! - TRY NEXT BREADCRUMB #####");
                                match = false;
                                break;
                            }
                        }

                        if (match) {
                            //console.log('found it!', $.cookie('bcHistory'));
                            $('.breadcrumbs').hide();
                            $(this).show();
                            getBreadCrumbs();
                            return false;
                        } else {
                            //console.log('No match!');
                        }
                    });
                }
            }

            function checkPage() {
                // are breadcrumbs on this page?
                var bcWrapper = $('#c4-breadcrumbs-id10T');
                // is this a product page? 

                //console.log('Product Page?', productPage);
                // does page have breadcrumb wrapper?            

                if (bcWrapper.length > 0 || bcs.length > 0) {
                    //console.log('breadcrumbs are present!');
                    bcPresence = true;
                } else {
                    //console.log('breadcrumbs are not present!');
                    bcPresence = false;
                }
                return bcPresence;
            }

            return {
                getCV: getCookieVal,
                setCV: setCookieVal,
                delCV: deleteCookieVal,
                matchBC: matchBreadCrumbs,
                setBC: getBreadCrumbs,
                bctOnPage: checkPage
            };
        })();

        $.cookie.json = true;

        if (bctMgmt.bctOnPage()) {
            if (bctMgmt.getCV() === undefined) {
                bctMgmt.setBC();
            } else {
                bctMgmt.matchBC();
            }
        } else {
            bctMgmt.setBC();
        }

        $('#left-navigation').find("a").click(function(e) {
            e.preventDefault();
            //console.log('left nav');
            var bcArray = [];

            bcArray.push({
                title: 'Home',
                href: 'http://www.storkbabygiftbaskets.com/index.html'
            });

            // put home & link array info into the cookie
            // check this before adding it
            bcArray.push({
                title: $(this).text(),
                href: $(this).attr('href')
            });
            bctMgmt.setCV(bcArray);
            window.location.href = $(this).attr('href');
        });

        window.bctMgmt = bctMgmt;

        //console.log('#####################END SCRIPT#############');
    });
}(jQuery));