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
        menu: ".menu-content",
        richText: ".blog-body"
    },
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
    const delay = el.dataset.delay || Math.min(index * 90, 360);
    el.style.transitionDelay = `${delay}ms`;
};

// ==============================
// FADE-IN MODULE
// ==============================
// Reveals elements individually as each one actually enters the
// viewport, rather than as whole page sections all at once. Elements
// that cross into view together (e.g. a row of gallery tiles) are
// given a small staggered delay so they still read as a sequence.
const Fade = (() => {

    // Markdown-rendered article bodies are a single blob of HTML we
    // don't control node-by-node, so tag each top-level block (each
    // paragraph, heading, image, etc.) as its own fade-in target.
    function prepareRichText() {
        $$(CONFIG.selectors.richText).forEach(body => {
            Array.from(body.children).forEach(child => {
                child.classList.add("fade-in");
            });
        });
    }

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
        prepareRichText();

        const items = $$(CONFIG.selectors.items);

        if ("IntersectionObserver" in window) {
            const observer = new IntersectionObserver((entries, obs) => {
                entries
                    .filter(entry => entry.isIntersecting)
                    .forEach((entry, index) => {
                        const el = entry.target;
                        applyDelay(el, index);
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
        requestAnimationFrame(() => {
            img.classList.add("loaded");
            item.classList.add("visible");
        });
    }

    function processItem(item, img, index) {
        reveal(item, img, index);
    }

    function apply(items) {
        items.forEach((item, index) => {
            const img = $("img", item);
            if (!img) return;

            if (img.complete) {
                processItem(item, img, index);
            } else {
                img.onload = () => processItem(item, img, index);
            }
        });
    }

    return { apply };
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
    UI.init();
}

document.addEventListener("DOMContentLoaded", init);