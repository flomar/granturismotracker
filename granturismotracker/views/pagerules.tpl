% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <div class="flex-1 flex-hc frusso fs-m fg-blue-light mv-s">Sessions</div>
    <p class="mv-xs foswald fs-s fg-blue-light">Whenever a driver gets into the seat, a new session is started.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">The time limit for each session is 15 minutes, and when that time limit expires, the session ends. If the driver is on a hot lap when the time limit expires, the driver may finish the lap. After the end of the session, the best lap is submitted. If not a single lap was completed, a zero lap will be submitted.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">Note that the submission of a zero lap also applies if the driver decides to change track or car without having finished at least a single lap first. The addition and removal of tuning parts does not warrant the submission of a zero lap, unless, of course, no lap was finished with the either the old tune or the new tune.</p>
    <div class="flex-1 flex-hc frusso fs-m fg-blue-light mv-s">Tracks & Cars</div>
    <p class="mv-xs foswald fs-s fg-blue-light">All tracks are raced in dry weather, and the time of day may be chosen by the driver.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">With regards to tires, street cars are restricted Sports Soft (SS), and race cars are restricted to Racing Soft (RS).</p>
    <p class="mv-xs foswald fs-s fg-blue-light">All other settings can be changed at the discretion of the driver, including the addition and removal of tuning parts.</p>
    <div class="flex-1 flex-hc frusso fs-m fg-blue-light mv-s">Driving</div>
    <p class="mv-xs foswald fs-s fg-blue-light">At all times, two wheels must remain on track.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">If that rule is broken in the eyes of race control, a retry of the session should be initiated.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">If the driver refuses to initiate a retry, race control reserves the right to investigate the incident further using instant replay after the current lap is finished, and then end the session prematurely and submit a zero lap if appropriate.</p>
    <div class="flex-1 flex-hc frusso fs-m fg-blue-light mv-s">Scoring</div>
    <p class="mv-xs foswald fs-s fg-blue-light">The score for each driver is recalculated after each session, and it consists of two components, one for current performance and one for past performance:</p>
    <p class="mv-xs foswald fs-s fg-blue-light">First, the fastest driver on any combination of track and car is awarded 100 points for current performance, and the slower drivers are awarded proportionally less points. For example, if the fastest driver set a lap time of 1:00.000, then that driver would be awarded 100 points, whereas drivers with a lap time of 2:00.000 would be awarded only 50 points, as 2:00.000 is only half as fast as 1:00.000.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">Second, the longer gold, silver, and bronze records remain unbeaten, the more points for past performance the corresponding drivers are awarded. For example, for each session not resulting in a faster lap time than a gold, silver, and bronze record, the corresponding drivers are awarded 1.0, 0.25, and 0.125 points, respectively, on top of their points earned for current performance.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">Note that the points for current performance are fully dynamic in that they can be taken away by other drivers, but the points for past performance are not.</p>
    <p class="mv-xs foswald fs-s fg-blue-light">Furthermore, for reasons of fairness, the points for current performance are adjusted with regards to the in-game performance points (PPs) of each car when a record is set. For example, if the fastest lap was submitted with 500 PPs at 1:00.000, and the second-fastest lap was submitted with 250 PPs at 2:00.000, both laps yield 100 points for current performance.</p>
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
