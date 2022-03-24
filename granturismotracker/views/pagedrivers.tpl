% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <% for driver in drivers: %>
        <div class="flex-column mv-xs p-xs bg-checkered" onclick="onDriver({{driver.id}})">
            <% points = "{0:.{1}f}".format(driver.points, 3) %>
            <% points_past = "{0:.{1}f}".format(driver.points_past, 3) %>
            <% points_current = "{0:.{1}f}".format(driver.points_current, 3) %>
            <div class="flex-row mv-xs">
                <img class="image-s mr-xs" src="/static/images/driver.png">
                <div class="flex-1 flex-hl flex-vc foswald fs-s">{{driver.name}}</div>
                <div class="flex-1 flex-hr flex-vc foswald fs-s"><strong>{{points}}</strong></div>
                <img class="image-s ml-xs" src="/static/images/points.png">
            </div>
            <div class="flex-row mv-xs">
                <img class="image-s mr-xs" src="/static/images/rank.png">
                <div class="flex-1 flex-hl flex-vc foswald fs-s">{{driver.rank}}</div>
                <div class="flex-1 flex-hr flex-vc foswald fs-s"><div class="fg-red">{{points_past}}</div></div>
                <img class="image-s ml-xs" src="/static/images/pointspast.png">
            </div>
            <div class="flex-row mv-xs">
                <img class="image-s mr-xs" src="/static/images/sessions.png">
                <div class="flex-1 flex-hl flex-vc foswald fs-s">{{driver.sessions}}</div>
                <div class="flex-1 flex-hr flex-vc foswald fs-s"><div class="fg-green">{{points_current}}</div></div>
                <img class="image-s ml-xs" src="/static/images/pointscurrent.png">
            </div>
        </div>
    <% end %>
</div>

<script>
function onDriver(id) {
    window.location.href = "/drivers/details/" + id;
}
</script>

% include("footer.tpl")
% include("htmlfooter.tpl")
