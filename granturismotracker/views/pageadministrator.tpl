% include("htmlheader.tpl")
% include("header.tpl")

<div class="flex-column m-s">
    <div class="foswald fs-m mh-s mt-m mb-s">Create Events</div>
    <form id="form_events_create" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_events_create_action">
            <input class="w-75 mv-xs" id="form_events_create_input_date_time_event_date_time" name="form_events_create_input_date_time_event_date_time" type="datetime-local" pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}">
            <input class="w-75 mv-xs" type="submit" value="Create">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Delete Events</div>
    <form id="form_events_delete" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_events_delete_action">
            <select class="w-75 mv-xs" id="form_events_delete_select_event_date_time" name="form_events_delete_select_event_date_time">
                <% for event in events: %>
                    <option value="{{event.date_time}}">{{event.date_time}}</option>
                <% end %>
            </select>
            <input class="w-75 mv-xs" id="form_events_delete_input_button_delete" type="button" value="Delete" onclick="onFormEventsDeleteInputButtonDelete()">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Create Drivers</div>
    <form id="form_drivers_create" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_drivers_create_action">
            <input class="w-75 mv-xs" id="form_drivers_create_input_text_driver_name" name="form_drivers_create_input_text_driver_name" type="text" placeholder="Name...">
            <input class="w-75 mv-xs" type="submit" value="Create">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Delete Drivers</div>
    <form id="form_drivers_delete" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_drivers_delete_action">
            <select class="w-75 mv-xs" id="form_drivers_delete_select_driver_name" name="form_drivers_delete_select_driver_name">
                <% for driver in drivers: %>
                    <option value="{{driver.name}}">{{driver.name}}</option>
                <% end %>
            </select>
            <input class="w-75 mv-xs" id="form_drivers_delete_input_button_delete" type="button" value="Delete" onclick="onFormDriversDeleteInputButtonDelete()">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Create Tracks</div>
    <form id="form_tracks_create" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_tracks_create_action">
            <input class="w-75 mv-xs" id="form_tracks_create_input_text_track_name" name="form_tracks_create_input_text_track_name" type="text" placeholder="Name...">
            <input class="w-75 mv-xs" type="submit" value="Create">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Delete Tracks</div>
    <form id="form_tracks_delete" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_tracks_delete_action">
            <select class="w-75 mv-xs" id="form_tracks_delete_select_track_name" name="form_tracks_delete_select_track_name">
                <% for track in tracks: %>
                    <option value="{{track.name}}">{{track.name}}</option>
                <% end %>
            </select>
            <input class="w-75 mv-xs" id="form_tracks_delete_input_button_delete" type="button" value="Delete" onclick="onFormTracksDeleteInputButtonDelete()">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Create Cars</div>
    <form id="form_cars_create" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_cars_create_action">
            <input class="w-75 mv-xs" id="form_cars_create_input_text_car_name" name="form_cars_create_input_text_car_name" type="text" placeholder="Name...">
            <input class="w-75 mv-xs" type="submit" value="Create">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Delete Cars</div>
    <form id="form_cars_delete" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_cars_delete_action">
            <select class="w-75 mv-xs" id="form_cars_delete_select_car_name" name="form_cars_delete_select_car_name">
                <% for car in cars: %>
                    <option value="{{car.name}}">{{car.name}}</option>
                <% end %>
            </select>
            <input class="w-75 mv-xs" id="form_cars_delete_input_button_delete" type="button" value="Delete" onclick="onFormCarsDeleteInputButtonDelete()">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Create Records</div>
    <form id="form_records_create" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_records_create_action">
            <select class="w-75 mv-xs" id="form_records_create_select_driver_name" name="form_records_create_select_driver_name">
                <% for driver in drivers: %>
                    <option value="{{driver.name}}">{{driver.name}}</option>
                <% end %>
            </select>
            <select class="w-75 mv-xs" id="form_records_create_select_track_name" name="form_records_create_select_track_name">
                <% for track in tracks: %>
                    <option value="{{track.name}}">{{track.name}}</option>
                <% end %>
            </select>
            <select class="w-75 mv-xs" id="form_records_create_select_car_name" name="form_records_create_select_car_name">
                <% for car in cars: %>
                    <option value="{{car.name}}">{{car.name}}</option>
                <% end %>
            </select>
            <input class="w-75 mv-xs" id="form_records_create_input_text_record_pps" name="form_records_create_input_text_record_pps" type="text" placeholder="PPs [000.000]...">
            <input class="w-75 mv-xs" id="form_records_create_input_text_record_time" name="form_records_create_input_text_record_time" type="text" placeholder="Time [00:00.000]...">
            <input class="w-75 mv-xs" type="submit" value="Create">
        </div>
    </form>
    <div class="foswald fs-m mh-s mt-m mb-s">Delete Records</div>
    <form id="form_records_delete" action="" method="post">
        <div class="flex-column ml-s">
            <input type="hidden" id="action" name="action" value="form_records_delete_action">
            <select class="w-75 mv-xs" id="form_records_delete_select_record" name="form_records_delete_select_record">
                <% for record in records: %>
                    <% date_time = record.date_time.strftime("%Y-%m-%d %H:%M:%S") %>
                    <% pps = "{0:.{1}f}".format(record.pps, 3) %>
                    <% time_minutes = int(int(record.time) / int(60 * 1000)) %>
                    <% time_seconds = int(int(record.time - time_minutes * 60 * 1000) / int(1000)) %>
                    <% time_milliseconds = int(int(record.time - time_minutes * 60 * 1000 - time_seconds * 1000)) %>
                    <% time = "{:01d}:{:02d}.{:03d}".format(time_minutes, time_seconds, time_milliseconds) %>
                    <option value="{{record.id}}">[{{date_time}}] {{record.driver.name}} / {{record.track.name}} / {{record.car.name}} ({{pps}}) / {{time}}</option>
                <% end %>
            </select>
            <input class="w-75 mv-xs" id="form_records_delete_input_button_delete" type="button" value="Delete" onclick="onFormRecordsDeleteInputButtonDelete()">
        </div>
    </form>
</div>

<script>
function onFormEventsDeleteInputButtonDelete() {
    if(confirm("Are you sure?")) {
        document.getElementById("form_events_delete").submit();
    }
}
function onFormDriversDeleteInputButtonDelete() {
    if(confirm("Are you sure?")) {
        document.getElementById("form_drivers_delete").submit();
    }
}
function onFormTracksDeleteInputButtonDelete() {
    if(confirm("Are you sure?")) {
        document.getElementById("form_tracks_delete").submit();
    }
}
function onFormCarsDeleteInputButtonDelete() {
    if(confirm("Are you sure?")) {
        document.getElementById("form_cars_delete").submit();
    }
}
function onFormRecordsDeleteInputButtonDelete() {
    if(confirm("Are you sure?")) {
        document.getElementById("form_records_delete").submit();
    }
}
</script>

% include("footer.tpl")
% include("htmlfooter.tpl")
