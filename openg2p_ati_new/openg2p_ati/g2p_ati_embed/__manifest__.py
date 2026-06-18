# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
{
    "name": "G2P ATI Embed",
    "category": "G2P",
    "version": "17.0.1.2.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "",
    "license": "Other OSI approved licence",
    "depends": ["base", "web"],
    "external_dependencies": {},
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/superset_dashboard_embedding_views.xml",
        "views/superset_dashboard_config_views.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "assets": {
        "web.assets_backend": [
            "g2p_ati_embed/static/src/components/**/*.js",
            "g2p_ati_embed/static/src/components/**/*.xml",
            "g2p_ati_embed/static/src/components/**/*.css",
            "g2p_ati_embed/static/src/components/**/*.scss",
        ],
    },
    "uninstall_hook": "uninstall_hook",
}
