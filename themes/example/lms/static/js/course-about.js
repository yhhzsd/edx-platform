
(function(require) {
    require(['edx-ui-toolkit/js/utils/html-utils'], function(HtmlUtils) {
        "use strict"
        $(function() {
            // Truncating the Course Description
            var entireDescriptionContent = $(".course-description").html();
            truncateDescription(entireDescriptionContent);

            // Truncating the Course learning points
            var entireLearningContent = $(".course-learning .list-bulleted").html();
            truncateLearningPoints(entireLearningContent);

        });

      $(window).load(function(){
            $(".instructor-image").leanModal({closeButton: ".modal_close", top: '10%'});
      });

      function expandDescription(entireDescriptionContent) {
         var showLessLinkHtml = '<a id="description_less" href="#" class="brand-link">Less</a>';
         HtmlUtils.setHtml(".course-description", HtmlUtils.HTML(entireDescriptionContent + showLessLinkHtml));
         $("#description_less").click(function(event) {
             event.preventDefault();
             truncateDescription(entireDescriptionContent);
         });
      }

      function truncateDescription(entireDescriptionContent) {
          if (entireDescriptionContent.length > 500) {
            var truncatedContent = entireDescriptionContent.substring(0, entireDescriptionContent.indexOf(" ", 500));
            var showMoreLinkHtml = '... <a id="description_show" href="#" class="brand-link">See More</a>';
            HtmlUtils.setHtml(".course-description", HtmlUtils.HTML(truncatedContent + showMoreLinkHtml));
            $("#description_show").click(function (event) {
                event.preventDefault();
                expandDescription(entireDescriptionContent);
            });
          }
      }

      function expandLearningPoints(entireLearningContent){
          var showLessLinkHtml = '<a id="learning_less" href="#" class="brand-link learning-points-btn">Less</a>';
          HtmlUtils.setHtml(".course-learning .list-bulleted", HtmlUtils.HTML(entireLearningContent + showLessLinkHtml));
          $("#learning_less").click(function(event){
              truncateLearningPoints(entireLearningContent);
          });
      }

      function truncateLearningPoints(entireLearningContent) {
          var learning_points_count = $(".course-learning .list-bulleted").children().length;
          if (learning_points_count > 6) {
              $(".course-learning .list-bulleted").children().slice((6 - learning_points_count)).remove();
              var showMoreLinkHtml = '<a id="learning_show" href="#" class="brand-link learning-points-btn">See More</a>';
              HtmlUtils.append(".course-learning .list-bulleted", HtmlUtils.HTML(showMoreLinkHtml));
              $("#learning_show").click(function (event) {
                  event.preventDefault();
                  expandLearningPoints(entireLearningContent);
              });
          }
      }
    });
}).call(this, require || RequireJS.require);
