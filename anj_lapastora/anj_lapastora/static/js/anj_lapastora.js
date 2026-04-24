// ==============================
// CONFIG
// ==============================
const CONFIG = {
    selectors: {
        items: ".item, .fade-in",
        galleryItems: ".item",
        gallery: "#gallery",
        images: "img",
        burger: "#burger",
        nav: "#mobileNav",
        menu: ".menu-content"
    },
    layouts: [
        "span-3x4",
        "span-2x4",
        "span-4x5",
        "span-2x3",
        "span-3x3",
        "span-1x2"
    ],
    scrollOffset: 200
};

// ==============================
// STATE
// ==============================
const state = {
    page: 2,
    loading: false,
    hasNext: true
};

// ==============================
// UTILITIES
// ==============================
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => ctx.querySelectorAll(sel);

const applyDelay = (el, index = 0) => {
    if (!el.classList.contains("fade-in")) return;
    const delay = el.dataset.delay || index * 100;
    el.style.transitionDelay = `${delay}ms`;
};

// ==============================
// FADE-IN MODULE
// ==============================
const Fade = (() => {

    function fallback() {
        $$(CONFIG.selectors.items).forEach((item, index) => {
            const rect = item.getBoundingClientRect();

            if (rect.top < window.innerHeight - 25) {
                applyDelay(item, index);
                item.classList.add("visible");
            }
        });
    }

    function init() {
        const items = $$(CONFIG.selectors.items);

        if ("IntersectionObserver" in window) {
            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (!entry.isIntersecting) return;

                    const el = entry.target;
                    applyDelay(el);
                    el.classList.add("visible");
                    obs.unobserve(el);
                });
            }, {
                rootMargin: "0px 0px -50px 0px",
                threshold: 0
            });

            items.forEach(item => observer.observe(item));
        } else {
            fallback();
            window.addEventListener("scroll", fallback);
        }
    }

    return { init };
})();

// ==============================
// LAYOUT + IMAGE MODULE
// ==============================
const Layout = (() => {

    function reveal(item, img, index) {
        setTimeout(() => {
            img.classList.add("loaded");
            item.classList.add("visible");
        }, index * 60);
    }

    function apply(items) {
        items.forEach((item, index) => {
            const layout = CONFIG.layouts[Math.floor(Math.random() * CONFIG.layouts.length)];
            item.classList.add(layout);

            const img = $("img", item);
            if (!img) return;

            if (img.complete) {
                reveal(item, img, index);
            } else {
                img.onload = () => reveal(item, img, index);
            }
        });
    }

    return { apply };
})();

// ==============================
// INFINITE SCROLL MODULE
// ==============================
const InfiniteScroll = (() => {

    function shouldLoad() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - CONFIG.scrollOffset;
    }

    function load() {
        if (state.loading || !state.hasNext || !shouldLoad()) return;

        state.loading = true;

        fetch(`?page=${state.page}`)
            .then(res => res.text())
            .then(html => {
                const doc = new DOMParser().parseFromString(html, "text/html");
                const newItems = $$(CONFIG.selectors.galleryItems, doc);

                if (!newItems.length) {
                    state.hasNext = false;
                    return;
                }

                const gallery = $(CONFIG.selectors.gallery);
                newItems.forEach(item => gallery.appendChild(item));

                Layout.apply(newItems);

                state.page++;
            })
            .finally(() => {
                state.loading = false;
            });
    }

    function init() {
        window.addEventListener("scroll", load);
    }

    return { init };
})();

// ==============================
// UI MODULE (BURGER MENU)
// ==============================
const UI = (() => {

    function initMenu() {
        const burger = $(CONFIG.selectors.burger);
        const nav = $(CONFIG.selectors.nav);

        if (!burger || !nav) return;

        const menu = $(CONFIG.selectors.menu, nav);
        if (!menu) return;

        const toggle = () => {
            nav.classList.toggle("active");
            document.body.classList.toggle("no-scroll");
        };

        const close = () => {
            nav.classList.remove("active");
            document.body.classList.remove("no-scroll");
        };

        burger.addEventListener("click", toggle);

        nav.addEventListener("click", (e) => {
            if (!menu.contains(e.target)) close();
        });

        $$("a", menu).forEach(link => {
            link.addEventListener("click", close);
        });
    }

    function disableImageContextMenu() {
        $$(CONFIG.selectors.images).forEach(img => {
            img.addEventListener("contextmenu", e => e.preventDefault());
        });
    }

    return {
        init: () => {
            initMenu();
            disableImageContextMenu();
        }
    };
})();

// ==============================
// INIT
// ==============================
function init() {
    const items = $$(CONFIG.selectors.galleryItems);

    Layout.apply(items);
    Fade.init();
    InfiniteScroll.init();
    UI.init();
}

document.addEventListener("DOMContentLoaded", init);