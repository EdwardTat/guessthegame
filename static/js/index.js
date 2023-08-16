let app = {};


let init = (app) => {

    app.data = {
        list_categories: [],
        test: "hi",
        checkGameData: false,
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.categories_load = function () {
        axios.get(get_categories_url, { params: {} }).then(function (r) {
            app.vue.list_categories = r.data.categories;
            app.vue.checkGameData = r.data.playerData;
            app.enumerate(app.vue.list_categories);
        });
    };

    app.openPopup = function () {
        axios.get(get_player_stat_info_url, {params: {}}).then(function (response) {
            console.log("r.data.output == ", response.data.output);
            temp = window.location.href;
            if (temp.includes("/index")) {
                temp = temp.replace("/index", "");
            }

            window.open(temp + "/stats/" + response.data.output, "Popup Window", "width=600,height=700");
        });
    };



    app.quiz_selection = function (cat_name) {
        console.log("cat_name = " + cat_name);
        temp = window.location.href;
        if (temp.includes("/index")) {
            temp = temp.replace("/index", "");
        }
        window.location.href = temp + `/category/${cat_name}`;



        //window.location.href = `/final_project/category/${cat_name}`;
        // axios.get(`/f/quizzes/${cat_name}`, { params: {} })
        //     .then(response => {
        //         //window.location.href = response.data.redirect;

        //     });
    };


    app.methods = {
        categories_load: app.categories_load,
        quiz_selection: app.quiz_selection,
        openPopup: app.openPopup,
    };


    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });


    app.init = () => {
        app.vue.categories_load();

    };

    app.init();
};

init(app);
