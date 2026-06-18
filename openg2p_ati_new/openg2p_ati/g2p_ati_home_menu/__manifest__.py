# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
{
    "name": "G2P ATI Home Menu",
    "summary": "Show the app grid as the ATI backend landing page",
    "category": "G2P",
    "version": "17.0.1.0.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": ["g2p_ati", "muk_web_theme"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "g2p_ati_home_menu/static/src/home_menu/home_menu.xml",
            "g2p_ati_home_menu/static/src/home_menu/home_menu.js",
            "g2p_ati_home_menu/static/src/home_menu/home_menu.scss",
        ],
    },
    "demo": [],
    "images": [],
    "application": False,
    "installable": True,
    "auto_install": False,
}

