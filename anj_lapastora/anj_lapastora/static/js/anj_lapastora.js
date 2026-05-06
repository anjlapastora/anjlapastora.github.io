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
        "span-3x3",
    ],
    scrollOffset: 200,
    ratios: {
        portrait: { width: "420px", aspect: "4/5" },
        landscape: { width: "480px", aspect: "3/2" }
    }
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
        requestAnimationFrame(() => {
            img.classList.add("loaded");
            item.classList.add("visible");
        });
    }

    function processItem(item, img, index) {
        const isPortrait = img.naturalHeight > img.naturalWidth;
        const type = isPortrait ? 'portrait' : 'landscape';
        item.classList.add(type);

        const mt = Math.floor(Math.random() * 120 + 30); 

        item.style.marginTop = `${mt}px`;
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