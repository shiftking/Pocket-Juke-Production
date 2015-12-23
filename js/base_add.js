var google = google || {};

  //window.alert("somthing 1");
google.appengine = google.appengine || {};
  //  window.alert("somthing 2");
google.appengine.pocket_juke = google.appengine.pocket_juke || {};
//  window.alert("somthing 3");
google.appengine.pocket_juke.party = google.appengine.pocket_juke.party || {};
//  window.alert("somthing 4");





/*


//handles the get response for the party api, searches for a specific party name
google.appengine.pocket_juke.party.getParty = function(name){
  gapi.client.pocket_juke.party.get_Party
}
google.appengine.pocket_juke.party.enableButtons =  function(){
  var getParty = document.querySelector('#party_name');
  getParty.addEventListener('click',function(e){

  })
}


google.appengine.
*/
google.appengine.pocket_juke.party.print_add_resp = function(resp){
  window.alert(resp);
}


//function to access the api call for adding party to the list of parties, it calls the function add party which is deffined in the python script
google.appengine.pocket_juke.party.add_party = function(
  party_name,code){
    //window.alert("somthing submitting submission for party");
    gapi.client.pocket_juke_api.pocket_juke.add_party({
      'name': party_name,
      'pass_code': code
    }).execute(function(resp){
      if(!resp.code){
        google.appengine.pocket_juke.party.print_add_resp(resp.response);
      }
    });
  }

//adding the event listers for the buttons
//general function statement
google.appengine.pocket_juke.party.enableButtons = function(){
  //setting up listener for the add party button
  //window.alert("somthing adding party getting values from fields");
  var addParty = document.querySelector('#add_party');
  addParty.addEventListener('click',function(e){
    //window.alert("somthing adding party");
    //calls the function defined in this js file
    google.appengine.pocket_juke.party.add_party(
      document.querySelector('#party_name').value,document.querySelector('#party_code').value
    );

  });
  


};

/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
google.appengine.pocket_juke.party.init = function(apiRoot) {
  // Loads the OAuth and helloworld APIs asynchronously, and triggers login
  // when they have completed.

  var apisToLoad;
  var callback = function() {
    if (--apisToLoad == 0) {
      google.appengine.pocket_juke.party.enableButtons();
    }
  }
  //window.alert("somthing in init");
  apisToLoad = 1; // must match number of calls to gapi.client.load()
  gapi.client.load('pocket_juke_api', 'v1', callback, apiRoot);
};
