import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)



class G2PCropProduction(models.Model):
    _name = "g2p.crop.production"
    _description = "Crop Production Details"
    _rec_name = "name"

    name = fields.Char(
        string="Reference",
        readonly=True,
        copy=False,
        default="New",
    )

    crop_registry_id = fields.Many2one(
        "g2p.crop.registry",
        string="Crop Registry",
        ondelete="cascade",
        required=True,
    )

    season_id = fields.Many2one(
        "g2p.season",
        string="Season",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('g2p.crop.production') or 'New'
        return super().create(vals_list)


    # ── Farmer & Plot Identity relays ────────────────────
    reg_farmer_id = fields.Char(related="crop_registry_id.farmer_id", string="Farmer ID", readonly=True)
    reg_fyda_id = fields.Char(related="crop_registry_id.fyda_id", string="Fayda ID", readonly=True)
    reg_farmer_display_id = fields.Char(related="crop_registry_id.farmer_display_id", string="Farmer Name", readonly=True)
    reg_land_id = fields.Many2one('g2p.land.information', related="crop_registry_id.land_info_id", string="Land ID", readonly=True)
    reg_ownership_type = fields.Selection(
        selection=[('private', 'Private'), ('leased', 'Leased'), ('government', 'Government')],
        related="crop_registry_id.ownership_type", string="Ownership Type", readonly=True)
    reg_land_area = fields.Float(related="crop_registry_id.land_area", string="Land Area (ha)", readonly=True)
    reg_land_category = fields.Selection(
        selection=[('seasonal', 'Seasonal'), ('horticulture', 'Horticulture')],
        related="crop_registry_id.land_category", string="Land Category", readonly=True)
    reg_soil_fertility = fields.Selection(
        selection=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        related="crop_registry_id.soil_fertility", string="Soil Fertility", readonly=True)
    reg_region_name_id = fields.Many2one("g2p.region", related="crop_registry_id.region_name_id", string="Region", readonly=True)
    reg_zone_name_id = fields.Many2one("g2p.zone", related="crop_registry_id.zone_name_id", string="Zone", readonly=True)
    reg_woreda_name_id = fields.Many2one("g2p.woreda", related="crop_registry_id.woreda_name_id", string="Woreda", readonly=True)
    reg_kebele_id = fields.Many2one('g2p.kebele', related="crop_registry_id.kebele_id", string="Kebele", readonly=True)

    # ── Cultivation Details relays ────────────────────────
    reg_crop_name_id = fields.Many2one("g2p.crop", related="crop_registry_id.crop_name_id", string="Crop Name", readonly=True)
    reg_crop_category_id = fields.Many2one("g2p.crop.category", related="crop_registry_id.crop_category_id", string="Crop Category", readonly=True)
    reg_crop_variety_id = fields.Many2one("g2p.crop.variety", related="crop_registry_id.crop_variety_id", string="Crop Variety", readonly=True)
    reg_seed_class = fields.Selection(
        selection=[('certified', 'Certified'), ('basic', 'Basic'), ('pre-basic', 'Pre-Basic')],
        related="crop_registry_id.actual_seed_class", string="Seed Class", readonly=True)
    reg_crop_seasons = fields.One2many("g2p.crop.season.line", related="crop_registry_id.crop_season_ids", string="Crop Seasons", readonly=True)
    reg_crop_planned_area = fields.Float(related="crop_registry_id.crop_planned_area", string="Planned Crop Area (ha)", readonly=True)
    reg_crop_expected = fields.Float(related="crop_registry_id.crop_expected", string="Expected Yield (quintals)", readonly=True)
    reg_actual_seed_qty = fields.Float(related="crop_registry_id.actual_seed_qty", string="Actual Seed Qty (kg)", readonly=True)

    # ── Fertilizer relay fields ────────────────────────────
    reg_seed_planned_fertilizer_type = fields.Selection(
        selection=[
            ('organic', 'Organic Fertilizers (Natural & Soil-Friendly)'),
            ('nitrogen', 'Nitrogen Fertilizers (For Leaf Growth)'),
            ('phosphorus', 'Phosphorus Fertilizers (For Root & Flower Growth)'),
            ('potassium', 'Potassium Fertilizers (For Strength & Disease Resistance)'),
            ('npk', 'Complex / Mixed Fertilizers (NPK)'),
            ('micronutrient', 'Micronutrient Fertilizers (Small but Essential)'),
        ],
        related="crop_registry_id.seed_planned_fertilizer_type",
        string="Planned Fertilizer Type", readonly=True)
    reg_seed_planned_fertilizer_name = fields.Many2one(
        'g2p.fertilizer',
        related="crop_registry_id.seed_planned_fertilizer_name",
        string="Planned Fertilizer Name", readonly=True)
    reg_actual_fertilizer_type = fields.Selection(
        selection=[
            ('organic', 'Organic Fertilizers (Natural & Soil-Friendly)'),
            ('nitrogen', 'Nitrogen Fertilizers (For Leaf Growth)'),
            ('phosphorus', 'Phosphorus Fertilizers (For Root & Flower Growth)'),
            ('potassium', 'Potassium Fertilizers (For Strength & Disease Resistance)'),
            ('npk', 'Complex / Mixed Fertilizers (NPK)'),
            ('micronutrient', 'Micronutrient Fertilizers (Small but Essential)'),
        ],
        related="crop_registry_id.actual_fertilizer_type",
        string="Actual Fertilizer Type", readonly=True)
    reg_actual_fertilizer_name = fields.Many2one(
        'g2p.fertilizer',
        related="crop_registry_id.actual_fertilizer_name",
        string="Actual Fertilizer Name", readonly=True)


    # ── Sowing ───────────────────────────────────────────────
    sowing_status = fields.Selection([
        ('sown', 'Sown'),
        ('not_sown', 'Not Sown'),
    ], string="Sowing Status")

    cluster_status = fields.Selection([
        ('clustered', 'Clustered'),
        ('independent', 'Independent'),
    ], string="Cluster Status")

    sown_area = fields.Float(string="Sown Area (ha)")
    sown_by_tractor = fields.Float(string="Sown by Tractor (ha)")
    actual_sowing_date = fields.Date(string="Actual Sowing Date")

    mechanization_rate_sowing = fields.Float(
        string="Mechanization Rate – Sowing (%)",
        compute="_compute_mech_rate",
        store=True,
    )

    # ── Harvest (visible when Sowing Status = Sown) ──────────
    crop_maturity_status = fields.Selection([
        ('green', 'Not Yet Ready'),
        ('yellow', 'Ready for Harvest'),
    ], string="Crop Maturity Status")

    harvest_date = fields.Date(string="Harvest Date")
    area_harvested = fields.Float(string="Area Harvested (ha)")
    qty_harvested = fields.Float(string="Quantity Harvested (quintal)")
    post_harvest_loss_pct = fields.Float(string="Post-harvest Loss (%)")
    qty_stored = fields.Float(string="Quantity Stored")
    qty_sold = fields.Float(string="Quantity Sold")

    # ── Harvest Method ───────────────────────────────────────
    harvest_method = fields.Many2one('g2p.machinery', string="Harvest Method")

    harvest_method_area = fields.Float(string="Harvest Method Area (ha)")

    # ── Production Result (computed) ─────────────────────────
    yield_per_ha = fields.Float(
        string="Yield (kg/ha)",
        compute="_compute_production_results",
        store=True,
    )
    yield_performance_pct = fields.Float(
        string="Yield Performance (%)",
        compute="_compute_production_results",
        store=True,
    )
    land_utilization_rate = fields.Float(
        string="Land Utilization Rate",
        compute="_compute_production_results",
        store=True,
    )
    seed_productivity = fields.Float(
        string="Seed Productivity",
        compute="_compute_production_results",
        store=True,
    )

    @api.constrains('actual_sowing_date')
    def _check_actual_sowing_date(self):
        for rec in self:
            if rec.actual_sowing_date and rec.actual_sowing_date > fields.Date.today():
                raise ValidationError("Actual Sowing Date cannot be a future date.")

    @api.onchange('actual_sowing_date')
    def _onchange_actual_sowing_date(self):
        if self.actual_sowing_date and self.actual_sowing_date > fields.Date.today():
            self.actual_sowing_date = False
            return {
                'warning': {
                    'title': 'Invalid Date',
                    'message': 'Actual Sowing Date cannot be a future date. Please select today or a past date.'
                }
            }

    # ── Computes ─────────────────────────────────────────────
    @api.depends('sown_area', 'sown_by_tractor')
    def _compute_mech_rate(self):
        for rec in self:
            rec.mechanization_rate_sowing = (
                (rec.sown_by_tractor / rec.sown_area * 100)
                if rec.sown_area else 0.0
            )

    @api.depends(
        'qty_harvested', 'area_harvested',
        'crop_registry_id.crop_expected',
        'crop_registry_id.actual_yield',
        'crop_registry_id.crop_planned_area',
        'crop_registry_id.actual_seed_qty',
    )
    def _compute_production_results(self):
        for rec in self:
            # Yield (kg/ha) = Qty Harvested ÷ Area Harvested
            rec.yield_per_ha = (
                rec.qty_harvested / rec.area_harvested
                if rec.area_harvested else 0.0
            )
            # Yield Performance % = (Actual Yield ÷ Expected Yield) × 100
            expected = rec.crop_registry_id.crop_expected
            actual = rec.crop_registry_id.actual_yield
            rec.yield_performance_pct = (
                (actual / expected * 100)
                if expected else 0.0
            )
            # Land Utilization Rate = Actual Area ÷ Planned Area
            planned_area = rec.crop_registry_id.crop_planned_area
            rec.land_utilization_rate = (
                rec.area_harvested / planned_area
                if planned_area else 0.0
            )
            # Seed Productivity = Total Yield ÷ Seed Used (kg)
            seed_used = rec.crop_registry_id.actual_seed_qty
            _logger.info('seed_used: %s', seed_used)
            total_yield = rec.qty_harvested * 100  # convert quintal → kg
            _logger.info('total_yield: %s', total_yield)
            rec.seed_productivity = (
                total_yield / seed_used
                if seed_used else 0.0
            )
