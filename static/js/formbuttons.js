$(function(){
    $('#btnCreateVPS').click(function(){

        // Form validation - user must enter Name and Description for processing to occur

        if (document.forms["vps"]["name"].value == "") {
            document.getElementById("valName").innerHTML = "Name must be filled out";
            return(false)
        }

        if (document.forms["vps"]["description"].value == "") {
            document.getElementById("valDescription").innerHTML = "Description must be filled out";
            return(false)
        }

        // Show animation while VPS is being created

        $("#loading").show();
        $("#content").hide();

        $.ajax({
            url: '/createVPS',
            data: $('form').serialize(),
            type: 'POST',

            // If it gets this far redirect to homepage passing vpsadded=yes argument
            success: function(response){
                window.location.href = "/?vpsadded=yes";
            },

            // Display error in browser console
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#btnUpdateVPS').click(function(){
        
        $.ajax({
            url: '/updateVPS',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                window.location.href = "/modifyVPS?id=" + response + "&updated=yes";
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#btnCreateDisk').click(function(){
        
        $.ajax({
            url: '/createDisk',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                window.location.href = "/modifyVPS?id=" + response + "&updated=yes";
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#btnUpdateDisk').click(function(){
        
        $.ajax({
            url: '/updateDisk',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                window.location.href = "/modifyVPS?id=" + response + "&updated=yes";
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#btnCreateNetwork').click(function(){
        
        $.ajax({
            url: '/createNetwork',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                window.location.href = "/modifyVPS?id=" + response + "&updated=yes";
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#btnCreateUser').click(function(){

        if (document.forms["createUser"]["inputName"].value == "") {
            document.getElementById("valName").innerHTML = "Name must be filled out";
            return(false)
        }

        if (document.forms["createUser"]["inputEmail"].value == "") {
            document.getElementById("valEmail").innerHTML = "Email must be filled out";
            return(false)
        }

        if (document.forms["createUser"]["inputPassword"].value == "") 
        {
            document.getElementById("valPassword").innerHTML = "Password must be filled out";
            return(false)
        }
        
        $.ajax({
            url: '/createUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                //console.log(response);
                window.location.href = "/UserManagement?useradded=yes";
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    $('#btnUpdateUser').click(function(){
        
        $.ajax({
            url: '/updateUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                var  args = response.split(',');

                if (args[1] == "User Updated") 
                    window.location.href = "/UserManagement?userupdated=yes";
                else
                    window.location.href = "/modifyUser?id=" + args[0] + "&error=" + args[1];
            },
            error: function(error){
                console.log(error);
            }
        });
    });

});