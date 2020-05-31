$(function () {
    $("#refresh-div").hide()

    $('#refresh-btn').click(function () {
        location.reload()
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.update(tabs[0].id, { url: tabs[0].url });
        });
    });


    // $('#description').hide();
    // $('#see-description').click(function () {
    //     $('#see-description').hide();
    //     $('#description').show();
    // });


    var currentState = null
    chrome.storage.sync.get(['currentState'], function (result) {
        console.log('Value currently is ' + result.currentState);
        currentState = result.currentState
        console.log("Current " + currentState)
        var $toggleBtn = $("#toggle-btn");

        if (currentState === "stop") {
            $toggleBtn.text("OFF");
            $toggleBtn.removeClass("btn-success")
            $toggleBtn.addClass("btn-danger")
        }
        else if (currentState === "start") {
            $toggleBtn.text("ON");
            $toggleBtn.removeClass("btn-danger")
            $toggleBtn.addClass("btn-success")
        }
        else {
            chrome.storage.sync.set({ "currentState": "start" }, function () {
                $toggleBtn.text("ON");
                $toggleBtn.removeClass("btn-danger")
                $toggleBtn.addClass("btn-success")
                console.log("First set to start")
            });
            currentState = "start"
        }

        $toggleBtn.click(function () {
            if (currentState === "start") {
                $toggleBtn.text("OFF");
                $toggleBtn.removeClass("btn-success")
                $toggleBtn.addClass("btn-danger")
                chrome.storage.sync.set({ "currentState": "stop" }, function () {
                    console.log("Set to stop")
                });
            }
            else if (currentState === "stop") {
                $toggleBtn.text("ON");
                $toggleBtn.removeClass("btn-danger")
                $toggleBtn.addClass("btn-success")
                chrome.storage.sync.set({ "currentState": "start" }, function () {
                    console.log("Set to start")
                });

            }
            else {
                chrome.storage.sync.set({ "currentState": "stop" }, function () {
                    console.log("Last set to stop")
                });
            }
            $("#refresh-div").show()
        });
    });
});