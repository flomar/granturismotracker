% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <% if len(reports) > 0: %>
        <div class="flex-1 flex-hc frusso fs-m fg-blue-light mv-s">Reports</div>
        <% for report in reports: %>
            <% date_time = report.date_time.strftime("%Y-%m-%d %H:%M:%S") %>
            <% pps = "{0:.{1}f}".format(report.pps, 3) %>
            <% time_minutes = int(int(report.time) / int(60 * 1000)) %>
            <% time_seconds = int(int(report.time - time_minutes * 60 * 1000) / int(1000)) %>
            <% time_milliseconds = int(int(report.time - time_minutes * 60 * 1000 - time_seconds * 1000)) %>
            <% time = "{:01d}:{:02d}.{:03d}".format(time_minutes, time_seconds, time_milliseconds) %>
            <% performance = "{0:.{1}f}".format(report.performance, 3) %>
            <div class="flex-row mv-xs p-xs bg-checkered">
                <div>
                    <% if report.time == 0: %>
                    [{{date_time}}]&nbsp;<span class="fg-report-highlight">{{report.driver.name}}</span>&nbsp;completely&nbsp;<span class="fg-report-highlight">shit the bed</span>&nbsp;at&nbsp;<span class="fg-report-highlight">{{report.track.name}}</span>&nbsp;driving the&nbsp;<span class="fg-report-highlight">{{report.car.name}}</span>&nbsp;({{pps}}).
                    <% elif report.gold: %>
                    [{{date_time}}]&nbsp;<span class="fg-report-highlight">{{report.driver.name}}</span>&nbsp;performed for&nbsp;<span class="fg-report-highlight">{{performance}}</span>&nbsp;points and won a&nbsp;<span class="fg-report-highlight">gold</span>&nbsp;badge at&nbsp;<span class="fg-report-highlight">{{report.track.name}}</span>&nbsp;driving the&nbsp;<span class="fg-report-highlight">{{report.car.name}}</span>&nbsp;({{pps}}) with a time of &nbsp;<span class="fg-report-highlight">{{time}}</span>.
                    <% elif report.silver: %>
                    [{{date_time}}]&nbsp;<span class="fg-report-highlight">{{report.driver.name}}</span>&nbsp;performed for&nbsp;<span class="fg-report-highlight">{{performance}}</span>&nbsp;points and won a&nbsp;<span class="fg-report-highlight">silver</span>&nbsp;badge at&nbsp;<span class="fg-report-highlight">{{report.track.name}}</span>&nbsp;driving the&nbsp;<span class="fg-report-highlight">{{report.car.name}}</span>&nbsp;({{pps}}) with a time of &nbsp;<span class="fg-report-highlight">{{time}}</span>.
                    <% elif report.bronze: %>
                    [{{date_time}}]&nbsp;<span class="fg-report-highlight">{{report.driver.name}}</span>&nbsp;performed for&nbsp;<span class="fg-report-highlight">{{performance}}</span>&nbsp;points and won a&nbsp;<span class="fg-report-highlight">bronze</span>&nbsp;badge at&nbsp;<span class="fg-report-highlight">{{report.track.name}}</span>&nbsp;driving the&nbsp;<span class="fg-report-highlight">{{report.car.name}}</span>&nbsp;({{pps}}) with a time of &nbsp;<span class="fg-report-highlight">{{time}}</span>.
                    <% else: %>
                    [{{date_time}}]&nbsp;<span class="fg-report-highlight">{{report.driver.name}}</span>&nbsp;performed for&nbsp;<span class="fg-report-highlight">{{performance}}</span>&nbsp;points at&nbsp;<span class="fg-report-highlight">{{report.track.name}}</span>&nbsp;driving the&nbsp;<span class="fg-report-highlight">{{report.car.name}}</span>&nbsp;({{pps}}) with a time of &nbsp;<span class="fg-report-highlight">{{time}}</span>.
                    <% end %>
                </div>
            </div>
        <% end %>
    <% end %>
    <% if len(events) > 0: %>
        <div class="flex-1 flex-hc frusso fs-m fg-blue-light mv-s">Events</div>
        <% for event in events: %>
            <% date_time = event.date_time.strftime("%A, %Y-%m-%d %H:%M:%S") %>
            <% if event.date_time_expiration >= now: %>
                <div class="flex-1 flex-hc m-xs foswald fs-s fg-blue-light">{{date_time}}</div>
            <% else: %>
                <div class="flex-1 flex-hc m-xs foswald fs-s fg-blue-light"><s>{{date_time}}</s></div>
            <% end %>
        <% end %>
    <% end %>
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
