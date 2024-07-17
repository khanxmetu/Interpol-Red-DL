export const format_dates_in_notice = (data) => {
    if (data.last_fetched_date !== undefined) {
        data.last_fetched_date = convert_date_to_human_readable(new Date(data.last_fetched_date));
    }
    if (data.last_modified_date !== undefined) {
        data.last_modified_date = convert_date_to_human_readable(new Date(data.last_modified_date));
    }
    if (data.first_fetched_date !== undefined) {
        data.first_fetched_date = convert_date_to_human_readable(new Date(data.first_fetched_date));
    }

    if (data.date_of_birth !== undefined) {
        data.date_of_birth = get_date_string(new Date(data.date_of_birth));
    }
}

const get_time_string = (date_obj) => {
    const options = { hour: "numeric", minute: "numeric", hour12: true };
    return date_obj.toLocaleTimeString("en-US", options);
}

const get_date_string = (date_obj) => {
    const options = { year: "numeric", month: "numeric", day: "numeric" };
    return date_obj.toLocaleDateString("en-US", options);
}
const convert_date_to_human_readable = (date_obj) => {
    const timeStr = get_time_string(date_obj);
    const dateStr = get_date_string(date_obj);
    return `${timeStr} ${dateStr}`;;
}


