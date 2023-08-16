let app = {};


let init = (app) => {

    app.data = {
        quizName: initialData.quizName
    };

     app.methods = {

    };


    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });


    app.init = () => {
    };

    app.init();
};

init(app);
