% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <div class="flex-1 flex-hc frusso fs-m fg-blue-light">Events</div>
    <% for event in events: %>
        <% date_time = event.date_time.strftime("%A, %Y-%m-%d %H:%M:%S") %>
        <% if event.date_time >= now: %>
            <div class="flex-1 flex-hc m-xs foswald fs-s fg-blue-light">{{date_time}}</div>
        <% else: %>
            <div class="flex-1 flex-hc m-xs foswald fs-s fg-blue-light"><s>{{date_time}}</s></div>
        <% end %>
    <% end %>
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
