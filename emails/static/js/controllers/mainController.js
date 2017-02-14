'use strict';

angular.module('App')
    .controller('MainCtrl', ['$http', '$window', 'API', function ($http, $window, API) {
        var main = this;
        main.emails = [];

        main.getMails = function () {
            main.loading = true;
            $http({ 'method': 'GET', 'url': API.emails })
                .then(
                    function (emails) {
                        main.emails = emails.data;
                        main.loading = false;
                    },
                    function (err) {
                        main.loading = false;
                        if (err.status === 403) {
                            $window.location.href = '/logout';
                        } else {
                            main.error = 'Can\'t get your emails. Try again later.';
                        }
                    }
                );
        };

        main.getMails();
    }]);