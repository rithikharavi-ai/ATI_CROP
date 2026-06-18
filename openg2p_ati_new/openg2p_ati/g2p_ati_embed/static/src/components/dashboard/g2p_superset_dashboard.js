/** @odoo-module */
import {Component, onWillStart, useState, useSubEnv} from "@odoo/owl";
import {getDefaultConfig} from "@web/views/view";
import {registry} from "@web/core/registry";

const DASHBOARD_RELOAD_PARAM = "odoo_iframe_reload";

export class G2PSupersetDashboardEmbedded extends Component {
    setup() {
        this.state = useState({
            isLoading: true,
            isFrameLoading: false,
            dashboardUrl: "",
            iframeKey: 0,
            iframeUrl: "",
            error: "",
        });

        const routerActionId = this.env.services.router?.current?.hash?.action;
        const actionId =
            this.props.actionId || this.props.action?.id || this.env.config?.actionId || routerActionId;
        this.actionId = Number(actionId) || actionId;
        this.reloadSequence = 0;
        const orm = this.env.services.orm;

        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });





    //    let navbar;
    // let isVisible = false;  // 🧠 Track current visibility manually

    // onMounted(() => {
    //     navbar = document.querySelector(".o_main_navbar");
    //     if (!navbar) return;

    //     this._originalDisplay = navbar.style.display;

    //     // Initially hide
    //     navbar.style.display = "none";
    //     isVisible = false;

    //     // Hover behavior
    //     this._showNavbar = () => {
    //         navbar.style.display = "flex";
    //         isVisible = true;
    //     };

    //     this._hideNavbar = () => {
    //         navbar.style.display = "none";
    //         isVisible = false;
    //     };

    //     navbar.addEventListener("mouseenter", this._showNavbar);
    //     navbar.addEventListener("mouseleave", this._hideNavbar);

    //     // ✅ Escape toggles visibility
    //     this._handleKeyDown = (e) => {
    //         if (e.key === "Escape") {
    //             if (isVisible) {
    //                 this._hideNavbar();
    //             } else {
    //                 this._showNavbar();
    //             }
    //         }
    //     };

    //     document.addEventListener("keydown", this._handleKeyDown);
    // });

    // onWillUnmount(() => {
    //     if (!navbar) return;

    //     navbar.removeEventListener("mouseenter", this._showNavbar);
    //     navbar.removeEventListener("mouseleave", this._hideNavbar);
    //     document.removeEventListener("keydown", this._handleKeyDown);

    //     // Restore default style
    //     navbar.style.display = this._originalDisplay || "";
    // });



    







        onWillStart(() => this.loadDashboards(orm));
    }

    getDashboardIframeUrl(url) {
        this.reloadSequence += 1;
        const reloadToken = `${Date.now()}_${this.reloadSequence}`;

        try {
            const dashboardUrl = new URL(url, window.location.origin);
            dashboardUrl.searchParams.set(DASHBOARD_RELOAD_PARAM, reloadToken);
            return dashboardUrl.href;
        } catch {
            const separator = url.includes("?") ? "&" : "?";
            return `${url}${separator}${DASHBOARD_RELOAD_PARAM}=${encodeURIComponent(reloadToken)}`;
        }
    }

    setDashboardUrl(url) {
        const dashboardUrl = (url || "").trim();
        this.state.dashboardUrl = dashboardUrl;
        this.state.iframeKey += 1;
        this.state.iframeUrl = dashboardUrl ? this.getDashboardIframeUrl(dashboardUrl) : "";
        this.state.isFrameLoading = Boolean(dashboardUrl);
    }

    reloadDashboard() {
        if (!this.state.dashboardUrl) {
            return;
        }
        this.state.error = "";
        this.setDashboardUrl(this.state.dashboardUrl);
    }

    onIframeLoad() {
        this.state.isFrameLoading = false;
    }

    onIframeError() {
        this.state.isFrameLoading = false;
        this.state.error = "Dashboard failed to load. Please reload the dashboard.";
    }

    async loadDashboards(orm) {
        try {
            if (!this.actionId) {
                this.setDashboardUrl("");
                this.state.error = "Dashboard action was not loaded. Please reopen the menu.";
                return;
            }

            const data = await orm.searchRead(
                "g2p.superset.dashboard.config",
                [["action", "=", this.actionId]],
                ["url"],
                {limit: 1}
            );

            this.setDashboardUrl(data[0]?.url || "");
            this.state.error = this.state.dashboardUrl ? "" : "No dashboard is configured for this menu.";
        } catch (error) {
            console.error("Error loading Superset dashboard:", error);
            this.setDashboardUrl("");
            this.state.error = "Unable to load the Superset dashboard.";
        } finally {
            this.state.isLoading = false;
        }
    }
}
G2PSupersetDashboardEmbedded.template = "g2p_ati_embed.G2PSupersetDashboardEmbedded";
registry.category("actions").add("g2p.superset_dashboard_embedded", G2PSupersetDashboardEmbedded);
