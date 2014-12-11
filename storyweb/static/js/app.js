var storyweb = angular.module('storyweb', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'angular-loading-bar', 'contenteditable', 'truncate']);

storyweb.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
  cfpLoadingBarProvider.latencyThreshold = 100;
}]);

storyweb.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {

  $routeProvider.when('/', {
    templateUrl: 'article_list.html',
    controller: 'ArticleListCtrl'
  });

  $routeProvider.when('/cards/:id', {
    templateUrl: 'card.html',
    controller: 'CardCtrl'
  });

  $routeProvider.when('/search', {
    templateUrl: 'search.html',
    controller: 'SearchCtrl'
  });

  $routeProvider.otherwise({
    redirectTo: '/'
  });

  $locationProvider.html5Mode(false);
}]);
