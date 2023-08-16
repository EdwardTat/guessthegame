let app = {};


let init = (app) => {

    app.data = {
        list_quizzes: [],
    };

    app.annotate_quizes = (a, b) => {
        let k = 0;
        var temp = 0;
        a.map((e) => {
            console.log("\nfor " + e.id);
            temp = b.indexOf(e.id);
            e.ownerStatus = (temp !== -1);
            console.log("owner status = " + e.ownerStatus);

        })
    }

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };


    app.load_quizzes = (categoryName) => {
        axios.get(get_quizzes_url, { params: { categoryName: categoryName } }).then(function (response) {
            app.vue.list_quizzes = app.enumerate(response.data.quizzes);
            app.annotate_quizes(app.vue.list_quizzes, response.data.owned);
        });
    }

    app.delete_quiz_entry = function (id) {
        axios.post(delete_quiz_url, {
            quizId: id,
        }).then(function (r) {
            app.load_quizzes(initialData.categoryName);
        })
    }

    app.enter_quiz = (quizID) => {
        //temp = window.location.href;
        //temp = temp.substring(0, temp.lastIndexOf('category/'));
        //console.log("cat name = " + temp);
        //window.location.href = `/final_project/quiz/${quizID}`;

        window.location.href = window.location.href.substring(
            0, window.location.href.lastIndexOf('/category/' + initialData.categoryName)) +
            `/quiz/${quizID}`;
    },

    app.add_game = () => {
        console.log("Needs Implement " + initialData.categoryName)
            //return "/add_game/"+ encodeURIComponent(initialData.categoryName)
            //window.location.href = "Project/static/add_game/"+initialData.categoryName;
        window.location.href = window.location.href.substring(
            0, window.location.href.lastIndexOf('/category/' + initialData.categoryName)) + '/add_game/' + initialData.categoryName;
    },

    app.edit_quiz =(quizid) =>{
        window.location.href = window.location.href.substring(
            0, window.location.href.lastIndexOf('/category/' + initialData.categoryName)) +
            `/edit_quiz/${quizid}`;
    },

    app.methods = {
        load_quizzes: app.load_quizzes,
        enter_quiz: app.enter_quiz,
        add_game: app.add_game, //needs implement
        annotate_quizes: app.annotate_quizes,
        delete_quiz_entry: app.delete_quiz_entry,
        edit_quiz: app.edit_quiz,
    };


    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });


    app.init = () => {
        app.vue.load_quizzes(initialData.categoryName);
    };

    app.init();
};

init(app);
