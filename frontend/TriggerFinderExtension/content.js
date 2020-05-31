// var images = document.getElementsByTagName('img');
// for (var i = 0, l = images.length; i < l; i++) {
//   images[i].src = 'http://placekitten.com/' + images[i].width + '/' + images[i].height;
// }

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}


function httpPost(url, element)
{
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr){
        xhr.open("POST", url, true);
    } else if (typeof XDomainRequest != "undefined"){
        xhr = new XDomainRequest();
        xhr.open("POST", url);
    } else {
        xhr = null;
    }

    if(xhr != null)
    {
        value = element.innerHTML
        element.innerHTML = "The text is being examined"        
    
        xhr.onreadystatechange = function () {
            console.log("Changed " + this.readyState)
            if (xhr.readyState != 4) return;
    
            if (xhr.status == 200) {
                response = JSON.parse(xhr.response);
                element.innerHTML = response["response"]
            }
            else
            {
                element.innerHTML = "error"
                console.log("Error")
            }
        };

        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            text: value
        }));
    }
    
}

isOn = true

elements = ["p", "li", "h1", "h2"]

if(isOn)
{
    // httpPost("http://127.0.0.1:5000/predictText", document.body)
    var all = document.getElementsByTagName("*");

    for (var i=0; i < all.length; i++) {
        console.log(all[i].tagName)
        if(elements.includes(all[i].tagName.toLowerCase()))
        {
            console.log(all[i].innerHTML)
            httpPost("http://127.0.0.1:5000/predictText", all[i])
        }
    }
}