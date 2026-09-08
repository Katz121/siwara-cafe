(function() {
    try {
        const STORAGE_KEY = 'takuapa-trip';
        let listeners = [];

        function getList() {
            try {
                const data = localStorage.getItem(STORAGE_KEY);
                return data ? JSON.parse(data) : [];
            } catch (e) {
                return [];
            }
        }

        function saveList(list) {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
            } catch (e) {
                // Ignore errors like quota exceeded or private mode restrictions
            }
        }

        function notify() {
            const list = getList();
            
            // Notify subscribers
            listeners.forEach(fn => {
                try {
                    fn(list);
                } catch (e) {}
            });
            
            // Update UI
            updateDOM(list);
        }

        function updateDOM(list) {
            try {
                // Update toggle buttons
                const buttons = document.querySelectorAll('[data-trip-add]');
                buttons.forEach(btn => {
                    try {
                        const id = btn.getAttribute('data-trip-add');
                        if (id) {
                            const isInTrip = list.includes(id);
                            btn.textContent = isInTrip ? 'อยู่ในทริปแล้ว' : 'เพิ่มลงทริป';
                            btn.setAttribute('aria-pressed', isInTrip ? 'true' : 'false');
                        }
                    } catch (err) {}
                });

                // Update count displays
                const countEls = document.querySelectorAll('[data-trip-count]');
                countEls.forEach(el => {
                    try {
                        el.textContent = list.length;
                        el.hidden = list.length === 0;
                    } catch (err) {}
                });

                // Update badge visibility
                const badges = document.querySelectorAll('[data-trip-badge]');
                badges.forEach(badge => {
                    try {
                        badge.hidden = list.length === 0;
                    } catch (err) {}
                });
            } catch (e) {}
        }

        const TakuaTrip = {
            list: function() {
                return getList();
            },
            has: function(id) {
                return getList().includes(id);
            },
            add: function(id) {
                try {
                    const list = getList();
                    if (!list.includes(id)) {
                        list.push(id);
                        saveList(list);
                        notify();
                    }
                } catch (e) {}
            },
            remove: function(id) {
                try {
                    let list = getList();
                    if (list.includes(id)) {
                        list = list.filter(item => item !== id);
                        saveList(list);
                        notify();
                    }
                } catch (e) {}
            },
            toggle: function(id) {
                try {
                    if (TakuaTrip.has(id)) {
                        TakuaTrip.remove(id);
                    } else {
                        TakuaTrip.add(id);
                    }
                } catch (e) {}
            },
            clear: function() {
                try {
                    saveList([]);
                    notify();
                } catch (e) {}
            },
            count: function() {
                return getList().length;
            },
            on: function(fn) {
                try {
                    if (typeof fn === 'function') {
                        listeners.push(fn);
                    }
                } catch (e) {}
            }
        };

        window.TakuaTrip = TakuaTrip;

        function init() {
            try {
                updateDOM(getList());
                
                document.addEventListener('click', (e) => {
                    try {
                        const btn = e.target.closest('[data-trip-add]');
                        if (btn) {
                            const id = btn.getAttribute('data-trip-add');
                            if (id) {
                                TakuaTrip.toggle(id);
                            }
                        }
                    } catch (err) {}
                });
            } catch (e) {}
        }

        // Initialize safely
        try {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', init);
            } else {
                init();
            }
        } catch (e) {}

        // Listen for changes from other tabs
        window.addEventListener('storage', (e) => {
            try {
                if (e.key === STORAGE_KEY) {
                    notify();
                }
            } catch (err) {}
        });

    } catch (e) {
        // Ultimate fallback to prevent any errors from escaping
        console.error('TakuaTrip initialization failed', e);
    }
})();
