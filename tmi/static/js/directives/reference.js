storyweb.directive('storywebReference', ['$http', function($http) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'story': '=',
      'card': '=',
      'reference': '='
    },
    templateUrl: 'reference.html',
    link: function (scope, element, attrs, model) {

    }
  };
}]);
