/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */
/*  MTL website JavaScript functions (c) Chris Veness 2008-2016                                   */
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

// var ie11 = !(window.ActiveXObject) && 'ActiveXObject' in window;
//
// document.addEventListener('DOMContentLoaded', function() {
//
//   // set external links to 'target=_blank' (note doesn't work on IE, but...)
//   var elHref = document.querySelectorAll('a[href^="http://"],a[href^="https://"],a[href^="//"]');
//   for (var i=0; i<elHref.length; i++) elHref[i].target = '_blank';
//
//
//   /* google analytics tracking code - use jQuery getScript() to load tracking code after DOM load is complete
//   var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
//   jQuery.getScript(gaJsHost + "google-analytics.com/ga.js", function(){
//     try {
//       var pageTracker = _gat._getTracker("UA-966502-1");
//       pageTracker._trackPageview();
//     } catch(err) {}
//   }); */
//
// });


/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-85917736-1', 'auto');
ga('send', 'pageview');

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/*
 * add isNumber function - JavaScript: The Good Parts, Douglas Crockford, O'Reilly
 */
if (typeof(isNumber) === "undefined") {
  var isNumber = function isNumber(value) {
    return typeof value === 'number' && isFinite(value);
  };
}

// developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/String/trim#Polyfill
if (!String.prototype.trim) {
  String.prototype.trim = function () {
    return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '');
  };
}

// developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Object/assign#Polyfill
if (typeof Object.assign != 'function') {
  (function () {
    Object.assign = function (target) {
      'use strict';
      // We must check against these specific cases.
      if (target === undefined || target === null) {
        throw new TypeError('Cannot convert undefined or null to object');
      }

      var output = Object(target);
      for (var index = 1; index < arguments.length; index++) {
        var source = arguments[index];
        if (source !== undefined && source !== null) {
          for (var nextKey in source) {
            if (source.hasOwnProperty(nextKey)) {
              output[nextKey] = source[nextKey];
            }
          }
        }
      }
      return output;
    };
  })();
}

// developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach#Polyfill
if (!Array.prototype.forEach) {
  Array.prototype.forEach = function(callback, thisArg) {
    var T, k;
    if (this === null) {
      throw new TypeError(' this is null or not defined');
    }
    var O = Object(this);
    var len = O.length >>> 0;
    if (typeof callback !== "function") {
      throw new TypeError(callback + ' is not a function');
    }
    if (arguments.length > 1) {
      T = thisArg;
    }
    k = 0;
    while (k < len) {
      var kValue;
      if (k in O) {
        kValue = O[k];
        callback.call(T, kValue, k, O);
      }
      k++;
    }
  };
}
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */
