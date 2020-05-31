// document.addEventListener('DOMContentLoaded', function() {
//     var checkPageButton = document.getElementById('checkPage');
//     checkPageButton.addEventListener('click', function() {
  
//       chrome.tabs.getSelected(null, function(tab) {
//         d = document;
  
//         var f = d.createElement('form');
//         f.action = 'http://gtmetrix.com/analyze.html?bm';
//         f.method = 'post';
//         var i = d.createElement('input');
//         i.type = 'hidden';
//         i.name = 'url';
//         i.value = tab.url;
//         f.appendChild(i);
//         d.body.appendChild(f);
//         f.submit();

//         console.log(f.action)
//       });
//     }, false);
//   }, false);

// $(function(){
//   //default value is "start"
  
//   //cache button DOM element reference
  

//   //update button status
  

//   //register button click handler
//   $toggleBtn.click(function(){
//       if(currentState==="start"){
//           $toggleBtn.text("OFF");
//           localStorage.currentState="stop";
//       }
//       if(currentState==="stop"){
//           $toggleBtn.text("ON");
//           localStorage.currentState="start";
//       }
//   });
// });

