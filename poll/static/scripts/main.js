"use strict";$.support.cors=!0;var baseUrl="http://localhost:3000/poll",showScores=function(o){$("#content").show(),$("#dog1Score").html(o.dog1+"%"),$("#dog2Score").html(o.dog2+"%")},showError=function(){$("#content").hide(),$("#error").show()},getScores=function(){$.ajax({url:baseUrl+"/scores",method:"GET"}).done(showScores).fail(showError)},voteDog1=function(){$.ajax({url:baseUrl+"/vote/dog1",method:"POST"}).always(getScores)},voteDog2=function(){$.ajax({url:baseUrl+"/vote/dog2",method:"POST"}).always(getScores)};$("#voteDog1").on("click",voteDog1),$("#voteDog2").on("click",voteDog2),getScores();