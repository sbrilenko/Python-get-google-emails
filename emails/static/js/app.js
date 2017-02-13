'use strict';

var app = angular.module('App', []);

app.constant('API', {
    'emails': '/emails'
});

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[{').endSymbol('}]');
});
