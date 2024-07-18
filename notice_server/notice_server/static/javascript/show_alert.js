
export const show_alert = (message, type) => {
    var alert_id = "alert_" + new Date().getTime();

    var alert_div = document.createElement("div");
    alert_div.id = alert_id;
    alert_div.classList.add("alert", "alert-" + type, "alert-dismissible", "fade", "show");
    alert_div.setAttribute("role", "alert");

    var message_node = document.createTextNode(message);
    alert_div.appendChild(message_node);

    var close_button = document.createElement("button");
    close_button.type = "button";
    close_button.classList.add("close");
    close_button.setAttribute("data-dismiss", "alert");
    close_button.setAttribute("aria-label", "Close");

    var closeSpan = document.createElement("span");
    closeSpan.setAttribute("aria-hidden", "true");
    closeSpan.innerHTML = "&times;";

    close_button.appendChild(closeSpan);
    alert_div.appendChild(close_button);

    var alert_container = document.getElementById("alert-container");
    alert_container.appendChild(alert_div);

    setTimeout(() => {
        document.getElementById(alert_id).remove();
    }, 3000);
}
