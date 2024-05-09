$(document).ready(function () {
  // alert
  init_alert();
  // search
  init_search();
  // notification
  init_notification();
});

const init_alert = () => {
  window.setTimeout(function () {
    const alertElement = document.getElementById("alert");
    if (typeof alertElement != "undefined" && alertElement != null) {
      document.getElementById("alert").classList.add("d-none");
    }
  }, 2500);
};

const init_search = () => {
  const search = document.getElementById("search");
  search.addEventListener("focus", function () {
    location.href = "/search";
  });
};

const handle_page_click = async (page) => {
  if (page === undefined || page === null || page === "") {
    console.log("page", page);
    return false;
  }

  // current page do not fetch again
  current_page = document
    .querySelector(".page-item.active")
    .querySelector("a").textContent;
  if (page === parseInt(current_page)) {
    return false;
  }

  // re-render
  re_render({ page: page });
};

const re_render = async (paramsToAdd = {}, keysToRemove = []) => {
  // get render id
  const render_id = document.getElementById("render-id").textContent;
  if (render_id === "undefined" || render_id === null || render_id === "") {
    console.error("render id is missing");
    return false;
  }

  // get render url
  let render_url = document.getElementById("render-url").textContent;
  if (render_url === undefined || render_url === null || render_url === "") {
    console.error("render url is missing");
    return false;
  }

  // create new render url
  let new_render_url;

  // add specified parameters
  if (Object.keys(paramsToAdd).length > 0) {
    new_render_url = create_add_param_render_url(render_url, paramsToAdd);
  }

  // remove specified parameters
  if (keysToRemove.length > 0) {
    new_render_url = create_remove_param_render_url(
      new_render_url,
      keysToRemove
    );
  }

  // update render url
  document.getElementById("render-url").innerHTML = new_render_url;

  // fetch page content
  const response = await getFetch(new_render_url)()();

  // re-render search results, client side rendering here
  document.getElementById(render_id).innerHTML = response;
};

const create_add_param_render_url = (render_url, paramsArray) => {
  const url = new URL(render_url, window.location.origin);

  const params = url.searchParams;
  Object.entries(paramsArray).forEach(([key, value]) => {
    params.set(key, value);
  });
  url.search = params.toString();

  return `${url.pathname}${url.search}${url.hash}`;
};

const create_remove_param_render_url = (render_url, keyArray) => {
  const url = new URL(render_url, window.location.origin);

  const params = url.searchParams;
  keyArray.forEach((key) => {
    params.delete(key);
  });
  url.search = params.toString();

  return `${url.pathname}${url.search}${url.hash}`;
};

const init_notification = () => {
  const notice = document.getElementById("notice");
  if (notice === undefined || notice === null) {
    return false;
  }

  const notification = document.getElementById("notification");
  if (notification === undefined || notice === null) {
    return false;
  }

  notice.addEventListener("click", function () {
    if (notification.classList.contains("d-none")) {
      notification.classList.remove("d-none");
    } else {
      notification.classList.add("d-none");
    }
  });

  const notification_close = document.getElementById("closeNotification");
  if (notification_close === undefined || notification_close === null) {
    return false;
  }

  notification_close.addEventListener("click", function () {
    notification.classList.add("d-none");
  });
};
