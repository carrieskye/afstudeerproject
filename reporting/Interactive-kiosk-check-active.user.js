// ==UserScript==
// @name         Interactive-kiosk-check-active
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.torfs.be/*
// @grant        none
// @require http://code.jquery.com/jquery-3.3.1.min.js
// ==/UserScript==

(function() {
    // check if user is active part
    var idleState = false;
    var idleTimer = null;

    const ws = new WebSocket("ws://localhost:5001/");
    ws.onopen = function () {
        ws.send("socket open on remote page");
    };


    $('*').bind('mousemove click mouseup mousedown keydown keypress keyup submit change mouseenter scroll resize dblclick', function () {
        clearTimeout(idleTimer);
        if (idleState == true) {
            ws.send('active');
        }
        idleState = false;
        idleTimer = setTimeout(function () {
            ws.send('idle');
            idleState = true; }, 5 * 1000);
    });
    $("body").trigger("mousemove");
    // end


})();