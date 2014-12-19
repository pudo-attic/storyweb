// this is derived from: 
// https://github.com/thijsw/angular-medium-editor

storyweb.directive('mediumEditor', function() {
  return {
    require: 'ngModel',
    restrict: 'AE',
    scope: {
    },
    link: function(scope, iElement, iAttrs, ctrl) {

      angular.element(iElement).addClass('angular-medium-editor');

      // Parse options
      var placeholder = '',
          opts = {
            'buttons': ["bold", "italic", "anchor", "header1", "header2", "quote", "orderedlist"],
            'cleanPastedHTML': true
          };

      var onChange = function() {
        scope.$apply(function() {

          // If user cleared the whole text, we have to reset the editor because MediumEditor
          // lacks an API method to alter placeholder after initialization
          if (iElement.html() === '<p><br></p>' || iElement.html() === '') {
            opts.placeholder = placeholder;
            var editor = new MediumEditor(iElement, opts);
          }

          ctrl.$setViewValue(iElement.html());
        });
      };

      // view -> model
      iElement.on('blur', onChange);
      iElement.on('input', onChange);

      // model -> view
      ctrl.$render = function() {

        if (!this.editor) {
          // Hide placeholder when the model is not empty
          if (!ctrl.$isEmpty(ctrl.$viewValue)) {
            opts.placeholder = '';
          }

          this.editor = new MediumEditor(iElement, opts);
        }

        iElement.html(ctrl.$isEmpty(ctrl.$viewValue) ? '' : ctrl.$viewValue);
        
        // hide placeholder when view is not empty
        if(!ctrl.$isEmpty(ctrl.$viewValue)) {
          angular.element(iElement).removeClass('medium-editor-placeholder');
        }
      };

    }
  };

});
