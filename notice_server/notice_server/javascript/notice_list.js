import {format_dates_in_notice} from "./utils.js"
import {show_alert} from "./show_alert.js"

const table_data_fields = [
    "notice_id",
    "name",
    "forename",
    "last_fetched_date",
    "last_modified_date",
    "first_fetched_date"
];

const make_view_button_cell = (url) => {
    const view_btn_cell = document.createElement("td");
    const view_button = document.createElement("button");
    view_button.classList.add("btn", "btn-outline-primary", "btn-stretch");
    view_button.innerText = "View";
    view_button.addEventListener("click", () => {
        window.location.href = url;
    });
    view_btn_cell.append(view_button);
    return view_btn_cell;
}

const add_new_notice_row = (data) => {
    const table_body = document.querySelector("#notices_table tbody");
    const new_row = document.createElement("tr");
    new_row.id = "notice_row_" + data.notice_id;
    table_data_fields.forEach(key => {
        const new_cell = document.createElement("td");
        new_cell.textContent = data[key];
        new_row.append(new_cell);
    });
    const path = `/notice/${data.notice_id}`;
    new_row.append(make_view_button_cell(path));
    table_body.append(new_row);
}
const update_existing_notice_row = (data, row) => {
    for (let i = 0; i < table_data_fields.length; i++) {
        const key = table_data_fields[i];
        const new_value = data[key];
        if (new_value !== undefined) {
            row.children[i].innerText = new_value;
        }
    }
}
const add_notice_to_table = (data) => {
    const row_id = "notice_row_" + data.notice_id;
    const row = document.getElementById(row_id)
    format_dates_in_notice(data);
    if (row === null) add_new_notice_row(data);
    else update_existing_notice_row(data, row);
}
async function fetch_and_populate_table(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Got http status code: ${response.status}`);
        }
        const notices_data = await response.json();
        notices_data.forEach(notice_data => {
            add_notice_to_table(notice_data);
        });
    } catch (err) {
        console.log(`Failed to load notice list: ${err}`);
    }
}

const socket = io.connect()
socket.on("notice_update", (data) => {
  const notice_id = data.notice_id
  const update_type = data.update_type;
  const changed_data = data.changed_data;
  add_notice_to_table(changed_data);
  show_alert(`Notice: ${notice_id} ${update_type}`, "success");

})
fetch_and_populate_table("/api/notice_list");
