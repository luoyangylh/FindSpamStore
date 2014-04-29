//var restaurantList = {};

function begin() {
    var list = document.getElementById("list");
            console.log(spamList[i]);
        var scroll = document.createElement("div");
        scroll.className = "listScroll";
    for (var i = 0; i < 20; i++) {

        var div = document.createElement("div");

        div.className = "spam";
        var a = document.createElement("a");
        // var id = document.createElement("h5");
        a.textContent = spamList[i]["name"];
        console.log(spamList[i]["business_id"]);
        a.href = 'javascript:search("'+spamList[i]["business_id"]+'");';
        // a.onClick = "hello";
        // function() {
        //     search(spamList[i]["business_id"]);
        //     console.log(spamList[i]["business_id"]);
        // }
        //"search("+spamList[i]["business_id"]+");"

        // = "search("+spamList[i]["business_id"]+");";
        // a.appendChild(id);
        var s = document.createElement("h5");
        s.textContent = "Scores difference: " + spamList[i]["diff"].toFixed(3);
        div.appendChild(a);
        div.appendChild(s);
        scroll.appendChild(div);
    }
    list.appendChild(scroll);
}

function setup(storeName) {

    // var myData = JSON.parse("/data/restaurant_ranked_reviewers.json", function (key, value) {
    //     // var type;
    //     // if (value && typeof value === 'object') {
    //     //     type = value.type;
    //     //     if (typeof type === 'string' && typeof window[type] === 'function') {
    //     //         return new (window[type])(value);
    //     //     }
    //     // }
    //     // return value;
    //     for(var i=0;i<10;i++){
    //     	console.log(key);
    //     	console.log(value);
    //     }
    // });
    // console.log(myData);

    // for(var i=0; i<RESTAURANT.length;i++){
    // 	console.log(RESTAURANT[i]["name"]);
    // restaurantList[RESTAURANT[i]["name"]] = RESTAURANT[i];


    // }

    console.log(restaurantList);

    var store = document.getElementById("store");
    while (store.firstChild) {
        store.removeChild(store.firstChild);
    }


    var name = document.createElement("h3");
    //console.log(storeName);
    name.textContent = restaurantList[storeName]["name"];
    var hr = document.createElement("hr");

    var addr = document.createElement("h4");
    addr.textContent = restaurantList[storeName]["full_address"];
    var our_score = document.createElement("h4");
    our_score.textContent = "Our Score: " + restaurantList[storeName]["our_score"].toFixed(2);
    our_score.className = "score";
    var stars = document.createElement("h4");
    stars.textContent = "Official Stars: " + restaurantList[storeName]["stars"];
    stars.className = "score";


    store.appendChild(name);
    store.appendChild(hr);
    store.appendChild(addr);
    store.appendChild(our_score);
    store.appendChild(stars);

    var div = document.createElement("div");
    div.className = "reviews";

    for (var i = 0; i < REVIEWS[restaurantList[storeName]["business_id"]].length; i++) {
    	var user = document.createElement("h5");
    	user.className = "userName";
    	user.textContent = REVIEWS[restaurantList[storeName]["business_id"]][i]["userName"]
        var review = document.createElement("h5");
        review.className = "review"
        review.textContent = REVIEWS[restaurantList[storeName]["business_id"]][i]["review"];
        div.appendChild(user);
        div.appendChild(review);
    }

    store.appendChild(div);









}

function search(searchID) {

    // console.log("search");
    // var searchID = document.getElementById("search");
    //console.log(searchID);
    searchStore = restaurantList[searchID]["name"];
    //console.log("NAME!!!!!!!");
    //console.log(searchStore);

    setup(searchID);
    var words = searchStore.split(" ");
    var searchWords = "";
    for (var i = 0; i < words.length; i++) {
        searchWords = searchWords + "+" + words[i];
    }
    var loc = restaurantList[searchID]["full_address"].split(" ");
    var searchLocation = "";
    for (var i = 0; i < loc.length; i++) {
        searchLocation = searchLocation + "+" + loc[i];
    }

    // console.log("ADDR!!!!!!!");
    // console.log(searchWords);
    // console.log(searchLocation);


    // console.log(searchWords);
    var frame = document.getElementById("frame");
    frame.src = "http://www.yelp.com/search?find_desc=" + searchWords + "&find_loc=" + searchLocation;



}


// Object.prototype.getKeyByValue = function( value ) {
//     for( var prop in this ) {
//         if( this.hasOwnProperty( prop ) ) {
//              if( this[ prop ] === value )
//                  return prop;
//         }
//     }
// }
