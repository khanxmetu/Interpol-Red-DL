import { format_dates_in_notice, get_cache_busted_url } from "./utils.js"
import { show_alert } from "./show_alert.js"
import {COUNTRIES, LANGUAGES, EYES, HAIRS, SEXES} from "./abbreviations_data.js"

const NOTICE_ID = document.getElementById("notice_det_id").innerText

const get_fullnames_from_codes = (codes, dict) => {
    if (!codes) return "N/A";
    const fullnames = codes.map(code => dict[code]);
    return fullnames.join(", ");
}

const create_list_item = (label_text, value_text) => {
    const list_item = document.createElement("li");
    list_item.classList.add("list-group-item");

    const label = document.createElement("strong");
    label.textContent = label_text;

    list_item.append(label);
    list_item.append(document.createTextNode(value_text));

    return list_item;
};

const populate_arrest_warrant = (charge, translation, issuing_country) => {
    if (!charge) charge = "N/A";
    if (!translation) translation = "N/A";
    if (!issuing_country) issuing_country = "N/A";
    const main_container = document.getElementById("notice_det_warrants");
    const warrant_container = document.createElement("ul");
    warrant_container.classList.add("list-group", "list-group-flush");

    const charge_item = create_list_item("Charge: ", charge);
    const translation_item = create_list_item("Charge Translation: ", translation);
    const issuing_country_item = create_list_item("Issuing Country: ", issuing_country);

    warrant_container.append(charge_item, translation_item, issuing_country_item);
    main_container.append(warrant_container);
};

const populate_text_item = (id, text) => {
    if (!text) text = "N/A";
    document.getElementById(id).textContent = text;
}

const populate_image = (url) => {
    const outer_div = document.createElement("div");
    outer_div.classList.add("col-md-4", "mb-4", "mx-auto");
    const inner_div = document.createElement("div");
    inner_div.classList.add("card");
    const img = document.createElement("img");
    img.src = url;
    img.classList.add("card-img-top");
    inner_div.append(img);
    outer_div.append(inner_div);
    document.getElementById("notice_det_imgs").append(outer_div);
}
const populate_notice_url = (url) => {
    const atag = document.getElementById("notice_det_url");
    atag.href = url;
    atag.textContent = url;
}

const populate_last_fetched_date = (data) => {
    format_dates_in_notice(data)
    populate_text_item("notice_det_last_fetch", data.last_fetched_date);
}

const populate_notice_detail = (data) => {
    format_dates_in_notice(data);
    populate_text_item("notice_det_id", data.notice_id);
    populate_text_item("notice_det_name", `${data.name}, ${data.forename}`)
    populate_text_item("notice_det_dob", data.date_of_birth)
    populate_text_item("notice_det_nations", get_fullnames_from_codes(data.nationalities, COUNTRIES))
    populate_text_item("notice_det_langs", get_fullnames_from_codes(data.languages_spoken_ids, LANGUAGES))
    populate_text_item("notice_det_sex", SEXES[data.sex_id]);
    populate_text_item("notice_det_height", data.height)
    populate_text_item("notice_det_weight", data.weight)
    populate_text_item("notice_det_last_fetch", data.last_fetched_date);
    populate_text_item("notice_det_last_mod", data.last_modified_date);
    populate_text_item("notice_det_first_fetch", data.first_fetched_date);
    populate_text_item("notice_det_dist_marks", data.distinguishing_marks);
    populate_text_item("notice_det_eyes", get_fullnames_from_codes(data.eyes_colors_id, EYES));
    populate_text_item("notice_det_hairs", get_fullnames_from_codes(data.hairs_id, HAIRS));
    populate_text_item("notice_det_place_birth", data.place_of_birth);
    populate_text_item("notice_det_country_birth", COUNTRIES[data.country_of_birth_id])
    populate_notice_url(data.url)

    document.getElementById("notice_det_imgs").innerHTML = ""
    data.image_ids.forEach(image_id => {
        const url = `${data.url}/images/${image_id}`;
        populate_image(url);
    })

    document.getElementById("notice_det_warrants").innerHTML = "";
    data.arrest_warrants.forEach(arrest_warrant => {
        populate_arrest_warrant(arrest_warrant.charge, arrest_warrant.charge_translation, COUNTRIES[arrest_warrant.issuing_country_id])
    });
}

async function fetch_and_populate_details(url) {
    try {
        const response = await fetch(get_cache_busted_url(url));
        if (!response.ok) {
            throw new Error(`Got http status code: ${response.status}`);
        }
        const notice_data = await response.json();
        populate_notice_detail(notice_data);
    } catch (err) {
        console.log(`Failed to load notice detail: ${err}`);
    }
}

const main = () => {
    fetch_and_populate_details(`/api/notice/${NOTICE_ID}`)
    const socket = io.connect("/")
    socket.on("notice_update", (data) => {
        const update_type = data.update_type;
        const changed_data = data.changed_data;
        if (update_type === "refetched") {
            populate_last_fetched_date(changed_data);
        } else if (data.notice_id == NOTICE_ID) {
            populate_notice_detail(changed_data);
        }
        show_alert(`Notice: ${data.notice_id} ${update_type}`, "success");

    });
};

main();