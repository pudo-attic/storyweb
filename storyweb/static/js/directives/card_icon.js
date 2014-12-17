storyweb.directive('storywebCardIcon', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'category': '='
    },
    templateUrl: 'card_icon.html',
    link: function (scope, element, attrs, model) {
    }
  };
}]);
