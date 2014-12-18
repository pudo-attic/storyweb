storyweb.directive('storywebCardItem', ['$http', '$location', function($http, $location) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'card': '='
    },
    templateUrl: 'card_item.html',
    link: function (scope, element, attrs, model) {
      scope.visit = function() {
        $location.search({});
        $location.path('/cards/' + scope.card.id);
      }

      scope.relDate = function() {
        return moment(scope.card.updated_at).fromNow();
      }
    }
  };
}]);
