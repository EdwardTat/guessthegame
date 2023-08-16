let app = {};


let init = (app) => {

    app.data = {
        username: '',
        wins: 0,
        losses: 0,
        winPercentage: '',
        avgGuesses: '',
        qt: [],
        users: [],
    };

    app.enumerate = (a) => {
        let k = 1;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.annotate_qt = (a) => {
        let k = 0;
        let x = 0;
        let y = 0;
        app.vue.wins = 0;
        app.vue.losses = 0;
        a.map((e) => {
            let text = "";
            if (e.status == 1) {
                app.vue.wins++;
                text = "Won In ";
                text = text.concat(e.guesses);
                if (e.guesses == 1) {
                    text = text.concat(" Guess!");
                } else {
                    text = text.concat(" Guesses!");
                }
                x = x + e.guesses;
            } else if (e.status == -1) {
                app.vue.losses = app.vue.losses + 1;
                text = "Couldn't Guess It Right";
            } else {
                text = ""
                text = text.concat(5 - e.guesses);
                if (e.guesses == 5) {
                    text = text.concat(" Guess Left");
                } else {
                    text = text.concat(" Guesses Left");
                }
            }
            console.log("text = " + text);
            e.text = text;

            if (app.vue.wins == 0) {
                app.vue.avgGuesses = 0;
            } else {
                app.vue.avgGuesses = (x / app.vue.wins);
            }
            if (app.vue.losses + app.vue.wins == 0) {
                app.vue.winPercentage = 100;
            } else {
                app.vue.winPercentage = (app.vue.wins / (app.vue.losses + app.vue.wins)) * 100;
            }
        })
    }

    app.stats_load = function (i) {
        axios.get(player_stats_load_url, { params: { playerId: i } })
            .then(function (r) {
                console.log("uname = " + r.data.uname);
                app.vue.username = r.data.uname;
                app.vue.qt = r.data.gamedata;
                app.annotate_qt(app.vue.qt);
                if (r.data.gamedata == null) {
                    app.vue.winPercentage = 0;
                }
                app.enumerate(app.vue.qt);
            });
    },

        app.load_users = function () {
            console.log("in here")
            axios.get(load_users_url, {})
                .then(function (r) {
                    app.vue.users = r.data.output;
                    console.log(app.vue.users[1].id)
                });
        }


    app.methods = {
        annotate_qt: app.annotate_qt,
        stats_load: app.stats_load,
        enumerate: app.enumerate,
        load_users: app.load_users,
    };


    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });


    app.init = () => {
        app.vue.load_users();
        app.vue.stats_load(initialData.playerId);

    };

    app.init();
};

init(app);
