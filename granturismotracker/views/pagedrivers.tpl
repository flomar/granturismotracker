% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    % for driver in drivers:
        <div class="flex-column mv-xs p-xs bg-blue-dark">
            <% points = "{0:.{1}f}".format(driver.points, 3) %>
            <div class="flex-row mv-xs">
                <img class="image-s mr-xs" src="/static/images/driver.png">
                <div class="flex-1 flex-hl flex-vc foswald fs-s">{{driver.name}}</div>
                <div class="flex-1 flex-hr flex-vc foswald fs-s">{{driver.rank}}</div>
                <img class="image-s ml-xs" src="/static/images/rank.png">
            </div>
            <div class="flex-row mv-xs">
                <img class="image-s mr-xs" src="/static/images/sessions.png">
                <div class="flex-1 flex-hl flex-vc foswald fs-s">{{driver.sessions}}</div>
                <div class="flex-1 flex-hr flex-vc foswald fs-s">{{points}}</div>
                <img class="image-s ml-xs" src="/static/images/points.png">
            </div>
        </div>
    % end
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
