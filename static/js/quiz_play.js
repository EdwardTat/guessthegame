let app = {};


let init = (app) => {

    app.data = {
        current_quiz: [], //database row for current quiz
        current_guess: '', //users current guess
        tryNum: 1,// how many guesses the user has made. (To display image)
        current_image_index: 1,
        current_image: '',//image to display in html
        succeedStatus: 0, //whether or not the user succeeded
        comments: [],
        cbar: '',
        game_upvote_status: 0,
        answerOptions: [],
    };

    app.load_comments = function (id) {
        axios.get(get_comments_url, {
            params: {
                gameId: id
            }
        }).then(function (r) {

            app.vue.comments = r.data.output;
            app.enumerate(app.vue.comments);
            app.annotate_comments(app.vue.comments, r.data.upvoteData,
                r.data.upvoteStatus, r.data.ownerStatus);
        });
    }

    app.reply_button_function = function (i) {
        app.vue.cbar = "@" + app.vue.comments[i].author + " |  \n\n" + app.vue.cbar;
    }

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.annotate_comments = (a, b, c, d) => {
        let k = 0;
        var temp = 0, i = 0;
        a.map((e) => {
            e.utime = Sugar.Date(e.time).relative();
            temp = b.indexOf(e.id);
            if (temp !== -1) {
                e.ustat = c[temp];
            } else {
                e.ustat = 0;
            }

            e.ownerStatus = d[i];
            i++;
        });
        return a;
    }

    app.setImageIndex = (imageIndex) => {
        app.vue.current_image_index = imageIndex;
        let image = "image" + imageIndex;
        app.vue.current_image = app.vue.current_quiz[0][image];
    }

    app.delete_post = function (i) {
        axios.post(delete_comment_url, {
            postId: app.vue.comments[i].id,
        }).then(function (r) {
            app.load_comments(initialData.quizID);
        });
    }



    app.redirect = (url) => {
        temp = window.location.href.substring(0, window.location.href.lastIndexOf('/'));
        temp = temp.substring(0, temp.lastIndexOf('/'));
        window.location.href = temp + `${url}`;
        //console.log("website redirect = " + temp + `/${url}`);
        //window.location.href = `/final_project/${url}`;
    }

    app.backToMenu = () => {
        app.redirect("/category/" + app.vue.current_quiz[0]["categoryName"]);
    }


    //retrieves quiz from database and puts it into vue variable current_quiz
    app.getQuiz = function (id) {
        axios.post(get_quiz,
            {
                quiz_id: id
            })
            .then(function (response) {
                app.vue.current_quiz = response.data.quiz;
                app.vue.tryNum = 1;
                app.vue.current_image_index = 1;
                let image = "image" + this.current_image_index;
                app.vue.current_image = app.vue.current_quiz[0][image];
                if (response.data.playdata == null) {
                    app.vue.succeedStatus = 0;
                    app.vue.tryNum = 1;
                    app.vue.current_image_index = 1;
                    console.log("null called\n")
                    console.log("current image index = " + app.vue.current_image_index);

                } else {
                    app.vue.succeedStatus = response.data.playdata.status;
                    if (response.data.playdata.status == -1) {
                        app.vue.current_image_index = 1
                    } else {
                        app.vue.current_image_index = response.data.playdata.guesses;
                    }
                    app.vue.tryNum = response.data.playdata.guesses;
                }
                app.vue.game_upvote_status = response.data.gameUpvoteStatus;
                console.log("gup");
                console.log("r data status = " + response.data.gameUpvoteStatus);
                console.log("current image index = " + app.vue.current_image_index);
                app.setImageIndex(app.vue.current_image_index);
                console.log("playdata = " + response.data.playdata + "\n");
            });
    }


    //check if guess is right
    app.checkGuess = function () {
        axios.post(game_state_update_url,
            {
                guess: app.vue.current_guess,
                answer: app.vue.current_quiz[0].answer,
                tryNum: app.vue.tryNum,
                quizId: initialData.quizID,

            }).then(function (r) {
                app.vue.succeedStatus = r.data.status;
                app.vue.tryNum = r.data.tryNum;
                if (app.vue.succeedStatus != 0)
                    return;
                if (app.vue.current_image_index < 6) {
                    app.vue.current_image_index += 1;
                }
                let image = "image" + app.vue.current_image_index;
                app.vue.current_image = app.vue.current_quiz[0][image];
            })
    }

    app.upvote_process = function (i, order) {
        axios.post(comment_upvote_process_url, {
            upvote: order,
            post: app.vue.comments[i].id,
        }).then(function (r) {
            if (app.vue.comments[i].ustat === order) {
                app.vue.comments[i].ustat = 0;
            } else {
                app.vue.comments[i].ustat = order;
            }
            app.vue.comments[i].likeRatio = r.data.total;
        });
    }

    app.game_upvote_process = function (order) {
        axios.post(game_upvote_process_url, {
            game: initialData.quizID,
            order: order
        }).then(function (r) {

            app.vue.game_upvote_status = r.data.status;
        });
    }

    app.save_comment = function () {
        axios.post(comment_post_process_url, {
            post: app.vue.cbar,
            gameId: initialData.quizID,
        }).then(function (r) {
            app.vue.cbar = '';
            app.load_comments(initialData.quizID);
        });
    }

    app.get_answers = function () {
        axios.get(get_answers_url, { params: { qid: initialData.quizID } }).then(function (response) {
            app.vue.answerOptions = response.data.answers;
        });
    }

    app.methods =
    {
        setImageIndex: app.setImageIndex,
        redirect: app.redirect,
        backToMenu: app.backToMenu,
        getQuiz: app.getQuiz,
        checkGuess: app.checkGuess,
        load_comments: app.load_comments,
        save_comment: app.save_comment,
        enumerate: app.enumerate,
        annotate_comments: app.annotate_comments,
        upvote_process: app.upvote_process,
        reply_button_function: app.reply_button_function,
        delete_post: app.delete_post,
        game_upvote_process: app.game_upvote_process,
        get_answers: app.get_answers,
    };

    app.computed = {
        filteredAnswerOptions() {
            return this.answerOptions.filter(option => {
                if (typeof this.current_guess === 'string') {
                    return option.toLowerCase().indexOf(this.current_guess.toLowerCase()) !== -1;
                }
                return false;
            }).slice(0, 10);
        }
    };








    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
        computed: app.computed,
    });


    app.init = () => {
        app.vue.getQuiz(initialData.quizID);
        app.vue.load_comments(initialData.quizID);
        app.vue.get_answers();
    };

    app.init();
};

init(app);
