% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <div class="flex-column mv-xs p-xs bg-checkered">
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
            <img class="image-s mr-xs" src="/static/images/sessions.png">
            <div class="flex-1 flex-hl flex-vc foswald fs-s">{{driver.sessions}}</div>
            <div class="flex-1 flex-hr flex-vc foswald fs-s"><div class="fg-red">{{points_past}}</div>&nbsp;|&nbsp;<div class="fg-green">{{points_current}}</div></div>
            <img class="image-s ml-xs" src="/static/images/points.png">
        </div>
    </div>
    <div class="flex-column mv-xs p-xs bg-checkered">
        <div class="flex-row mv-xs">
            <div class="flex-column flex-1 flex-hc flex-vc">
                <img class="animate__animated animate__infinite animate__pulse image-m" src="/static/images/gold.png">
                <div class="flex-1 flex-hc flex-vc mt-xs foswald fs-s">{{gold}}</div>
            </div>
            <div class="flex-column flex-1 flex-hc flex-vc">
                <img class="animate__animated animate__infinite animate__pulse image-m" src="/static/images/silver.png">
                <div class="flex-1 flex-hc flex-vc mt-xs foswald fs-s">{{silver}}</div>
            </div>
            <div class="flex-column flex-1 flex-hc flex-vc">
                <img class="animate__animated animate__infinite animate__pulse image-m" src="/static/images/bronze.png">
                <div class="flex-1 flex-hc flex-vc mt-xs foswald fs-s">{{bronze}}</div>
            </div>
        </div>
    </div>
    <% for record in records: %>
        <% date_time = record.date_time.strftime("%Y-%m-%d %H:%M:%S") %>
        <% pps = "{0:.{1}f}".format(record.pps, 3) %>
        <% time_minutes = int(int(record.time) / int(60 * 1000)) %>
        <% time_seconds = int(int(record.time - time_minutes * 60 * 1000) / int(1000)) %>
        <% time_milliseconds = int(int(record.time - time_minutes * 60 * 1000 - time_seconds * 1000)) %>
        <% time = "{:01d}:{:02d}.{:03d}".format(time_minutes, time_seconds, time_milliseconds) %>
        <div class="flex-row mv-xs p-xs bg-checkered" style="position: relative;">
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
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{record.car.name}} ({{pps}})</div>
                </div>
                <div class="flex-row mv-xs">
                    <img class="image-s mr-xs" src="/static/images/time.png">
                    <div class="flex-1 flex-hl flex-vc foswald fs-s">{{time}}</div>
                </div>
                <% if record.gold: %>
                    <div class="flex-1 flex-hc flex-vc" style="position: absolute; left: 0; right: 0; top: 0; bottom: 0">
                        <div class="flex-1 flex-hc flex-vc w-25" style="position: absolute; left: 75%; right: 0; top: 0; bottom: 0;">
                            <img class="animate__animated animate__infinite animate__pulse image-l" src="/static/images/gold.png">
                        </div>
                    </div>
                <% elif record.silver: %>
                    <div class="flex-1 flex-hc flex-vc" style="position: absolute; left: 0; right: 0; top: 0; bottom: 0">
                        <div class="flex-1 flex-hc flex-vc w-25" style="position: absolute; left: 75%; right: 0; top: 0; bottom: 0;">
                            <img class="animate__animated animate__infinite animate__pulse image-l" src="/static/images/silver.png">
                        </div>
                    </div>
                <% elif record.bronze: %>
                    <div class="flex-1 flex-hc flex-vc" style="position: absolute; left: 0; right: 0; top: 0; bottom: 0">
                        <div class="flex-1 flex-hc flex-vc w-25" style="position: absolute; left: 75%; right: 0; top: 0; bottom: 0;">
                            <img class="animate__animated animate__infinite animate__pulse image-l" src="/static/images/bronze.png">
                        </div>
                    </div>
                <% end %>
            </div>
        </div>
    <% end %>
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
