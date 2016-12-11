/**
 * Created by Lennin Hernandez on 20/11/2016.
 */


'use strict';

//App principal
var visualifeApp=angular.module('endashApp',[
    'ngRoute',
    'ngCookies',
    'ngResource',
    'ngMap',
    'chart.js',
    'MapControllers',
    'NodeControllers',
    'ngMaterial'
]);


/*RUN*/
visualifeApp.run(function($http) {
    // Add validation to CSRF
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.headers.common['Content-Type']='application/json';
});

/*Configuracion general del modulo principal, se asigna por cada ruta, una view y un controlador*/
visualifeApp.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
        when('/', {
            templateUrl:'/static/js/endash/views/main.html',
            controller:'MapController',
            controllerAs:'controller'
        }).
        when('/nodes/:nodeId/', {
            templateUrl:'/static/js/endash/views/node.html',
            controller:'NodeController',
            controllerAs:'controller'
        }).
        otherwise({
            redirectTo:'/'
    });
}]);
    /*.config(['$mdThemingProvider', function($mdThemingProvider){

    $mdThemingProvider.theme('default').primaryPalette('red',{
        'default':'900'
    }).accentPalette('cyan', {
        'hue-3':'50',
        'hue-2':'800'
    }).warnPalette('orange', {
        'hue-3':'400'
    });
}]); */
