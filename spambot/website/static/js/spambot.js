window.Spam = Backbone.Model.extend({
    
})

window.SpamFactory = {
    get_next_spam : function(){
        console.log("Getting next spam!")
    }
}


window.WelcomeView = Backbone.View.extend({

    el: "#content",

    template: _.template($('#welcome_template').html()),
    
    initialize:function () {
    },

    events:{
        "click #showMeBtn":"showMeBtnClick"
    },

    render:function () {
        $(this.el).html(this.template());
        return this;
    },

    showMeBtnClick:function () {
        app.headerView.search();
    }

});


window.RecordView = Backbone.View.extend({
    

})


var AppRouter = Backbone.Router.extend({

    routes: {
        ""                  : "welcome",
        "/record"           : "record", 
        
        // "wines/page/:page"	: "list",
        // "wines/add"         : "addWine",
        // "wines/:id"         : "wineDetails",
        // "about"             : "about"
    },

    initialize: function () {
        
    },

    welcome: function() {
        if (!this.welcome_view) {
            this.welcome_view = new WelcomeView();
        }
        
        this.welcome_view.render()
    },

    record: function() {
        this.record_view = new RecordView();
    }
    

});

app = new AppRouter();
Backbone.history.start();


