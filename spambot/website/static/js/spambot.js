
VALID_PHONE_NUMBER = /^\+[0-9]*$/;



window.Spam = Backbone.Model.extend()

window.SpamHolder = Backbone.Collection.extend({
    model: Spam,
    url: "/spam",
})

window.CallStatus = Backbone.Model.extend({
    urlRoot : "/callstatus"
})

window.CallStatusView = Backbone.View.extend({
    el: "#callback_container",

    call_statuses : 
    { "ringing" :
      {"style":"info",
       "message" : "We're currently ringing your phone, you should receive a call very soon."},
      "in-progress" :
      {"style":"info",
       "message" : "Please follow the instructions laid out in the call. When you're finished speaking, just hang up."},
       "completed" :
       {"style":"success",
        "message" : "Your recording has been logged successfully, thanks for taking part!"},
      "failed" :
      {"style":"error",
       "message" : "Sorry, something appears to have gone wrong! If you have time, refresh the page and try again. Thanks!"},
      "busy" : 
       {"style":"error",
        "message": "We tried to call you but you were engaged. If you have time, refresh the page and try again. Thanks!"},
       "no-answer":
       {"style":"error",
        "message": "Sadly we couldn't reach you. If you have time, refresh the page and try again. Thanks!"}
    },

    template: _.template("<span class='text-<%=style%>'><%=message%></span>"),
    
    initialize: function() {
        this.poller = PollingManager.getPoller(this.model);
        this.model.on("change", this.render, this)
        this.poller.start()
    },

    render: function() {
        var status = this.model.get("status")
        this.$el.html(this.template(this.call_statuses[status]))
        if(!_.include(["ringing", "in-progress"], status)){
            this.poller.stop()
        }
    }
})

window.RecordView = Backbone.View.extend({
    el: "#record",

    template: _.template($("#record_template").html()),

    events: {
        "click #refresh_spam" : "refresh_spam",
        "submit #callback_form" : "create_callback",
        "focus #phone_number" : "hide_errors"  
    },
    
    initialize: function() {
        this.collection.on("reset", this.render, this)
    },

    spam: function() {
        return this.collection.models[0]
    },
    
    render: function () {
        $(this.el).html(this.template(this.spam().toJSON()));
        $("#phone_number").tooltip(
            {"title" : "To create an Intl Phone Number from a U.K. number drop the '0' and add '+44'. <br/>For exmaple, 07428262123 should become +447428262123",
             "trigger" : "focus",
             "placement" : "right",
            })
        return this;
    },

    refresh_spam : function() {
        this.collection.fetch()
    },

    hide_errors: function() {
        $("#phone_help").hide()
    },
    
    create_callback : function() {

        var number = $("#phone_number").val()

        if(! VALID_PHONE_NUMBER.test(number)){
            $("#phone_help").show()
            return false;
        }
        
        var topic = this.spam().get("topic")
        var id = this.spam().id
        that = this;
        
        $.post('/call',
               {"to_number" : number, "topic" : topic, "spam_id": id},
 	       function(response_data) {
                   var call_sid = JSON.parse(response_data)
                   var callstatus = new CallStatus({"id" : call_sid})
                   var callstatus_view = new CallStatusView({"model": callstatus})
               });
        
        return false;
    }
    
})


var AppRouter = Backbone.Router.extend({
    routes: {
        ""          : "welcome",
        "record"    : "new_recording", 
    },

    initialize : function() {
        
    },
    
    _show_instructions_if_required : function() {
        if($.cookie('should_show_instructions') == null){
            $('#instructions_modal').modal("show");
            $.cookie('should_show_instructions', '1');
        }
    },

    _transition_out : function(selector) {
        $(selector).effect("slide", { "direction" : "left",  "mode" : "hide"}, 1000)
    },

    _transition_in : function(selector, callback) {
        $(selector).effect("slide", {"direction" : "right", "mode" : "show"}, 1000, callback)
    },
    
    welcome: function() {
        $("#record").hide()
        $("#welcome").show()
    },
    
    new_recording: function() {
        this.spam_holder = new SpamHolder()
        this.record_view = new RecordView({collection: this.spam_holder})
        this._transition_out("#welcome")
        this._transition_in(this.record_view.el, this._show_instructions_if_required)
        this.spam_holder.fetch()
    }
});

app = new AppRouter();
Backbone.history.start();


