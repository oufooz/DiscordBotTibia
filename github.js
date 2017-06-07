var fs = require('fs');
var page = require('webpage').create();

page.open('https://secure.tibia.com/community/?subtopic=worlds&world=Hydera', function(status) {
    if (status !== 'success') {
        console.log('Unable to access network');
    } else {
        var content = page.evaluate(function(){
            x = document.getElementsByClassName("Odd");
            listOfPlayers = [];
            for(i =0;  i < x.length;i++){
                listOfPlayers.push(x[i].innerText);
            }
            x = document.getElementsByClassName("Even");
            for(i =0;  i < x.length;i++){
                listOfPlayers.push(x[i].innerText);
            }
            return listOfPlayers;
        });
        
        console.log("Content Length : " + content.length);
    /*    for(i =0;  i < content.length;i++){
    //       console.log(content[i]);
        }    */ 
        page.render('github.png');

        fs.write("output.txt",content,'w');
    }
    phantom.exit();
});

