document.addEventListener('DOMContentLoaded', () => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
            // Get the target from the "data-target" attribute
            const $target = document.getElementById(el.dataset.target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
            
        });
    });
});

function user_search(event, form) {
    event.preventDefault();

    if ((new FormData(form)).get("search") == "") {
        form.classList.remove("is-active");
        document.getElementById("user_search_results").innerHTML = "";
        return;
    }
    form.classList.add("is-active");

    fetch(form.action, {
        method: 'POST',
        body: new URLSearchParams(new FormData(form))
    }).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    }).then((body) => {
        let user_search_results = "";
        for (user of body) {
            user_search_results += `
                <a href="/user/${user.id}" class="card dropdown-item p-1">
                    <div class="card-content p-1 mb-1">
                        <div class="media">
                            <div class="media-left">
                                <figure class="image is-48x48">
                                    <img src="${user.picture_url}" style="max-height: 100%;" alt="Placeholder image">
                                </figure>
                            </div>
                            <div class="media-content">
                                <p class="title is-4">${user.username}</p>
                            </div>
                        </div>
                    </div>
                </a>`
        }
        document.getElementById("user_search_results").innerHTML = user_search_results;
    }).catch((error) => {
        // TODO handle error
    });
}

function check_post_length(input) {
    if (input.value.length >= input.maxLength) {
        document.getElementById("input_error").classList.remove("is-hidden");
    }
    else {
        document.getElementById("input_error").classList.add("is-hidden");
    }
}

function send_reset_code(event, form) {
    event.preventDefault();

    fetch(form.action, {
        method: 'POST',
        body: new URLSearchParams(new FormData(form))
    }).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    }).then((body) => {
        if (body.status == "success") {
            document.getElementById("reset_error").classList.add("is-hidden");
            document.getElementById("reset_submit").classList.remove("is-hidden");
        }
        else {
            document.getElementById("reset_error").textContent = body.error;
            document.getElementById("reset_error").classList.remove("is-hidden");
            document.getElementById("reset_submit").classList.add("is-hidden");
        }
    }).catch((error) => {
        // TODO handle error
    });
}