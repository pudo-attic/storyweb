storyweb.directive('storywebLink', ['$http', 'cfpLoadingBar', function($http, cfpLoadingBar) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'parent': '=',
      'link': '='
    },
    templateUrl: 'link.html',
    link: function (scope, element, attrs, model) {
      scope.mode = 'view';
      scope.card = {};
      scope.expanded = false;

      scope.$watch('link', function(l) {
        if (l) scope.card = l.child;
      });

      var saveCard = function() {
        cfpLoadingBar.start();
        var url = '/api/1/cards/' + scope.card.id;
        $http.post(url, scope.card).then(function(res) {
          scope.card = res.data;
          cfpLoadingBar.complete();
        });
      };

      var saveLink = function() {
        cfpLoadingBar.start();
        var url = '/api/1/cards/' + scope.parent.id + '/links/' + scope.link.id;
        scope.link.rejected = scope.link.status == 'rejected';
        $http.post(url, scope.link).then(function(res) {
          scope.link = res.data;
          cfpLoadingBar.complete();
        });
      };

      scope.mouseIn = function() {
        scope.$emit('highlight', scope.card.aliases);
      };

      scope.mouseOut = function() {
        scope.$emit('clearHighlight');
      };

      scope.toggleMode = function() {
        if (scope.editMode()) {
          saveCard();
        }
        scope.mode = scope.mode == 'view' ? 'edit' : 'view';
      };

      scope.toggleRejected = function() {
        if (scope.link.status == 'rejected') {
          scope.link.status = 'approved';
        } else {
          scope.link.status = 'rejected';
        }
        saveLink();
      };

      scope.expandCard = function() {
        scope.expanded = !scope.expanded;
      };

      scope.editMode = function() {
        return scope.mode == 'edit';
      };

      scope.viewMode = function() {
        return scope.mode == 'view';
      };

      scope.hasReferences = function() {
        return scope.card.references && scope.card.references.length > 0;
      };

      scope.hasText = function() {
        return scope.card.text && scope.card.text.length > 0;
      };

      scope.hasAliases = function() {
        return scope.card.aliases && scope.card.aliases.length > 1;
      };
    }
  };
}]);
