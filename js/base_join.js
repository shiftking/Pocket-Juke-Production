var google = google || {};

  //window.alert("somthing 1");
google.appengine = google.appengine || {};
  //  window.alert("somthing 2");
google.appengine.pocket_juke = google.appengine.pocket_juke || {};
//  window.alert("somthing 3");
google.appengine.pocket_juke.party = google.appengine.pocket_juke.party || {};
//  window.alert("somthing 4");


//handle the printing of the individual parties for the list of parties that is to be dispalyed to the user
google.appengine.pocket_juke.party.print_party = function(resp,row){
  var table_row = document.createElement('tr');
  //element.classList.add('row');
  var party_name = document.createElement('td');
  party_name.setAttribute('id','party_name_'+(row+1));
  party_name.innerHTML = resp.name;

  var attending = document.createElement('td');
  attending.innerHTML = 0;
  var join_button = document.createElement('button');
  var join_column = document.createElement('td');
  join_button.classList.add('btn-default');
  join_button.classList.add('btn');
  join_button.setAttribute('id','party_'+(row+1));
  join_button.innerHTML = "Join";
  join_column.appendChild(join_button);
  table_row.appendChild(party_name);
  table_row.appendChild(attending);
  table_row.appendChild(join_column);
  //element.innerHTML = resp.name;
  document.querySelector('#party_list').appendChild(table_row);
  google.appengine.pocket_juke.party.addlistener(row);
};
//function to access the api call for joining a Party
google.appengine.pocket_juke.party.join_party = function(name){
  gapi.client.pocket_juke_api.pocket_juke.join_party({
    'name':name
  }).execute(function(resp){
      if(!resp.code){

      }
  });
};
//fucntion to acces the api call for searching a party by its name
google.appengine.pocket_juke.party.get_parties = function(
  party_name,offset){
    gapi.client.pocket_juke_api.pocket_juke.get_parties({
      'name': party_name,
      'offset': offset
    }).execute(function(resp){
      if(!resp.code){
        if(resp.Parties.length > 0){
          for( var i =0; i< resp.Parties.length; i++){
            google.appengine.pocket_juke.party.print_party(resp.Parties[i],i);
          }
        }
      }
    });
};
//function to handle the api call for adding the party
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


google.appengine.pocket_juke.party.enableButtons = function(){
  //setting up listener for the add party button
  //window.alert("somthing adding party getting values from fields");



  var searchParty = document.querySelector('#search_for_party');
  searchParty.addEventListener('click',function(e){
    google.appengine.pocket_juke.party.get_parties(
      document.querySelector('#party_seach').value,0
    )
  })


};



google.appengine.pocket_juke.party.addlistener = function(id){
  var join_party = document.querySelector('#party_'+(id+1));
  join_party.addEventListener('click',function(e){
    var party_name = document.querySelector('#party_name_'+(id+1));
    google.appengine.pocket_juke.party.join_party(party_name.innerHTML);
  })
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
