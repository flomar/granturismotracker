% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <% for car in cars: %>
        <div class="flex-row mv-xs p-xs bg-checkered">
            <img class="image-s mr-xs" src="/static/images/car.png">
            <div class="flex-w50 flex-hl flex-vc foswald fs-s">{{car.name}}</div>
            <div class="flex-1 flex-hr flex-vc foswald fs-s">{{car.sessions}}</div>
            <img class="image-s ml-xs" src="/static/images/sessions.png">
        </div>
    <% end %>
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
