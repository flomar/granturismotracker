% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    % for record in records:
        <% date_time = record.date_time.strftime("%Y-%m-%d %H:%M:%S") %>
        <% time_minutes = int(int(record.time) / int(60 * 1000)) %>
        <% time_seconds = int(int(record.time - time_minutes * 60 * 1000) / int(1000)) %>
        <% time_milliseconds = int(int(record.time - time_minutes * 60 * 1000 - time_seconds * 1000)) %>
        <% time = "{:01d}:{:02d}.{:03d}".format(time_minutes, time_seconds, time_milliseconds) %>
        <div class="flex-row mv-xs p-xs bg-blue-dark">
            <div class="flex-column flex-1">
                <div class="flex-row mv-xs">
                    <img class="image-s mr-xs" src="/static/images/datetime.png">
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{date_time}}</div>
                </div>
                <div class="flex-row mv-xs">
                    <img class="image-s mr-xs" src="/static/images/driver.png">
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{record.driver.name}}</div>
                </div>
                <div class="flex-row mv-xs">
                    <img class="image-s mr-xs" src="/static/images/track.png">
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{record.track.name}}</div>
                </div>
                <div class="flex-row mv-xs">
                    <img class="image-s mr-xs" src="/static/images/car.png">
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{record.car.name}}</div>
                </div>
                <div class="flex-row mv-xs">
                    <img class="image-s mr-xs" src="/static/images/time.png">
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{time}}</div>
                </div>
            </div>
            <div class="flex-column flex-w25 flex-hc flex-vc">
                % if record.gold:
                    <img class="image-l" src="/static/images/gold.png">
                % end
                % if record.silver:
                    <img class="image-l" src="/static/images/silver.png">
                % end
                % if record.bronze:
                    <img class="image-l" src="/static/images/bronze.png">
                % end
            </div>
        </div>
    % end
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
