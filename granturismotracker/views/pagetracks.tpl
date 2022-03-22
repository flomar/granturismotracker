% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    % for track in tracks:
        <div class="flex-row mv-xs p-xs bg-blue-dark">
            <img class="image-s mr-xs" src="/static/images/track.png">
            <div class="flex-w50 flex-hl flex-vc foswald fs-s">{{track.name}}</div>
            <div class="flex-1 flex-hr flex-vc foswald fs-s">{{track.sessions}}</div>
            <img class="image-s ml-xs" src="/static/images/sessions.png">
        </div>
    % end
</div>

% include("footer.tpl")
% include("htmlfooter.tpl")
