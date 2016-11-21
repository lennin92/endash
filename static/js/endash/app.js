/**
 * Created by Lennin Hernandez on 20/11/2016.
 */


'use strict';

//App principal
var visualifeApp=angular.module('endashApp',[
    'ngRoute',
    'ngCookies',
    'ngResource',
    'uiGmapgoogle-maps',
    'MapControllers',
    'NodeControllers'
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
}]).config(['uiGmapGoogleMapApiProvider',
    function(uiGmapGoogleMapApiProvider) {
        uiGmapGoogleMapApiProvider.configure({
            key: __GOOGLE_API_KEY__,
            v: '3',
            libraries: 'weather,geometry,visualization'
    });
}]);
